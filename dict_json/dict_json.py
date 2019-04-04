"""
Dict with access to nested dict and list thru a single flat key
-----------------------------------------------------------------

Support to access values with one complex key
"""
import collections
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

"""


"""
DELIMITER = ':'

def getValue(json_dict_list, key):
    """
    Key contains individual dict and list keys separated by ":"
    Returns final value from complex key. None is returned when partial key is not found

    :param key: string of keys with ":" DELIMITER
    :return: value of final key
    """
    if isinstance(key, int):
        keys = [key]
    elif isinstance(key, str):
        keys = key.split(DELIMITER)
    else:
        keys = key
    my_dict = json_dict_list
    logger.debug(f'keys: {list(keys)}')
    for part_key in keys:
        logger.debug(f'\tpart_key: {part_key}')
        if isinstance(part_key, str):
            if part_key.isnumeric():
                part_key = int(part_key)
            elif part_key == '':
                return ''
        my_dict = my_dict[part_key]
    logger.debug(f'my_dict: {my_dict}')
    return my_dict

def setValue(json_dict_list, key, value):
    """
    Find last key in json_dict_list from key string
    Add [] for missing keys when next is int
    add MyDict() for missing keys when next is not int

    :param key: string of keys with ":" DELIMITER
    :param value: value for last key
    :return: None
    """
    if isinstance(key, int):
        keys = [key]
    elif isinstance(key, list):
        keys = key.copy()
    else:
        keys = key.split(DELIMITER)
    my_dict = json_dict_list
    prior_part_key = keys.pop(0)
    if isinstance(my_dict, list):
        prior_part_key = int(prior_part_key)
    logger.debug(f'keys: {list(keys)}, value: {value}')
    tabs = ''
    for part_key in keys:
        tabs += '\t'
        logger.debug(f'\tpart_key: {part_key}')
        if isinstance(prior_part_key, str):
            if prior_part_key not in my_dict or my_dict[prior_part_key] is None:
                # add [] or {} based on part_key isnumeric or letters
                my_dict[prior_part_key] = {part_key, None}
                logger.debug(f'{tabs}part_key: {part_key}, my_dict[prior_part_key]')
        else:
            if prior_part_key >= len(my_dict) or my_dict[prior_part_key] is None:
                # add [] or {} based on part_key isnumeric or letters
                part_key = int(part_key)
                my_dict[prior_part_key].append([None] * (part_key + 1 - len(my_dict)))
                logger.debug(f'{tabs}part_key: {part_key}, numeric')

        my_dict = my_dict[prior_part_key]
        prior_part_key = part_key if isinstance(my_dict, str) else int(part_key)
    if isinstance(my_dict, list):
        if prior_part_key >= len(my_dict): # or my_dict[prior_part_key] is None:
            # add [] or {} based on part_key isnumeric or letters
            part_key = int(part_key)
            my_dict += [None] * (part_key + 1 - len(my_dict))
            logger.debug(f'{tabs}part_key: {part_key}, numeric')
    logger.debug(f'prior_part_key: {prior_part_key}, value: {value}')
    my_dict[prior_part_key] = value
    return


def getKeys(json_dict_list, seralize=True):
    """
    get unique string of keys to values in response dict
    list use 0 for entry

    Add support to return keys as list

    :return: list of all key string to access elements
    """
    response = json_dict_list
    notDone = True
    if isinstance(response, dict):
        keys = iter(response.keys())
        logger.debug(f'dict keys: {response.keys()}')
    elif isinstance(response, list):
        keys = iter(range(len(response)))
        logger.debug(f'list keys: {list(range(len(response)))}')
    else:
        logger.debug(f'scalar keys: {response}')
        notDone = False
    jsonStack = collections.deque()
    fullKeys = []
    fullKey = []
    while notDone:
        tabs = '\t' * len(jsonStack)
        if isinstance(response, dict):
            key = next(keys, None)
        elif isinstance(response, list):
            key = next(keys, None)
        else:
            key = None
        logger.debug(f'\t{tabs}key: {key}')
        if key is None:
            if len(jsonStack) > 0:
                (response, fullKey, keys) = jsonStack.pop()
            else:
                notDone = False
        else:
            logger.debug(f'\t{tabs}\tresponse[key]: {response[key]}')
            if isinstance(response[key], (list, dict)):
                logger.debug(f'\t\t\t{tabs}list/dict')
                jsonStack.append((response, fullKey, keys))
                fullKey = fullKey.copy()
                response = response[key]
                key = key if isinstance(key, str) else str(key)
                fullKey.append(key)
                if isinstance(response, dict):
                    sortedKeys = sorted(response.keys())
                    keys = iter(sortedKeys)
                else:
                    response = [0] if len(response) == 0 else response
                    keys = iter(range(len(response)))
                    pass
            else:
                logger.debug(f'\t\t\t{tabs}value')
                if len(response) > 0 and isinstance(response[key], (dict, list)):
                    key = response[key]
                else:
                    key = key if isinstance(key, str) else str(key)
                    # if seralize:
                    #     fullKeys.append(DELIMITER.join(fullKey + [key]))
                    # else:
                    #     fullKeys.append(fullKey + [key])

                    fullKeys.append(DELIMITER.join(fullKey + [key]) if seralize else fullKey + [key])

                    key = None
        logger.debug(f'{tabs}*** last fullKey: {fullKeys[-1] if len(fullKeys) > 0 else  "start"}')
    return fullKeys
