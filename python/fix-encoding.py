import csv

input_file = 'data/ratings_lite2.csv'
# input_file = 'data/users_lite2.csv'
print('Creating new file')
fix_file = open("data/ratings_lite3.csv", "w", newline='', encoding='UTF-8')
# fix_file = open("data/users_lite3.csv", "w", newline='', encoding='UTF-8')
fieldnames = ['User-ID', 'ISBN', 'Book-Rating'] # review header
# fieldnames = ['User-ID', 'Location', 'Age'] # users header
writer = csv.DictWriter(fix_file, fieldnames=fieldnames, delimiter=';')
writer.writeheader()

with open(input_file, encoding='latin-1') as data:  # 1
    for row in csv.DictReader(data, delimiter=",", skipinitialspace=True):
        item = {key: value for key, value in row.items()}
        writer.writerow(item)
        print(item)
