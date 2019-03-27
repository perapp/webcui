"""
Tests for typed parameters.
"""
import webcui

def cmd(your_name: str, your_age: int):
   """A command greeting you"""
   return f"Hello {your_name}. {your_age} is a nice age!"

if __name__ == '__main__':
   webcui.run(cmd)
