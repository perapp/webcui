import webcui

def cmd(your_name):
   """A command greeting you"""
   return f"Hello {your_name}!"

if __name__ == '__main__':
   webcui.run(cmd)
