from discord.commands import slash_command
from cogs.ext import AgentCog
from servman.typings import IParcel
from servman.helpers import action
from time import time_ns
import asyncio
import json
import types


class PingService:
    def __init__(self, ctx):
        self.owner = ctx.author
        self.messageable = ctx
        self.service_request_sent = False
        self.service_active = False
        self.identifier = f'pinger_service_pool_{ctx.author.id}'
        self.destination_id = None
        self.failed = False


class Ping(AgentCog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.agent_cog = None
        self.pending_services = {} # identifier: service
        self.active_services = {} # connection_id: service


    async def finalize(self):
        self.agent_cog = self.bot.get_cog('Agent')
        await self.agent_cog.servman_agent.wait_until_connected()

        async def on_service_created(agent, identifier, connection_id, websocket, queue):
            service = self.pending_services.pop(identifier)
            self.active_services[identifier] = service
            service.service_active = True
            service.destination_id = connection_id

        self.agent_cog.servman_agent.on_service_created = types.MethodType(on_service_created, self.agent_cog.servman_agent)

    async def wait_for_service_active(self, ctx):
        service = self.active_services.get(f'pinger_service_pool_{ctx.author.id}', None)
        print(service)
        if not service:
            service = PingService(ctx)

        while not service.service_active and not service.failed:
            if not service.service_request_sent:
                self.pending_services[service.identifier] = service

                agent_id = self.agent_cog.servman_agent._agent_id,
                connection_id = self.agent_cog.servman_agent._primary_websocket.request_headers['connection_id']
                identifier = service.identifier

                args = []
                kwargs = {
                    'owner_id': agent_id,
                    'owner_connection_id': connection_id,
                    'identifier': identifier

                }
                target = 'pinger_service'
                options = {}

                service_request_parcel: IParcel = {
                    'routing': 'servman',
                    'action': 'create_service',
                    'data': {
                        'args': args,
                        'kwargs': kwargs,
                        'target': target,
                        'options': options
                    },
                }

                await self.agent_cog.servman_agent._primary_message_queue.put(json.dumps(service_request_parcel))

                service.service_request_sent = True
            else:
                await asyncio.sleep(0)

    # Commands
    @slash_command(guild_ids=[843921354516332574])
    async def ping(self, ctx, name: str=None, wait=0):
        await self.wait_for_service_active(ctx)

        identifier = f'pinger_service_pool_{ctx.author.id}'
        service = self.active_services[identifier]
        
        name = name or ctx.author.name
        T_SENT = time_ns()
        
        ping_parcel: IParcel = {
            'routing': 'service',
            'action': 'ping',
            'destination_id': service.destination_id,
            'data': {
                'name': name,
                'T_SENT': T_SENT
            }
        }
        
        await self.agent_cog.servman_agent._primary_message_queue.put(json.dumps(ping_parcel))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@ Pinging")
    
    @action()
    async def pong(self, parcel: IParcel, websocket, queue):
        identifier = parcel['data']['identifier']
        service = self.active_services[identifier]
        T_SENT = parcel['data']['T_SENT']
        T_ARRIVED = parcel['data']['T_ARRIVED']
        T_DELTA = (T_ARRIVED - T_SENT) / 1000000
        T_RETURN = (time_ns() - T_ARRIVED) / 1000000

        msg = f'Hey, {service.owner.name}! It took {T_DELTA}ms for your message to arrive at the service, and an extra {T_RETURN}ms to travel back.'

        await service.messageable.respond(msg)
    
    @action()
    async def close_service(self, parcel: IParcel, websocket, queue):
        destination_id = parcel['data']['from']
        service = self.active_services.pop(destination_id)

        msg = f'Hey, we noticed you haven\'t pinged in a while, so we\'re closing this service.'

        await service.messageable.reply(content=msg)


def setup(bot):
    bot.add_cog(Ping(bot))