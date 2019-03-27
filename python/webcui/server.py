import responder
from dataclasses import dataclass
import inspect

@dataclass
class Parameter(object):
    name: str
    label: str

class Server(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.api = responder.API(templates_dir="www")
        self.api.add_route("/", self.on_get)

    def on_get(self, req, resp):
        doc = self.cmd.__doc__
        if not doc:
            doc = self.cmd.__name__

        spec = inspect.getfullargspec(self.cmd)
        params = [Parameter(x, "Foo")
                  for x in spec.args]
        resp.html = self.api.template("form.html",
                                      doc=doc,
                                      params=params)

    def run(self):
        api.run(address="0.0.0.0",
                port=8080)

    @property
    def requests(self):
        return self.api.requests

def run(cmd):
    Server(cmd).run()
