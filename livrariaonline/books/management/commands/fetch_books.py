# books/management/commands/fetch_books.py

import requests
from django.core.management.base import BaseCommand
from livrariaonline.books.models import Book
from datetime import datetime

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        url = 'https://openlibrary.org/people/mekBot/books/want-to-read.json'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            books_data = data.get('reading_log_entries', [])

            for entry in books_data:
                book_data = entry['work']
                title = book_data.get('title')
                author = ', '.join(book_data.get('author_names', []))
                first_publish_year = book_data.get('first_publish_year')
                cover_id = book_data.get('cover_id')
                open_library_id = book_data.get('key')
                logged_date_str = entry.get('logged_date')

                try:
                    logged_date = datetime.strptime(logged_date_str, "%Y/%m/%d, %H:%M:%S")
                except ValueError:
                    logged_date = None

                book, created = Book.objects.update_or_create(
                    open_library_id=open_library_id,
                    defaults={
                        'title': title,
                        'author': author,
                        'first_publish_year': first_publish_year,
                        'cover_id': cover_id,
                        'logged_date': logged_date
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Book "{title}" added to the database.'))
                else:
                    self.stdout.write(f'Book "{title}" updated.')
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data from the API.'))
