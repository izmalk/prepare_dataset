import csv

n = 1
y = 1
print('Creating new file')
ratings_file = open("data/ratings_lite2.csv", "w", newline='', encoding='latin-1')
fieldnames = ['User-ID', 'ISBN', 'Book-Rating']
writer = csv.DictWriter(ratings_file, fieldnames=fieldnames)
writer.writeheader()
print('Opening user short list')
with open("data/users_lite2.csv", encoding='latin-1') as data:  # 1
    for row in csv.DictReader(data, delimiter=",", skipinitialspace=True):
        item = {key: value for key, value in row.items()}  # fieldnames (keys) are taken from the first row
        print('Opening rating list')
        with open("data/ratings_lite.csv", encoding='latin-1') as old:  # 1
            for row_old in csv.DictReader(old, delimiter=",", skipinitialspace=True):
                row_old_item = {key: value for key, value in row_old.items()}
                # print(row_old_item)
                if item['User-ID'] == row_old_item['User-ID']:
                    print(n, item, y, row_old_item)
                    n += 1
                    writer.writerow(row_old_item)
                y += 1
ratings_file.close()
print('Users parsing ended')
