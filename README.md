![wildfire logo](logo.png)

# Wildfire

[![PyPI Version](https://img.shields.io/pypi/v/wildfire.svg)](https://pypi.python.org/pypi/wildfire)
[![Build Status](https://travis-ci.org/floscha/wildfire.svg?branch=master)](https://travis-ci.org/floscha/wildfire)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

*Wildfire is a library to automatically generate HTTP services for arbitrary Python classes, inspired by Google's [Python Fire](https://opensource.google.com/projects/python-fire) which generates command line applications instead.*

## Installation

For now, it is only possible to install Wildfire from source.
1. Clone the repository
1. Run `pip install .`


## Basic Usage

Right now, Wildfire only works properly on classes.
Other Python objects like functions, modules, objects, dictionaries, lists, tuples, etc. are planned to be supported in the future.

Here's an example of calling Wildfire on a class.

```python
import wildfire

class Calculator(object):
  """A simple calculator class."""

  def double(self, number):
    return 2 * number

if __name__ == '__main__':
  wildfire.Wildfire(Calculator)
```
(We use the [example](https://github.com/google/python-fire#basic-usage) from Python Fire to show the similarity of both APIs.)

Then, from the command line, you can query the web service like so:

```bash
$ curl -d '{"number": 5}' -H "Content-Type: application/json" -X POST http://localhost:5000/double
10
```
