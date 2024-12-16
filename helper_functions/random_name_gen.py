import random
from pyjokes import get_joke

def get_random_name():
    first_names = ['Adam', 'Nick', 'John', 'Sandy', 'Mary', 'Joe', 'Stan']
    last_names = ['Smith', 'Johnson', 'Masters', 'Lake', 'Taylor']
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    return name

def get_random_content():
    return get_joke("en", "all")