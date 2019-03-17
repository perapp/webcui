# webcui

A Python package for creating Webcui apps. A Webcui app is to the web what a Command Line Interface app is for the command line.

The goal of Webcui is to make it as easy as possible for Python developers to share their Python app with the world.

Webcui features:
* Generate HTML forms from regular Python functions. Function parameters become input fields. Function is executed when the user submit the form.
* Use function decorators to add help text and better labels to fields.
* Build, test and deploy app with simple command line.
* Admin interface (a Webcui app of course :-p) to configure cloud provider and continous delivery pipeline.

## Installation
$ pip install webcui

## Usage

Here's an example of a simple Webcui app:
```
@param("Name", help="Your name")
@param("Number of spam", default=2, help="How much spam do you want?")
@param("Side", default="ham")
def cmd(name, n_spam, side):
   spams = n_spam * ["spam"]
   return f"No problem {name}, one order of {', '.join(spams)} and {side} coming up."

if __name__ == '__main__':
   webcui.run(cmd)
```

To run the Webcui app on your own computer run:
`$ python app.py --run`

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
