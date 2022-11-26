import csv, uuid, random
from typedb.client import TypeDB, SessionType, TransactionType

random.Random()

def parse_data_to_dictionaries(input):
    """
      1. reads the file through a stream,
      2. adds the dictionary to the list of items
      :param input.file as string: the path to the data file, minus the format
      :returns items as list of dictionaries: each item representing a data item from the file at input.file
    """
    print('parsing started')
    items = []

    with open(input["file"] + ".csv", encoding='latin-1') as data:  # 1
        for row in csv.DictReader(data, delimiter=";", skipinitialspace=True):
            # row = [d.replace('"', '').replace("\'", '') for d in row]
            item = {key: value for key, value in row.items()}  # fieldnames (keys) are taken from the first row
            items.append(item)  # 2
    print('parsing ended')
    return items


def load_data_into_typedb(input, session):
    """
      loads the csv data into our TypeDB phone_calls database:
      1. gets the data items as a list of dictionaries
      2. for each item dictionary
        a. creates a TypeDB transaction
        b. constructs the corresponding TypeQL insert query
        c. runs the query
        d. commits the transaction
      :param input as dictionary: contains details required to parse the data
      :param session: off of which a transaction will be created
    """
    items = parse_data_to_dictionaries(input)  # 1
    x = 1
    for item in items:  # 2
        print(x)
        x += 1
        print(item)
        with session.transaction(TransactionType.WRITE) as transaction:  # a
            TypeQL_insert_query = input["template"](item)  # b
            print("Executing TypeQL Query: " + TypeQL_insert_query)
            transaction.query().insert(TypeQL_insert_query)  # c
            transaction.commit()  # d

    print("\nInserted " + str(len(items)) +
          " items from [ " + input["file"] + ".csv] into TypeDB.\n")


def books_template(book):
    return 'insert $b isa Book, has id "' + str(uuid.uuid4()) + '", has ISBN "' + book["ISBN"] + '", has name "' + book["Book-Title"] + '", has Book_Author "' \
           + book["Book-Author"] + '", has Publisher "' + book["Publisher"] + '", has price ' + str(random.randint(3, 100)) \
           + ', has stock ' + str(random.randint(0, 25)) + ';'

'''
def users_template(person):
    # insert person
    TypeQL_insert_query = 'insert $person isa person, has phone-number "' + \
                         person["phone_number"] + '"'
    if person["first_name"] != "":
        TypeQL_insert_query += ', has first-name "' + person["first_name"] + '"'
        TypeQL_insert_query += ', has last-name "' + person["last_name"] + '"'
        TypeQL_insert_query += ', has city "' + person["city"] + '"'
        TypeQL_insert_query += ", has age " + str(person["age"])
    TypeQL_insert_query += ";"
    return TypeQL_insert_query


def ratings_template(contract):
    # match company
    TypeQL_insert_query = 'match $company isa company, has name "' + \
                         contract["company_name"] + '";'
    # match person
    TypeQL_insert_query += ' $customer isa person, has phone-number "' + \
                          contract["person_id"] + '";'
    # insert contract
    TypeQL_insert_query += " insert (provider: $company, customer: $customer) isa contract;"
    return TypeQL_insert_query
'''

Inputs = [
    {
        "file": "books_lite",
        "template": books_template
    },

    '''
    ,
    {
        "file": "users",
        "template": users_template
    },
    {
        "file": "ratings",
        "template": ratings_template
    }
    '''
]

data_path = "data/"

with TypeDB.core_client("localhost:1729") as client:  # 1
    with client.session("test2", SessionType.DATA) as session:  # 2
        for input in Inputs:
            input["file"] = data_path + input["file"]  # 3a
            print("Loading from [" + input["file"] + ".csv] into TypeDB ...")
            load_data_into_typedb(input, session)  # 3b



