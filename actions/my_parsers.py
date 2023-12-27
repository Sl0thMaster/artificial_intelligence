import requests
from bs4 import BeautifulSoup as bs


def parse_recommended_books(url):
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    book_list = soup.find_all('div', class_='item')
    with open("cache/recommended_books.txt", "w", encoding='utf-8') as f:
        for book in book_list:
            title = book.find('div', class_='name').contents[0].contents[0]
            link = book.find('div', class_='name').contents[0]['href']
            if not book.find('div', class_='author').contents[0].contents:
                author = 'авторство не указано'
            else:
                author = book.find('div', class_='author').contents[0].contents[0]
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
    return title, author, genres, rating, rating_count, times_read, description


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
                        f.write(f"book - {book.contents[0]} - {'https://flibusta.club' + book['href']} - ")
                    else:
                        if book.contents:
                            f.write(f"{book.contents[0]}\n")
                        else:
                            f.write('\n')
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
                    genre += line.contents[0] + ' '
            else:
                title = book.find('a').contents[0]
                link = book.find('a')['href']
                f.write(f'{genre}- {title} - {"https://flibusta.club" + link}\n')


if __name__ == "__main__":
    base_url = "https://flibusta.club/"
    response = requests.get(base_url + 'g/')
    soup = bs(response.content, 'html.parser')
    p_genre = soup.find('div', class_='p_genre')

    with open("cache/genres.txt", "w", encoding='utf-8') as f:
        genres_count = 0
        for line in p_genre:
            if genres_count % 2 == 0:
                genre = line.contents[0]
            else:
                subgenres = line.find_all('a')
                subgenres_count = 0
                for subgenre in subgenres:
                    if subgenres_count % 2 == 1:
                        name = subgenre.contents[0]
                        link = subgenre['href']
                        f.write(f"{genre} - {name} - {base_url + link}\n")
                    subgenres_count += 1
            genres_count += 1


# parse_recommended_books(url)
#
# with open("recommended_books.txt", "r", encoding='utf-8') as f:
#     books = f.readlines()
#     for book in books:
#         url = book[book.rfind(' - ') + 3:-1]
#         title, author, genres, rating, rating_count, times_read, description = book_info(url)
#         print(f'title: {title}, author: {author}\ngenres: {genres}\nrating: {rating}, '
#               f'rating_count: {rating_count}, times_read: {times_read}\ndescription: {description}')