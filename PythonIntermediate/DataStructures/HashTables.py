import string
def combine_dictionaries(dict1, dict2, dict3):
    new_dict = {}
    for i in dict1:
        new_dict[i] = dict1[i]
    for i in dict2:
        new_dict[i] = dict2[i]
    for i in dict3:
        new_dict[i] = dict3[i]
    return new_dict


def combine_update(dict1, dict2, dict3):
    temp = dict1.copy()
    temp.update(dict2)
    temp.update(dict3)
    return temp


def combine(dict1, dict2, dict3):
    # ** is called dictionary unpacking operator
    return {**dict1, **dict2, **dict3}


def key_exists(key, dict):
    return key in dict


def alphabet():
    temp = {}
    for i in range(1, 27):
        temp[chr(96+i)] = i
    return temp


def alphabet2():
    return dict(zip(string.ascii_lowercase, range(1, 27)))


a = {'name': 'Sara', 'age': 24, 'job': 'teacher'}
b = {'name1': 'James', 'age1': 12, 'job1': 'teacher'}
c = {'name2': 'Nina', 'age2': 51, 'job2': 'teacher'}

print(combine_dictionaries(a, b, c))
print(combine_update(a, b, c))
print(combine(a, b, c))
print(key_exists('name1', a))
print(alphabet())
print(alphabet2())
