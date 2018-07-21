![wildfire logo](logo.png)

# Wildfire

[![Build Status](https://travis-ci.org/floscha/wildfire.svg?branch=master)](https://travis-ci.org/floscha/wildfire)
[![Coverage Status](https://coveralls.io/repos/github/floscha/wildfire/badge.svg?branch=master)](https://coveralls.io/github/floscha/wildfire?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ebf01a8a4dc343218f3c467bffb32721)](https://www.codacy.com/app/floscha/wildfire?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=floscha/wildfire&amp;utm_campaign=Badge_Grade)
[![PyPI Version](https://img.shields.io/pypi/v/wildfire.svg)](https://pypi.python.org/pypi/wildfire)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

*Wildfire is a library to automatically generate HTTP services for arbitrary Python classes, inspired by Google's [Python Fire](https://opensource.google.com/projects/python-fire) which generates command line applications instead.*


## Installation

To install Wildfire with pip, run `pip install wildfire`

To install Wildfire from source, first clone the repository and then run `python setup.py install`


## Basic Usage

Right now, Wildfire only works properly on classes.
Other Python objects like functions, modules, objects, dictionaries, lists, tuples, etc. are planned to be supported in the future.

Here's an example of calling Wildfire on a class.

```python
# service.py
import wildfire

class Calculator(object):
  """A simple calculator class."""

  def double(self, number):
    return 2 * number

api = wildfire.Wildfire(Calculator)
```
(We use the [example](https://github.com/google/python-fire#basic-usage) from Python Fire to show the similarity of both APIs.)

Run the server script using [Gunicorn](http://gunicorn.org/):
```bash
$ gunicorn service:api
```

Then, from the command line, you can query the web service like so:

```bash
$ curl -d '{"number": 5}' -H "Content-Type: application/json" -X POST http://localhost:5000/double
10
```
