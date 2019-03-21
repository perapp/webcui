# webcui

A Python package for creating Webcui apps. A Webcui app is to the web what a Command Line Interface app is for the command line.
The goal of Webcui is to make it as easy as possible for Python developers to share their Python app with the world.

Webcui features:
* Generate HTML forms from regular Python functions. Function parameters become input fields. Function is executed when the user submit the form.
[//]: # * Use function decorators to add help text and better labels to fields. (Coming soon)
[//]: # * Build, test and deploy app with simple command line. (Coming soon)
[//]: # * Admin interface (a Webcui app of course :-p) to configure cloud provider and continous delivery pipeline. (Coming soon)

## Installation
Install Python 3.6 or later
```
$ pip install webcui
```

## Usage

Here's an example of a simple Webcui app:
```python
import webcui

def cmd(number_of_spam: int, side: str = "eggs"):
   """Calculate the price of a breakfast order."""
   spams = number_of_spam * ["spam"]
   dish = f"{', '.join(spams)} and {side}"
   price = number_of_spam * 1.5 + 2
   return f"The price of an order of {dish} is €{price:.2f}"

if __name__ == '__main__':
   webcui.run(cmd)
```

To run the Webcui app on your own computer run:
```
$ python app.py --run
```
