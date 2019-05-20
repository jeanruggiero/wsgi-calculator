# !/usr/env/bin python

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import functools
import operator
import traceback


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    return str(sum(int(num) for num in args))


def subtract(*args):
    """Returns a STRING with the difference of the arguments"""
    return str(int(args[0]) - int(args[1]))


def multiply(*args):
    """Returns a STRING with the product of the arguments"""
    return str(functools.reduce(operator.mul, (int(num) for num in args)))


def divide(*args):
    """Returns a STRING with the quotient of the arguments"""
    return str(int(args[0])//int(args[1]))


def how_to(*args):
    """Returns simple instructions for using the calculator"""
    return """<h1>Web Calculator</h1>
    <p>Type your calculation after the root address you see in 
    your address bar in the form: '/operator/operand1/operand2'.<br>
    For example: '/multiply/3/4' will return the product of 3 and 4, 12.<br><br>
    The operator choices are: add, subtract, multiply, and divide.</p>"""


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': how_to,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')
    func = funcs[path[0]]
    args = path[1:]
    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get("PATH_INFO", None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>You can't divide by zero! Try again!</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(("Content-length", str(len(body))))
        start_response(status, headers)
        return [body.encode()]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
