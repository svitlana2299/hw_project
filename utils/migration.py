from quotes.models import Quote, Tag, Author
from pymongo import MongoClient
import os
import django
import sys
# Додаємо батьківську папку до sys.path
sys.path.append("E:\python_go_it\web\HW_10_web")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")

django.setup()


# Решта вашого коду

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")

django.setup()

client = MongoClient("mongodb://localhost")
db = client.hw

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
    )


quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))

    if not exist_quote:
        author = db.authors.find_one({'_id': quote['author']})
        a = Author.objects.get(fullname=author['fullname'])
        q = Quote.objects.create(
            quote=quote['quote'],
            author=a
        )
        for tag in tags:
            q.tags.add(tag)
