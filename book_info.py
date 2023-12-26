import requests
from bs4 import BeautifulSoup as bs


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
        author = ''
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