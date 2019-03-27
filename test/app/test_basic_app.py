import webcui
import bs4 as bs

def cmd(your_name):
   """A command greeting you"""
   return f"Hello {your_name}!"

def test_form():
   doc = bs.B.BeautifulSoup(api.requests.get("/").text)
   assert doc.find(id="your_name") is not None

if __name__ == '__main__':
   webcui.run(cmd)
