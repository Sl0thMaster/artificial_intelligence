from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random
from my_parsers import *

BOOKS_TO_SHOW = 7


class ActionShowPopularBooks(Action):
    def name(self) -> Text:
        return "action_show_popular_books"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = 'https://flibusta.club/b/'
        parse_recommended_books(url)
        with open("cache/recommended_books.txt", "r", encoding='utf-8') as f:
            books = f.readlines()
            selected_book_numbers = []
            while len(selected_book_numbers) < 7:
                book_number = random.randint(0, len(books) - 1)
                if not book_number in selected_book_numbers:
                    selected_book_numbers.append(book_number)
            utter = ''
            new_books = ''
            count = 1
            for i in range(len(books)):
                if i in selected_book_numbers:
                    new_books += books[i]
                    utter += str(count) + ' ' + books[i][:books[i].rfind(' - ')] + '\n'
                    count += 1
        with open("cache/recommended_books.txt", "w", encoding='utf-8') as f:
            f.write(new_books)
        dispatcher.utter_message(text=utter)
        return []


# - action_show_genres
# - action_show_books_by_genre
# - action_show_search
# - action_show_found_books
# - action_show_found_authors
# - action_show_selected_book
# - action_give_book
