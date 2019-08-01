.. FlatDict documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dict_json
=========
|Version| |Status| |Coverage|

**dict_json** is a Python library for interacting with nested dicts and lists as a single
level dict or list with delimited keys. FlatDict supports Python 3.6+.

Jump to :ref:`installation`, :ref:`example`, :ref:`docs`, or :ref:`license`.

*For example:*

.. code-block:: python

    foo = {'foo': {'bar': 'baz', 'qux': 'corge'}}

*is represented as:*

.. code-block:: python

    {'foo:bar': 'baz',
     'foo:qux': 'corge'}

*And can still be accessed as:*

.. code-block:: python

    foo['foo']['bar']

*and*

.. code-block:: python

    foo['foo:bar']

Additionally, lists and tuples are also converted into dicts using enumerate().

*For example:*

.. code-block:: python

    d = {'list': ['a', 'b', 'c',]}

*Will be flattened as follows:*

.. code-block:: python

    flat = {'list:0': 'a', 'list:1': 'b', 'list:2': 'c'}

.. _installation:

Installation
------------

.. code-block:: bash

    $ pip install flatdict

.. _example:

Example Use
-----------

.. code-block:: python

    import pprint

    import dict_json

    values = {'foo': {'bar': {'baz': 0,
                              'qux': 1,
                              'corge': 2},
                      'grault': {'baz': 3,
                                 'qux': 4,
                                 'corge': 5}},
              'garply': {'foo': 0, 'bar': 1, 'baz': 2, 'qux': {'corge': 3}}}

    print(dict_json.getValue(values, 'foo:bar:baz'))

    dict_json.setValue(values, ('test:value:key', 10)

    pprint.pprint(values.as_dict())

    pprint.pprint(dict(values))

.. _docs:

Class Documentation
-------------------

.. automodule:: dict_json
    :members:
    :undoc-members:
    :inherited-members:

.. |Version| image:: https://img.shields.io/pypi/v/dict_json.svg?
   :target: http://badge.fury.io/py/dict_json

.. |Status| image:: https://img.shields.io/travis/gmr/dict_json.svg?
   :target: https://travis-ci.org/gmr/dict_json

.. |Coverage| image:: https://img.shields.io/codecov/c/github/gmr/dict_json.svg?
   :target: https://codecov.io/github/gmr/dict_json?branch=master
