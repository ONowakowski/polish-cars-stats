from bs4 import BeautifulSoup
from requests import get
import pandas as pd

df_urls = pd.read_csv('otomoto_urls.csv')


def get_price(bs_page_content):
    price = bs_page_content.find('span', class_='offer-price__number').get_text()
    return price.replace('        ', ' ').strip()


def get_offer_date(bs_page_content):
    date = bs_page_content.find('span', class_='offer-meta__value').get_text()
    return date


def get_offer_id(bs_page_content):
    id = bs_page_content.find_all('span', class_='offer-meta__value')[1].get_text()
    return id


def get_car_make(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Marka" in li.get_text():
                correct_li = li

    make = None
    if (correct_li != None):
        make = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return make


def get_car_model(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Model" in li.get_text():
                correct_li = li

    model = None
    if (correct_li != None):
        model = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return model


def get_prod_year(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Rok produkcji" in li.get_text():
                correct_li = li

    year = None
    if (correct_li != None):
        year = correct_li.find('div', class_='offer-params__value').get_text().strip()

    return year


def get_car_version(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Wersja" in li.get_text():
                correct_li = li

    version = None
    if (correct_li != None):
        version = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return version


def get_car_generation(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Generacja" in li.get_text():
                correct_li = li

    generation = None
    if (correct_li != None):
        generation = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return generation


def get_eng_power(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Moc" in li.get_text():
                correct_li = li

    power = None
    if (correct_li != None):
        power = correct_li.find('div', class_='offer-params__value').get_text().strip()

    return power


def get_eng_capacity(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "skokowa" in li.get_text():
                correct_li = li

    capacity = None
    if (correct_li != None):
        capacity = correct_li.find('div', class_='offer-params__value').get_text().strip()

    return capacity


def get_fuel_type(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Rodzaj paliwa" in li.get_text():
                correct_li = li

    fuel_type = None
    if (correct_li != None):
        fuel_type = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return fuel_type


def get_mileage(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Przebieg" in li.get_text():
                correct_li = li

    mileage = None
    if (correct_li != None):
        mileage = correct_li.find('div', class_='offer-params__value').get_text().strip()

    return mileage


def get_country_of_origin(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Kraj pochodzenia" in li.get_text():
                correct_li = li

    country = None
    if (correct_li != None):
        country = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return country


def get_gearbox_type(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Skrzynia biegów" in li.get_text():
                correct_li = li

    gearbox = None
    if (correct_li != None):
        gearbox = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return gearbox


def get_condition(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Stan" in li.get_text():
                correct_li = li

    condition = None
    if (correct_li != None):
        condition = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return condition


def get_color(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Kolor" in li.get_text():
                correct_li = li

    color = None
    if (correct_li != None):
        color = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return color


def get_body_type(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Typ" in li.get_text():
                correct_li = li

    body = None
    if (correct_li != None):
        body = correct_li.find('a', class_='offer-params__link').get_text().strip()

    return body


def get_doors(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Liczba drzwi" in li.get_text():
                correct_li = li

    doors = None
    if (correct_li != None):
        doors = correct_li.find('div', class_='offer-params__value').get_text().strip()

    return doors


def get_seats(bs_page_content):
    lists = bs_page_content.find_all('ul', class_='offer-params__list')
    correct_li = None
    for list in lists:
        li_list = list.find_all('li', 'offer-params__item')
        for li in li_list:
            if "Liczba miejsc" in li.get_text():
                correct_li = li

    seats = None

    if (correct_li != None):
        seats = correct_li.find('div', class_='offer-params__value').get_text().strip()

    return seats

df = pd.DataFrame(
    columns=['offer_id', 'offer_date', 'price', 'make', 'model', 'version', 'generation', 'eng_capacity', 'eng_power',
             'mileage',
             'body', 'country_of_origin', 'gearbox', 'fuel', 'prod_year', 'doors', 'seats', 'color', 'condition'])
for count, url in enumerate(list(df_urls.url)):
    print(f'No of url: {count}')
    try:
        page = get(url)
        bs = BeautifulSoup(page.content, 'html.parser')
        df = df.append({'offer_id': get_offer_id(bs),
                        'offer_date': get_offer_date(bs),
                        'price': get_price(bs),
                        'make': get_car_make(bs),
                        'model': get_car_model(bs),
                        'version': get_car_version(bs),
                        'generation': get_car_generation(bs),
                        'eng_capacity': get_eng_capacity(bs),
                        'eng_power': get_eng_power(bs),
                        'mileage': get_mileage(bs),
                        'body': get_body_type(bs),
                        'country_of_origin': get_country_of_origin(bs),
                        'gearbox': get_gearbox_type(bs),
                        'fuel': get_fuel_type(bs),
                        'prod_year': get_prod_year(bs),
                        'doors': get_doors(bs),
                        'seats': get_seats(bs),
                        'color': get_color(bs),
                        'condition': get_condition(bs)}, ignore_index=True)
        if count % 100 == 0:
            df.to_csv('otomoto_data_1.csv', index=False)
    except IndexError:
        print(f'IndexError with {count} iterate')
        pass


#print(df.to_string())
df.to_csv('otomoto_data_1.csv', index = False)
'''
print(get_price(bs))
print(get_offer_date(bs))
print(get_offer_id(bs))
print(get_car_make(bs))
print(get_car_model(bs))
print(get_body_type(bs))
print(get_country_of_origin(bs))
print(get_eng_capacity(bs))
print(get_doors(bs))
print(get_seats(bs))
print(get_color(bs))
print(get_eng_power(bs))
print(get_gearbox_type(bs))
print(get_mileage(bs))
print(get_fuel_type(bs))
print(get_condition(bs))
print(get_prod_year(bs))
print(get_car_version(bs))
print(get_car_generation(bs))
'''
