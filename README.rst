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
Examples
::::::::

.. code-block:: python

   In [1]: from dict-json import getValue

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

   In [3]: getValue(normal_dict, 'a')
   Out[3]:


   In [4]: getValue(normal_dict, 'b:a')
   Out[4]:

   In [5]: getValue(normal_dict, 'c:b:b')
   Out[5]:

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
Examples
::::::::

.. code-block:: python

   In [1]: from dict-json import setValue

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

   In [3]: setValue(normal_dict, 'a', 'newvalue')
   Out[3]:
   In [3]: getValue(normal_dict, 'a')
   Out[3]:


   In [4]: setValue(normal_dict, 'b:a', 'newvalue')
   Out[4]:
   In [4]: getValue(normal_dict, 'b:a')
   Out[4]:

   In [5]: setValue(normal_dict, 'c:c:b', 'newvalue newnode')
   Out[5]:
   In [5]: getValue(normal_dict, 'c:c:b')
   Out[5]:

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

   In [1]: from flatten_dict import getKeys

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

   In [3]: getKeys(normal_dict)
   Out[3]:


   In [3]: getKeys(normal_dict, 'list')
   Out[4]:
