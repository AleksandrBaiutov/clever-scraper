import json
import time

import logging

from flask import request, render_template

import create_app, database
from models import Books

app = create_app.create_app()
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET'])
def fetch():
    age = request.args.get('ageInput')
    availability = request.args.get('availabilityCheckbox')
    sort_type = request.args.get('sortType')
    books = database.get_all_filtered(Books, age, availability, sort_type)
    all_books = []
    for book in books:
        new_book = {
            "ISBN": book.ISBN,
            "name": book.name,
            "price": book.price,
            "discount": book.discount,
            "author": book.author,
            "min_age": book.min_age,
            "rating": book.rating,
            "review_number": book.review_number,
            "available": book.available,
            "link": book.link
        }

        all_books.append(new_book)
    return render_template("base.html", books=all_books), 200
if __name__ == '__main__':
       app.run(host='0.0.0.0', port=30006, debug=True)


