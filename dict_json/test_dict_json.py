import random
import pytest
from dict_json import dict_json
import json
# import yaml

delimiter = dict_json.DELIMITER
# delimiter = '\0'
# dict_json.DELIMITER = delimiter

# from .conftest import logging
import logging
logging.basicConfig(level=logging.DEBUG)
from dict_json import dict_json

"""
Generator for json
Need to generate dict and list test data.
d(5)(1:l(4)(d(2))

l(0:3, d
d(4)

"""
def d(*arg, n=1):
    """ Create a test dictionary
    Number of fields in dictionary
    keys are k99, values are random
    :param n: Number of keys in test dict
    :return:
    """
    d = {}
    for x in range(n):
        d[f'k{x}'] = 'x' + ('s' * x) if len(arg) == 0 else arg[x % len(arg)].copy()
    return d

def l(*arg, n=1):
    """ Create test list
    Number of elements in list
    values are random

    :param n: Number of elements in test list
    :return:
    """
    if arg == ():
        element = lambda x: 'x' + ('s' * x)
    else:
        element = lambda x: arg[x % len(arg)].copy()
    ls = [None] * n
    for index in range(n):
        ls[index] = element(index)
    return ls

d01 = d(n=3)
d02 = d(n=3)

l01 = l(n=3)
l02 = l(n=3)

d01l = d(n=3)
d01l['d0'] = l01
d01l['d1'] = l02
d01l['d2'] = d02

d02 = d(l01, l01, d01, n=3)

l03 = l(d02, n=2)
l04 = l(l01, n=3)
l05 = l(l04, n=3)


j01s = '''
{
"a": 1,
"b":
    {
        "c": 3,
        "d": 4
    }
}
'''
j01Ks = ['a', 'b:c', 'b:d']

y01s = """
a: 1
b:
    c: 3
    d: 4
"""

j02s = '''
{
"a": 1,
"b":
    [
        {
            "c": 3,
            "d": 4
        },
        {
            "c": 5,
            "d": 6
        }
    ]
}
'''
j02Ks = ['a', 'b:0:c', 'b:0:d', 'b:1:c', 'b:1:d']

#
# @pytest.fixture
# def printKeys(request):
#     return request.config.getoption("--print")

class TestGetKeys(object):
    def testGetKeysD01(self, printKeys, debug):
        d01Ks = ['k0', 'k1', 'k2']
        d01K = dict_json.getKeys(d01)
        print(f'keys: {d01K}') # if printKeys else ''
        assert len(d01K) == len(d01Ks)
        assert d01K == d01Ks

    def testGetKeysD02(self, printKeys, debug):
        d02Ks = ['k0:0', 'k0:1', 'k0:2', 'k1:0', 'k1:1', 'k1:2', 'k2:k0', 'k2:k1', 'k2:k2']
        d02K = dict_json.getKeys(d02)
        print(f'keys: {d02K}') # if printKeys else ''
        assert len(d02K) == len(d02Ks)
        assert d02K == d02Ks

    def testGetKeysD02List(self, printKeys, debug):
        d02Ks = [['k0', '0'], ['k0', '1'], ['k0', '2'],
                 ['k1', '0'], ['k1', '1'], ['k1', '2'],
                 ['k2', 'k0'], ['k2', 'k1'], ['k2', 'k2']]
        d02K = dict_json.getKeys(d02, seralize=False)
        print(f'keys: {d02K}') # if printKeys else ''
        assert len(d02K) == len(d02Ks)
        assert d02K == d02Ks

    def testGetKeysL01(self, printKeys, debug):
        l01Ks = ['0', '1', '2']
        l01K = dict_json.getKeys(l01)
        print(f'keys: {l01K}') if printKeys else ''
        assert len(l01K) == len(l01Ks)
        assert l01K == l01Ks

    def testGetKeysL04(self, printKeys, debug):
        l04Ks = ['0:0','0:1','0:2', '1:0', '1:1', '1:2', '2:0', '2:1', '2:2']
        l04K = dict_json.getKeys(l04)
        print(f'keys: {l04K}') if printKeys else ''
        assert len(l04K) == len(l04Ks)
        assert l04K == l04Ks

    def testGetKeysL05(self, printKeys, debug):
        l05Ks = ['0:0:0', '0:0:1', '0:0:2', '0:1:0', '0:1:1', '0:1:2', '0:2:0', '0:2:1', '0:2:2',
                 '1:0:0', '1:0:1', '1:0:2', '1:1:0', '1:1:1', '1:1:2', '1:2:0', '1:2:1', '1:2:2',
                 '2:0:0', '2:0:1', '2:0:2', '2:1:0', '2:1:1', '2:1:2', '2:2:0', '2:2:1', '2:2:2',]
        l05K = dict_json.getKeys(l05)
        print(f'keys: {l05K}') if printKeys else ''
        assert len(l05K) == len(l05Ks)
        assert l05K == l05Ks

    def testGetKeysj01(self, printKeys, debug):
        j01 = json.loads(j01s)
        j01K = dict_json.getKeys(j01)
        print(f'keys: {j01K}') if printKeys else ''
        assert len(j01K) == len(j01Ks)
        assert j01K == j01Ks

    def testGetKeysj02(self, printKeys, debug):
        j02 = json.loads(j02s)
        j02K = dict_json.getKeys(j02)
        print(f'keys: {j02K}') if printKeys else ''
        assert len(j02K) == len(j02Ks)
        assert j02K == j02Ks


