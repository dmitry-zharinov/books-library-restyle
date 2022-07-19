import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

BOOKS_FOLDER = 'books'
IMG_FOLDER = 'images'
PAGES_FOLDER = 'pages'


def init_template():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html'])
    )
    return env.get_template('template.html')


def load_books_from_json():
    with open("books.json", "r", encoding='utf8') as my_file:
        books_json = my_file.read()
        return list(chunked(json.loads(books_json), 2))


def run_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def on_reload():
    BOOKS_ON_PAGE = 10
    book_items = load_books_from_json()
    template = init_template()
    chunked_books = list(chunked(book_items, BOOKS_ON_PAGE))

    for page_num, books in enumerate(chunked_books):
        rendered_page = template.render(
            books=books,
            books_folder=BOOKS_FOLDER,
            img_folder=IMG_FOLDER,
        )
        index_filepath = os.path.join(PAGES_FOLDER, f'index{page_num}.html')

        with open(index_filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    Path(PAGES_FOLDER).mkdir(parents=True, exist_ok=True)
    server = Server()
    on_reload()
    server.watch('templates/*.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
