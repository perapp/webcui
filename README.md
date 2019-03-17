# webcui

A Python package for creating Webcui apps. A Webcui app is to the web what a Command Line Interface app is for the command line.
The goal of Webcui is to make it as easy as possible for Python developers to share their Python app with the world.

Webcui features:
* Generate HTML forms from regular Python functions. Function parameters become input fields. Function is executed when the user submit the form.
* Use function decorators to add help text and better labels to fields.
* Build, test and deploy app with simple command line.
* Admin interface (a Webcui app of course :-p) to configure cloud provider and continous delivery pipeline.

## Installation
```
$ pip install webcui
```

## Usage

Here's an example of a simple Webcui app:
```python
from webcui import param, run, ParamValueError

@param("Number of spam", default=2, help="How much spam do you want?")
@param("Side", default="eggs")
def cmd(n_spam: int, side: str):
   """
   Calculate the price of a breakfast order.
   """
   if n_spam < 1:
      raise ParamValueError("Number of spam", "All our dishes has at least one spam.")
   spams = n_spam * ["spam"]
   dish = f"{', '.join(spams)} and {side}"
   price = n_spam * 1.5 + 2
   return f"The price of an order of {dish} is €{price}."

if __name__ == '__main__':
   run(cmd)
```

To run the Webcui app on your own computer run:
```
$ python app.py --run
```

To deploy to a cloud provider first configure your app using the admin tool and then run deploy.
```
$ python app.py --admin
$ python app.py --deploy
```
The configuration will be saved in webcui.conf

A continuous delivery pipeline can easily be configured using the commands:
```
$ python app.py --build
$ python app.py --test
$ python app.py --deploy
```
