import asyncio

class Client(asyncio.Protocol):

    def connection_made(self, transport):
        self.connected = True
        # save the transport
        self.transport = transport

    def data_received(self, data):
        # forward data to the server
        self.server_transport.write(data)

    def connection_lost(self, *args):
        self.connected = False

class Server(asyncio.Protocol):
    clients = {}
    def connection_made(self, transport):
        # save the transport
        self.transport = transport

    @asyncio.coroutine
    def send_data(self, data):
        # get a client by its peername
        peername = self.transport.get_extra_info('peername')
        client = self.clients.get(peername)
        # create a client if peername is not known or the client disconnect
        if client is None or not client.connected:
            protocol, client = yield from loop.create_connection(
                Client, 'google.com', 80)
            client.server_transport = self.transport
            self.clients[peername] = client
        # forward data to the client
        client.transport.write(data)

    def data_received(self, data):
        # use a task so this is executed async
        asyncio.Task(self.send_data(data))

@asyncio.coroutine
def initialize(loop):
    # use a coroutine to use yield from and get the async result of
    # create_server
    server = yield from loop.create_server(Server, '127.0.0.1', 8888)

loop = asyncio.get_event_loop()

# main task to initialize everything
asyncio.Task(initialize(loop))

# run
loop.run_forever()
