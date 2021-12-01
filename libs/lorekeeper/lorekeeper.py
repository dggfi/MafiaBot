import sys, traceback, logging
from uuid import uuid4 as uuidv4
import asyncio
import dataset

class LoreMixin:
    _save_attrs = None # columns
    _table_name = None

    def create_lore(self):
        return { k: getattr(self.subject, k) for k in self._save_attrs }

    def graft_lore(self, attrs):
        for (k, v) in attrs:
            setattr(self.subject, k, v)


class LoreEntry(LoreMixin):
    @property
    def subject(self):
        return self._subject
    
    @property
    def key(self):
        return self._key

    def __init__(self, subject):
        """

        """
        self._subject = subject
        self._key = uuidv4()


class Spread:
    def __init__(self, name):
        self.name = name
        self.entries = {}
    
    def clear(self):
        self.entries = {}


class LoreKeeper:
    def __init__(self, connection_uri='sqlite:///lore.db'):
       self.connection_uri = connection_uri
       self.database = dataset.connect(connection_uri)
       self.spreads = {} # table name: Spreads
       self.entries = {} # subject: LoreEntry

       logger = logging.getLogger('lorekeeper')
       logger.setLevel(logging.INFO)
       handler = logging.FileHandler(filename='logs/lorekeeper.log', encoding='utf-8', mode='w')
       handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
       logger.addHandler(handler)
       self.logger = logger

    def track(self, subject):
        entry = LoreEntry(subject)
        self.entries[subject] = entry
        self.add_entry(entry)

    def forget(self, subject):
        entry = self.entries.pop(subject, None)
        if entry:
            spread = self.spreads.pop(entry._table_name, None)
            if spread:
                spread.pop(entry._table_name)
            self.entries.pop(subject)

    def add_entry(self, entry):
        spread = self.spreads.get(entry._table_name, None)
        if not spread:
            spread = Spread(entry._table_name)
            self.spreads[entry._table_name] = spread
        spread.entries[entry.key] = entry
    
    def transcribe_sync(self):
        self.database.begin()
        try:
            for spread in self.spreads.values():
                lores = (entry.create_lore() for entry in spread.entries.values())
                table = self.database[spread.name]
                table.upsert_many(lores, ['key'])
        except Exception:
            self.logger.exception(f'Exception inside of transcribe_sync')
            self.database.rollback()
        else:
            self.database.commit()
    
    async def transcribe_async(self):
        self.database.begin()
        try: 
            for spread in self.spreads.values():
                table = self.database[spread.name]
                for entry in spread.entries.values():
                    table.upsert(entry.create_lore(), [entry.key])
                    await asyncio.sleep(0)
        except Exception:
            self.logger.exception(f'Exception inside of transcribe_async')
            self.database.rollback()
        else:
            self.database.commit()

    def search(self, entry, criteria, limit_one=True):
        table = self.database[entry._table_name]
        if limit_one:
            return table.find_one(**criteria)
        else:
            return table.find(**criteria)