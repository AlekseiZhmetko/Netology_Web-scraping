import requests
import bs4
from fake_headers import Headers
import time
import string

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'гаджеты', 'сообщества', 'elena_pastukhova']

headers = Headers(os='win', headers=True).generate()

url = 'https://habr.com'
target_url = '/ru/all/'

response = requests.get(url+target_url, headers=headers)
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')

for article in articles:
    snippets = article.find_all(class_='tm-article-snippet')
    for snippet in snippets:
        words_list = snippet.text.strip().lower().translate(str.maketrans('', '', string.punctuation)).split()
        if any(set(words_list).intersection(set(KEYWORDS))) is True:
            article_datetime = article.find(class_='tm-article-snippet__datetime-published').time['datetime']
            ts = time.strptime(article_datetime[:10], "%Y-%m-%d")
            article_date = time.strftime("%d/%m/%Y", ts)
            title = article.find('h2').find('span').text
            href = article.find(class_='tm-article-snippet__title-link').attrs['href']
            link = url+href
            print(article_date, '-', title, '-', link)
