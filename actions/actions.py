from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from my_parsers import *

choose_number = 'Выберите номер из списка ниже:\n'


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
            utter = ''
            for i in range(len(books)):
                utter += str(i + 1) + ' ' + books[i][:books[i].rfind(' - ')] + '\n'
        dispatcher.utter_message(text=choose_number + utter)
        return []


class ActionShowGenres(Action):
    def name(self) -> Text:
        return "action_show_genres"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        update_genres_and_subgenres()
        with open("cache/genres.txt", "r", encoding='utf-8') as f:
            genres = f.readlines()
            utter = ''
            for i in range(len(genres)):
                utter += str(i + 1) + ' ' + genres[i]
        dispatcher.utter_message(text=choose_number + utter)
        return []


class ActionShowSubgenres(Action):
    def name(self) -> Text:
        return "action_show_subgenres"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not tracker.get_slot("NUMBER"):
            dispatcher.utter_message(text='action_show_subgenres' + ' get None')
            return []
        choice = int(tracker.get_slot("NUMBER"))
        update_genres_and_subgenres()
        with open("cache/genres.txt", "r", encoding='utf-8') as f:
            genres = f.readlines()
            genre = genres[choice - 1][:-1]
        with open("cache/subgenres.txt", "r", encoding='utf-8') as f:
            subgenres = f.readlines()
            utter = ''
            counter = 1
            new_subgenres = ''
            for subgenre in subgenres:
                if subgenre[:subgenre.find(' - ')] == genre:
                    new_subgenres += subgenre
                    utter += str(counter) + ' ' + subgenre[subgenre.find(' - ') + 3:subgenre.rfind(' - ')] + '\n'
                    counter += 1
        with open("cache/subgenres.txt", "w", encoding='utf-8') as f:
            f.write(new_subgenres)
        dispatcher.utter_message(text=choose_number + utter)
        return []


class ActionShowBooksBySubgenre(Action):
    def name(self) -> Text:
        return "action_show_books_by_subgenre"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not tracker.get_slot("NUMBER"):
            dispatcher.utter_message(text='action_show_books_by_subgenre' + ' get None')
            return []
        choice = int(tracker.get_slot("NUMBER"))
        with open("cache/subgenres.txt", "r", encoding='utf-8') as f:
            subgenres = f.readlines()
            link = subgenres[choice - 1][subgenres[choice - 1].rfind(' - ') + 3:-1]
            parse_recommended_books(link)
        with open("cache/recommended_books.txt", "r", encoding='utf-8') as f:
            books = f.readlines()
            utter = ''
            for i in range(len(books)):
                utter += str(i + 1) + ' ' + books[i][:books[i].rfind(' - ')] + '\n'
        dispatcher.utter_message(text=choose_number + utter)
        return []


class ActionShowFoundBooks(Action):
    def name(self) -> Text:
        return "action_show_found_books"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not tracker.get_slot("ASK"):
            dispatcher.utter_message(text='action_show_found_books' + ' get None')
            return []
        ask = tracker.get_slot("ASK")
        question = ''
        for word in ask:
            question += word + ' '
        search(question)
        with open("cache/search_results.txt", "r", encoding='utf-8') as f:
            results = f.readlines()
        utter = ''
        counter = 1
        with open("cache/search_results.txt", "w", encoding='utf-8') as f:
            for line in results:
                if line[:line.find(' - ')] == 'book':
                    utter += str(counter) + ' ' + line[line.find(' - ') + 3: line.rfind(' - ')] + '\n'
                    f.write(line)
                    counter += 1
        dispatcher.utter_message(text=choose_number + utter)
        return []


class ActionShowFoundAuthors(Action):
    def name(self) -> Text:
        return "action_show_found_authors"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not tracker.get_slot("ASK"):
            dispatcher.utter_message(text='action_show_found_authors' + ' get None')
            return []
        ask = tracker.get_slot("ASK")
        question = ''
        for word in ask:
            question += word + ' '
        search(question)
        with open("cache/search_results.txt", "r", encoding='utf-8') as f:
            results = f.readlines()
        utter = ''
        counter = 1
        with open("cache/search_results.txt", "w", encoding='utf-8') as f:
            for line in results:
                if line[:line.find(' - ')] == 'author':
                    utter += str(counter) + ' ' + line[line.find(' - ') + 3: line.rfind(' - ')] + '\n'
                    f.write(line)
                    counter += 1
        dispatcher.utter_message(text=choose_number + utter)
        return []


class ActionShowBooksByAuthor(Action):
    def name(self) -> Text:
        return "action_show_books_by_author"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not tracker.get_slot("NUMBER"):
            dispatcher.utter_message(text='action_show_books_by_author' + ' get None')
            return []
        choice = int(tracker.get_slot("NUMBER"))
        with open("cache/search_results.txt", "r", encoding='utf-8') as f:
            results = f.readlines()
        link = results[choice - 1][results[choice - 1].rfind(' - ') + 3:-1]
        books_by_author(link)
        with open("cache/books_by_author.txt", "r", encoding='utf-8') as f:
            books = f.readlines()
        utter = ''
        for i in range(len(books)):
            utter += str(i + 1) + ' ' + books[i][:books[i].rfind(' - ')] + '\n'
        dispatcher.utter_message(text=choose_number + utter)
        return []


class ActionShowSelectedBook(Action):
    def name(self) -> Text:
        return "action_show_selected_book"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not (tracker.get_slot("NUMBER") and tracker.get_slot("TEMPLATE")):
            dispatcher.utter_message(text='action_show_selected_book' + ' get None')
            return []
        choice = int(tracker.get_slot("NUMBER"))
        template = tracker.get_slot("TEMPLATE")
        search_by = tracker.get_slot("SEARCH_BY")
        if template == 'жанр':
            with open("cache/recommended_books.txt", "r", encoding='utf-8') as f:
                books = f.readlines()
                url = books[choice - 1][books[choice - 1].rfind(' - ') + 3:-1]
        elif template == 'рекомендация':
            with open("cache/recommended_books.txt", "r", encoding='utf-8') as f:
                books = f.readlines()
                url = books[choice - 1][books[choice - 1].rfind(' - ') + 3:-1]
        else:
            if search_by == 'название':
                with open("cache/search_results.txt", "r", encoding='utf-8') as f:
                    books = f.readlines()
                    url = books[choice - 1][books[choice - 1].rfind(' - ') + 3:-1]
            else:
                with open("cache/books_by_author.txt", "r", encoding='utf-8') as f:
                    books = f.readlines()
                    url = books[choice - 1][books[choice - 1].rfind(' - ') + 3:-1]
        title, author, genres, rating, rating_count, times_read, description, img_link = book_info(url)
        utter = f'{title} - {author}\n'
        utter += 'Жанры: '
        utter += genres[0]
        for i in range(1, len(genres)):
            utter += ', ' + genres[i]
        utter += '\n'
        if rating_count != '':
            utter += 'Рейтинг: ' + rating + ' ' + rating_count + '\n'
        else:
            utter += 'Нет оценок\n'
        utter += 'Прочитано ' + times_read + '\n'
        if description != '':
            utter += 'Описание: ' + description
        dispatcher.utter_message(text=utter, image=img_link)
        return []


class ResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("TEMPLATE", None),
                SlotSet("ASK", None),
                SlotSet("NUMBER", None),
                SlotSet("SEARCH_BY", None)]

# - action_give_book
