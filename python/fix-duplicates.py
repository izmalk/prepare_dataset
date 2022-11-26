import csv

input = 'data/ratings_lite3.csv'
# input = 'data/users_lite3.csv'
with open(input) as f:
    data = list(csv.reader(f))
    new_data = [a for i, a in enumerate(data) if a not in data[:i]]
    with open(input, 'w') as t:
        write = csv.writer(t)
        write.writerows(new_data)
