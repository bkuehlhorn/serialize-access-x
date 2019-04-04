dict_json
============
.. image:: https://img.shields.io/travis/bkuehlhorn/dict_json/master.svg
   :target: https://travis-ci.org/bkuehlhorn/dict_json
.. image:: https://img.shields.io/pypi/v/dict_json.svg
   :target: https://pypi.python.org/pypi/dict_json
.. image:: https://img.shields.io/pypi/l/dict_json.svg
   :target: https://pypi.python.org/pypi/dict_json

A flexible utility for accessing nested dict and list objects in Python with single searialized key.


Introduction
------------
This Python package provide functions to access nested dict and list objects.
Provides a dynamic access to entries. Normal access is with several ``[]`` for
nested value.
Entries are accessed by string of delimited keys/indexes or list of keys/indexes.

* ``getValue(json_dict_list, key)`` returns value
* ``addValue(json_dict_list, key, value)`` adds value to key entry, additional dict/list are created to access entry
* ``getKeys(json_dict_list, seralize)`` returns list of seralized keys for each value in dict/list. ``seralize``=True returns strings. False returns list

It also provides some key joining methods (reducer), and you can choose the reducer you want or even implement your own reducer. You can also choose to invert the resulting flat dict.

Documentation
-------------

Dict Json
```````

.. code-block:: python

   def getValue(json_dict_list, key):
       """
       Key contains individual dict and list keys separated by ":"
       Returns final value from complex key. None is returned when partial key is not found

       :param key: string of keys with ":" DELIMITER
       :return: value of final key
       """

.. code-block:: python

   def setValue(json_dict_list, key, value):
       """
       Find last key in json_dict_list from key string
       Add [] for missing keys when next is int
       add MyDict() for missing keys when next is not int

       :param key: string of keys with ":" DELIMITER
       :param value: value for last key
       :return: None
       """
.. code-block:: python

   def getKeys(json_dict_list, seralize=True):
       """
       get unique string of keys to values in response dict
       list use 0 for entry

       Add support to return keys as list

       :return: list of all key string to access elements
       """

Examples
::::::::

.. code-block:: python

   In [1]: from flatten_dict import flatten

   In [2]: normal_dict = {
      ...:     'a': '0',
      ...:     'b': {
      ...:         'a': '1.0',
      ...:         'b': '1.1',
      ...:     },
      ...:     'c': {
      ...:         'a': '2.0',
      ...:         'b': {
      ...:             'a': '2.1.0',
      ...:             'b': '2.1.1',
      ...:         },
      ...:     },
      ...: }

   In [3]: flatten(normal_dict)
   Out[3]:
   {('a',): '0',
    ('b', 'a'): '1.0',
    ('b', 'b'): '1.1',
    ('c', 'a'): '2.0',
    ('c', 'b', 'a'): '2.1.0',
    ('c', 'b', 'b'): '2.1.1'}

   In [4]: flatten(normal_dict, reducer='path')
   Out[4]:
   {'a': '0',
    'b/a': '1.0',
    'b/b': '1.1',
    'c/a': '2.0',
    'c/b/a': '2.1.0',
    'c/b/b': '2.1.1'}

   In [5]: flatten(normal_dict, reducer='path', inverse=True)
   Out[5]:
   {'0': 'a',
    '1.0': 'b/a',
    '1.1': 'b/b',
    '2.0': 'c/a',
    '2.1.0': 'c/b/a',
    '2.1.1': 'c/b/b'}

   In [6]: def underscore_reducer(k1, k2):
      ...:     if k1 is None:
      ...:         return k2
      ...:     else:
      ...:         return k1 + "_" + k2
      ...:

   In [7]: flatten(normal_dict, reducer=underscore_reducer)
   Out[7]:
   {'a': '0',
    'b_a': '1.0',
    'b_b': '1.1',
    'c_a': '2.0',
    'c_b_a': '2.1.0',
    'c_b_b': '2.1.1'}

Unflatten
`````````

.. code-block:: python

   def unflatten(d, splitter='tuple', inverse=False):
       """Unflatten dict-like object.

       Parameters
       ----------
       d: dict-like object
           The dict that will be unflattened.
       splitter: {'tuple', 'path', function} (default: 'tuple')
           The key splitting method. If a function is given, the function will be
           used to split.
           'tuple': Use each element in the tuple key as the key of the unflattened dict.
           'path': Use ``pathlib.Path.parts`` to split keys.
       inverse: bool (default: False)
           Whether you want to invert the key and value before flattening.

       Returns
       -------
       unflattened_dict: dict
       """

Examples
::::::::

.. code-block:: python

   In [1]: from flatten_dict import unflatten

   In [2]: flat_dict = {
      ...:     ('a',): '0',
      ...:     ('b', 'a'): '1.0',
      ...:     ('b', 'b'): '1.1',
      ...:     ('c', 'a'): '2.0',
      ...:     ('c', 'b', 'a'): '2.1.0',
      ...:     ('c', 'b', 'b'): '2.1.1',
      ...: }

   In [3]: unflatten(flat_dict)
   Out[3]:
   {'a': '0',
    'b': {'a': '1.0', 'b': '1.1'},
    'c': {'a': '2.0', 'b': {'a': '2.1.0', 'b': '2.1.1'}}}

   In [4]: flat_dict = {
      ...:     'a': '0',
      ...:     'b/a': '1.0',
      ...:     'b/b': '1.1',
      ...:     'c/a': '2.0',
      ...:     'c/b/a': '2.1.0',
      ...:     'c/b/b': '2.1.1',
      ...: }

   In [5]: unflatten(flat_dict, splitter='path')
   Out[5]:
   {'a': '0',
    'b': {'a': '1.0', 'b': '1.1'},
    'c': {'a': '2.0', 'b': {'a': '2.1.0', 'b': '2.1.1'}}}

   In [6]: flat_dict = {
      ...:     '0': 'a',
      ...:     '1.0': 'b/a',
      ...:     '1.1': 'b/b',
      ...:     '2.0': 'c/a',
      ...:     '2.1.0': 'c/b/a',
      ...:     '2.1.1': 'c/b/b',
      ...: }

   In [7]: unflatten(flat_dict, splitter='path', inverse=True)
   Out[7]:
   {'a': '0',
    'b': {'a': '1.0', 'b': '1.1'},
    'c': {'a': '2.0', 'b': {'a': '2.1.0', 'b': '2.1.1'}}}

   In [8]: def underscore_splitter(flat_key):
      ...:     return flat_key.split("_")
      ...:

   In [9]: flat_dict = {
      ...:     'a': '0',
      ...:     'b_a': '1.0',
      ...:     'b_b': '1.1',
      ...:     'c_a': '2.0',
      ...:     'c_b_a': '2.1.0',
      ...:     'c_b_b': '2.1.1',
      ...: }

   In [10]: unflatten(flat_dict, splitter=underscore_splitter)
   Out[10]:
   {'a': '0',
    'b': {'a': '1.0', 'b': '1.1'},
    'c': {'a': '2.0', 'b': {'a': '2.1.0', 'b': '2.1.1'}}}
