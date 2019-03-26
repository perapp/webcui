import responder

api = responder.API()
cmds = []

@api.route("/")
def main(req, resp):
    resp.text = "Hello!"

def run(cmd):
    cmds.append(cmd)
    api.run()
