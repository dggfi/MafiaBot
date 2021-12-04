from servman.helpers import ServmanAgent, action
from servman.typings import IParcel
from path import Path
from time import time_ns
import json


class PingerService(ServmanAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(connection_config=kwargs['connection_config'])

        # Connection details
        self.owner_id = kwargs['owner_id']
        self.owner_connection_id = kwargs['owner_connection_id']
        self.identifier = kwargs['identifier']

        # State
        self.t_refreshed = 0
        self.t_since_refresh = 0
        self.t_timeout = 5 # seconds


    # Tasks
    async def on_connect(self, websocket, queue):
        credentials_parcel: IParcel = {
            'routing': 'client',
            'destination_id': self.owner_connection_id,
            'action': 'catch_service_credentials',
            'data': {
                'identifier': self.identifier,
                'connection_id': websocket.request_headers['connection_id']
            }
        }

        await self._primary_websocket.send(json.dumps(credentials_parcel))

    # keepalive
    async def keepalive(self):
        await self.wait_until_connected()

        while self.t_since_refresh < self.t_timeout:
             self.t_since_refresh = (time_ns() - self.t_refreshed) / 1000000000
        
        client_parcel = {
            'routing': 'client',
            'destination': self.owner_connection_id,
            'action': 'close_service',
            'from': self._primary_connection_id
        }

        await self._primary_message_queue.put(json.dumps(client_parcel))

        servman_parcel = {
            'routing': 'servman',
            'action': 'close_service',
            'data': {
                'identifier': self.identifier
            }
        }

        await self._primary_message_queue.put(json.dumps(servman_parcel))


    @action()
    async def ping(self, parcel: IParcel, websocket, queue):
        self.t_refreshed = time_ns()
        self.t_since_refresh = 0
        T_SENT = parcel['data']['T_SENT']

        pong_parcel: IParcel = {
            'routing': 'client',
            'action': 'pong',
            'destination_id': self.owner_connection_id,
            'data': {
                'T_SENT': T_SENT,
                'T_ARRIVED': time_ns(),
                'identifier': self.identifier
            }
        }

        await self._primary_message_queue.put(json.dumps(pong_parcel))


def pinger_service(*args, **kwargs):
    config_file = Path("conf/pinger_config.json")
    if not config_file.exists():
        print("Error: Connection config for service does not exist!")
        exit()
    connection_config = json.loads(config_file.read_text(encoding='utf-8'))
    kwargs['connection_config'] = connection_config

    pinger_service = PingerService(*args, **kwargs)
    pinger_service.run()