class TestGetValue(object):
    """
    Tests for getValue

    Simple dict
    Simple list
    Nested dict, dict
    Nested dict, list, dict
    Nested list, dict
    Nested list, list, dict

    Simple dict - missing key
    Simple list - missing index
    Nested dict, dict - missing second key
    Nested dict, list, dict - missing second index
    Nested list, dict - missing second key
    Nested list, list, dict - missing third key

    """
    def testDictSimpleExist(self): # Simple dict
        key = f'k1'
        fieldValue = dict_json.getValue(d01, key)
        assert fieldValue == d01[key]

    def testDictListExist(self): # Nested dict, list-str
        key = ['d1', '1']
        fieldValue = dict_json.getValue(d01l, dict_json.DELIMITER.join(key))
        assert fieldValue == d01l[key[0]][int(key[1])]

    def testDictListIntExist(self): # Nested dict, list-int
        key = ['d1', 1]
        fieldValue = dict_json.getValue(d01l, key)
        assert fieldValue == d01l[key[0]][key[1]]

    def testDictListIntL05Exist(self): # Nested dict, list-int
        key = ['1', 1, '0']
        fieldValue = dict_json.getValue(l05, key)
        assert fieldValue == l05[int(key[0])][int(key[1])][int(key[2])]

    def testJsonDictListExist(self): # Nested json dict, list, dict
        key = ['a']
        j02 = json.loads(j02s)
        fieldValue = dict_json.getValue(j02, dict_json.DELIMITER.join(key))
        assert fieldValue == j02[key[0]]

    def testJsonDictListExist2(self): # Nested json dict, list, dict
        key = ['b', '1']
        j02 = json.loads(j02s)
        fieldValue = dict_json.getValue(j02, dict_json.DELIMITER.join(key))
        assert fieldValue == j02[key[0]][int(key[1])]

    def testJsonDictListMissingList(self): # Nested json dict, list, dict
        key = ['a', '1']
        j02 = json.loads(j02s)
        with pytest.raises(TypeError):
            assert dict_json.getValue(j02, dict_json.DELIMITER.join(key))

    def testJsonDictListMissing2(self): # Nested json dict, list, dict
        key = ['b', '3']
        j02 = json.loads(j02s)
        with pytest.raises(IndexError):
            assert dict_json.getValue(j02, dict_json.DELIMITER.join(key))

    def testDictMissing(self): # Simple dict - missing key
        key = f'k1n'
        with pytest.raises(KeyError):
            assert dict_json.getValue(d01, key)


class TestAddValue(object):
    """
    Tests for addValue

    Using d02

    """
    def testD01KeyValueExists(self):
        key = 'k1l'
        newValue = 'yyy'
        dict_json.setValue(d01, key, newValue)
        fieldValue = dict_json.getValue(d01, key)
        assert fieldValue == newValue

    def testD01KeyValueMissing(self):
        key = 'k1n'
        newValue = 'yyy'
        dict_json.setValue(d01, key, newValue)
        fieldValue = dict_json.getValue(d01, key)
        assert fieldValue == newValue

    def testD02KeyValueExists(self):
        key = 'd1'
        newValue = 'yyy'
        dict_json.setValue(d02, key, newValue)
        fieldValue = dict_json.getValue(d02, key)
        assert fieldValue == newValue

    def testD02KeyValueMissing(self):
        key = 'd1l'
        newValue = 'yyy'
        dict_json.setValue(d02, key, newValue)
        fieldValue = dict_json.getValue(d02, key)
        assert fieldValue == newValue

    def testD02IndexIntValueMissing(self):
        key = ['k1', 1]
        newValue = 'yyy'
        dict_json.setValue(d02, key, newValue)
        fieldValue = dict_json.getValue(d02, key)
        assert fieldValue == newValue

    def testD02IndexStrValueMissing(self):
        # dict_json.DELIMITER = '\0'
        key = dict_json.DELIMITER.join(['k1', '5'])
        newValue = 'yyy'
        dict_json.setValue(d02, key, newValue)
        fieldValue = dict_json.getValue(d02, key)
        assert fieldValue == newValue

    def testL05IndexValueExist(self):
        key = dict_json.DELIMITER.join(['1', '1'])
        newValue = 'yyy'
        dict_json.setValue(l05, key, newValue)
        fieldValue = dict_json.getValue(l05, key)
        assert fieldValue == newValue

    def testL05IndexValueMissing(self):
        key = dict_json.DELIMITER.join(['1', '3'])
        newValue = 'yyy'
        dict_json.setValue(l05, key, newValue)
        fieldValue = dict_json.getValue(l05, key)
        assert fieldValue == newValue