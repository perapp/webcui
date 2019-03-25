import webcui

def cmd(your_name):
   """A command greeting you"""
   return f"Hello {your_name}!"

def test_form():
   assert webcui.make_form(cmd) == "<form/e>"

if __name__ == '__main__':
   webcui.run(cmd)
