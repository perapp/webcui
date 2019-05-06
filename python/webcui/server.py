import responder
from dataclasses import dataclass
import inspect
import traceback
from .app import App

@dataclass
class Parameter(object):
    name: str
    label: str

class Server(object):
    def __init__(self, cmd=None, app=None):
        if app:
            self.app = app
        else:
            self.app = App(cmd)

        self.argspec = inspect.getfullargspec(self.app.cmd)
        self.api = responder.API(templates_dir="www")
        self.api.add_route("/", self.on_get)

    def on_get(self, req, resp):
        if req.params.get("run") == "true":
            try:
                result = self.run_cmd(req.params)
            except:
                result = f"Oops, the command generated an error\n{traceback.format_exc()}"
        else:
            result = None

        doc = self.app.cmd.__doc__
        if not doc:
            doc = self.app.cmd.__name__

        params = [Parameter(x, x)
                  for x in self.argspec.args]
        resp.html = self.api.template("form.html",
                                      doc=doc,
                                      params=params,
                                      result=result)

    def run_cmd(self, params):
        missing_args = set(self.argspec.args) - params.keys()
        if missing_args:
            raise ValueError(f"Mandatory parameter(s) missing: {', '.join(missing_args)}")

        paramv = [self.parse_arg(x, params[x])
                  for x in self.argspec.args]
        return self.app.cmd(*paramv)
    
    def parse_arg(self, name, value):
        type_ = self.argspec.annotations.get(name)
        if isinstance(type_, type):
            return type_(value)
        return value

    def run(self):
        self.api.run(address="0.0.0.0",
                     port=80)

    @property
    def requests(self):
        return self.api.requests

def run(cmd):
    Server(cmd).run()
