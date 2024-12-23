class Server:
    ip = 1
    def __init__(self):
        self.ip = Server.ip
        self.data = []
        self.router = None
        Server.ip += 1

    def get_ip(self):
        return self.ip

    def get_data(self):
        data = self.data.copy()
        self.data.clear()
        return data

    def send_data(self, data):
        if not self.router:
            return 'Sorry, this server is not connected at the moment.'
        self.router.buffer.append(data)


class Router:
    def __init__(self):
        self.servers = {}
        self.buffer = []

    def link(self, server):
        server.router = self
        self.servers[server.get_ip()] = server

    def unlink(self, server):
        if server.router == self:
            server.router = None
            del self.servers[server.get_ip()]

    def send_data(self):
        send_later = []
        while self.buffer:
            data = self.buffer.pop(0)
            if data.ip not in self.servers:
                send_later.append(data)
                continue
            self.servers[data.ip].data.append(data.data)
        self.buffer = send_later


class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip
