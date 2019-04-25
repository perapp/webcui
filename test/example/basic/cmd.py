import webcui

def cmd(number_of_spam: int, side: str = "eggs"):
   """Calculate the price of a breakfast order."""
   spams = number_of_spam * ["spam"]
   dish = f"{', '.join(spams)} and {side}"
   price = number_of_spam * 1.5 + 2
   return f"The price of an order of {dish} is €{price:.2f}"

if __name__ == '__main__':
   webcui.run(cmd)

########

def test_ex():
    server = webcui.Server(cmd)
    assert server.requests.get("/").text is not None

