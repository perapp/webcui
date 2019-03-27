import responder
from dataclasses import dataclass
import inspect

api = responder.API(templates_dir="www")

@dataclass
class Parameter(object):
    name: str
    label: str


@api.route("/")
class ServerImpl(object):
    def __init__(self):
        super().__init__()
        self.cmd = None

    def on_get(self, req, resp):
        # TODO: self.cmd is None since constructor is called from responder.
        print(self.cmd)
        doc = self.cmd.__doc__
        if not doc:
            doc = self.cmd.__name__

        spec = inspect.getfullargspec(self.cmd)
        params = [Parameter(x, "Foo")
                  for x in spec.args]
        resp.html = api.template("form.html",
                                 doc=doc,
                                 params=params)

    def run(self):
        api.run(address="0.0.0.0",
                port=8080)

    @property
    def requests(self):
        return api.requests

def Server(cmd):
    if cmd is None:
        raise ValueError("cmd argument must be specified")
    server = ServerImpl()
    server.cmd = cmd
    return server

def run(cmd):
    Server(cmd).run()
