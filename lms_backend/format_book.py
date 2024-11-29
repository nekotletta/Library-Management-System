import json

# Read data from the 'bookinfo.txt' file
with open('bookinfo.txt', 'r') as file:
    data = file.readlines()

books = []
for line in data:
    line = line.split(',')
    book = {
        "model": "yourapp.book",
        "pk": line[0],
        "fields": {
            "title": line[3],
            "release_date": line[4],
            "author_id": line[1],
            "genre_id": line[2],
            "isbn": line[5],
            "copies_available": line[6],
            "description": line[7]
        }
    }
    books.append(book)

# Write the formatted data to a JSON file
with open('books.json', 'w') as f:
    json.dump(books, f, indent=2)