import responder

api = responder.API()

@api.route("/")
class Server:
    def __init__(self, cmd):
        self.cmd = cmd

    def on_get(self, req, resp):
        resp.html = api.template("form.html")

    def run(self):
        api.run(address="0.0.0.0",
                port=8080)

    @property
    def requests(self):
        return api.requests

def run(cmd):
    Server(cmd).run()
