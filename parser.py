import requests
from bs4 import BeautifulSoup as bs

base_url = "https://flibusta.club/"
response = requests.get(base_url + 'g/')
soup = bs(response.content, 'html.parser')
p_genre = soup.find('div', class_='p_genre')

with open("genres.txt", "w", encoding='utf-8') as f:
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


