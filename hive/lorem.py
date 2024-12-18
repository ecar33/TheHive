from faker import Faker

fake = Faker()

def get_random_name():
    return fake.name()

def get_random_body():
    return fake.paragraph()