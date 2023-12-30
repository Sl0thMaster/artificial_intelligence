import requests
from bs4 import BeautifulSoup as bs
import random

BOOKS_TO_SHOW = 7


def parse_recommended_books(url):
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    books = soup.find_all('div', class_='item')
    selected_book_numbers = []
    while len(selected_book_numbers) < BOOKS_TO_SHOW:
        book_number = random.randint(0, len(books) - 1)
        if book_number not in selected_book_numbers:
            selected_book_numbers.append(book_number)
    with open("cache/recommended_books.txt", "w", encoding='utf-8') as f:
        for i in range(len(books)):
            if i in selected_book_numbers:
                title = books[i].find('div', class_='name').contents[0].contents[0]
                link = books[i].find('div', class_='name').contents[0]['href']
                if not books[i].find('div', class_='author').contents[0].contents:
                    author = 'авторство не указано'
                else:
                    author = books[i].find('div', class_='author').contents[0].contents[0]
                f.write(f"{title} - {author} - {'https://flibusta.club' + link}\n")


def book_info(url):
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')

    title = soup.find('div', class_='b_biblio_book_top').find('div', class_='book_name').h1.contents[0]
    if soup.find('div', class_='b_biblio_book_annotation'):
        if soup.find('div', class_='b_biblio_book_annotation').find('p', class_='book'):
            description = soup.find('div', class_='b_biblio_book_annotation').find('p', class_='book').contents[0]
        elif soup.find('div', class_='b_biblio_book_annotation').find('p'):
            description = soup.find('div', class_='b_biblio_book_annotation').find('p').contents[0]
    else:
        description = ''

    if not soup.find('div', class_='row author'):
        author = 'авторство не указано'
    else:
        author = soup.find('div', class_='row author').find('a').contents[0]
    if not soup.find('div', class_='book_rating').find('span', class_='rating_count'):
        rating_count = ''
        rating = ''
    else:
        rating_count = soup.find('div', class_='book_rating').find('span', class_='rating_count').contents[0]
        rating = soup.find('div', class_='book_rating').find('meta', itemprop='ratingValue')['content']
    times_read = soup.find('div', class_='row views').find('span', class_="row_content").contents[0]
    row_genres = soup.find('div', class_='row genre').find('span', class_="row_content").contents
    genres = []
    for i in range(len(row_genres)):
        if i % 2 == 1:
            genres.append(row_genres[i].contents[0])
    link = soup.find('div', class_='book_img').find('img')['src']
    img_link = 'https://flibusta.club' + link
    return title, author, genres, rating, rating_count, times_read, description, img_link


def search(ask):
    url = 'https://flibusta.club/booksearch?ask=' + ask
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    books = soup.find('li').find_all('a', class_=lambda x: x != 'active')
    is_book = False
    is_title = False
    with open("cache/search_results.txt", "w", encoding='utf-8') as f:
        for book in books:
            if book['href'][1] != 's':
                if book['href'][1] == 'b':
                    is_book = is_title = True
                if is_book:
                    if is_title:
                        title = ''
                        for i in range(len(book.contents)):
                            if i == 1:
                                title += book.contents[i].contents[0]
                            else:
                                title += book.contents[i]
                        link = 'https://flibusta.club' + book['href']
                        f.write(f"book - {title} - ")
                    else:
                        if book.contents:
                            f.write(f"{book.contents[0]}")
                        else:
                            f.write('авторство не указано')
                        f.write(f' - {link}\n')
                    is_title = False
                else:
                    f.write(f"author - {book.contents[0]} - {'https://flibusta.club' + book['href']}\n")


def books_by_author(url):
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    books = soup.find_all('div', class_=lambda x: x in ['genre__name', 'book__line'])
    with open("cache/books_by_author.txt", "w", encoding='utf-8') as f:
        for book in books:
            if book['class'][0] == 'genre__name':
                genres = book.find_all('a', class_="genre_link")
                genre = ''
                for line in genres:
                    if line.contents:
                        genre += line.contents[0] + ' '
            else:
                title = book.find('a').contents[0]
                link = book.find('a')['href']
                f.write(f'{title} - {genre}- {"https://flibusta.club" + link}\n')


def update_genres_and_subgenres():
    base_url = "https://flibusta.club/"
    response = requests.get(base_url + 'g/')
    soup = bs(response.content, 'html.parser')
    p_genre = soup.find('div', class_='p_genre')
    with open("cache/subgenres.txt", "w", encoding='utf-8') as f:
        genres_count = 0
        genres = ''
        for line in p_genre:
            if genres_count % 2 == 0:
                genre = line.contents[0]
                genres += genre + '\n'
            else:
                subgenres = line.find_all('a')
                subgenres_count = 0
                for subgenre in subgenres:
                    if subgenres_count % 2 == 1:
                        name = subgenre.contents[0]
                        link = subgenre['href']
                        f.write(f"{genre} - {name} - {'https://flibusta.club' + link}\n")
                    subgenres_count += 1
            genres_count += 1
    with open("cache/genres.txt", "w", encoding='utf-8') as f:
        f.write(genres)


if __name__ == "__main__":
    update_genres_and_subgenres()
