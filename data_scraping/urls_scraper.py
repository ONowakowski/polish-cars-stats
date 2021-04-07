from bs4 import BeautifulSoup
from requests import get
import pandas as pd

URL = 'https://www.otomoto.pl/osobowe/?search%5Border%5D=created_at%3Adesc&page='

def get_urls_from_page(page_number, df):
    url_page = f'{URL}{page_number}'
    page = get(url_page)
    bs = BeautifulSoup(page.content, 'html.parser')

    print(f'Working on page {page_number}')

    for offer in bs.find_all('a', class_='offer-title__link'):
        offer_title = offer.get_text().strip()
        offer_url = offer.get('href')
        df = df.append({'title':offer_title, 'url':offer_url}, ignore_index=True)

    return df

def get_urls_from_page_range(first_page, last_page):
    df_urls = pd.DataFrame(columns=['title', 'url'])
    for page in range(first_page, last_page+1):
        df_urls = get_urls_from_page(page, df_urls)

    return df_urls

df = get_urls_from_page_range(1, 500)
df.to_csv('otomoto_urls.csv')