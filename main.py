import bs4
import requests
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

base_url = 'https://habr.com/'
url = base_url + 'ru/all/'
headers = Headers().generate()


def connect_to_url(url, headers):
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    text = response.text
    return text


def scraping(text):
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    return articles


def get_preview_info(articles, keywords):
    for article in articles:
        results = article.find_all(class_='tm-article-body tm-article-snippet__lead')
        results = [result.text.lower().split(' ') for result in results]
        if set(*results) & set(KEYWORDS):
            date = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
            title = article.find('h2').find('span').text
            href = article.find(class_='tm-article-snippet__title-link').attrs['href']
            link = base_url + href[1:]
            print(f'{date} ====> {title} ====> {link}')


def get_article_info(articles, keywords):
    for article in articles:
        href = article.find(class_='tm-article-snippet__title-link').attrs['href']
        link = base_url + href[1:]
        articles_data = scraping(connect_to_url(link, headers))
        for data in articles_data:
            results = [x.text.lower().split(' ') for x in data.find_all(id='post-content-body')]
            if set(*results) & set(KEYWORDS):
                date = data.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
                title = data.find('h1').find('span').text
                print(f'{date} ====> {title} ====> {link}')


if __name__ == '__main__':
    articles = scraping(connect_to_url(url, headers))
    print('Совпадения по preview:')
    get_preview_info(articles, KEYWORDS)
    print()
    print('Совпадения по тексту статьи:')
    get_article_info(articles, KEYWORDS)