from exchangeratesapi import Api
import pandas as pd

api = Api()

df_raw = pd.read_csv('otomoto_data.csv')
df = df_raw.copy()

# eng_capacity always has cm3, I can erase it
df.eng_capacity = [f'{capacity}'[:-4].replace(' ', '') for capacity in df['eng_capacity']]
df.eng_capacity = pd.to_numeric(df.eng_capacity)

# eng_power always has km, also can erase it
df.eng_power = [f'{power}'[:-3].replace(' ', '') for power in df['eng_power']]
df.eng_power = pd.to_numeric(df.eng_power)

# create new feature - currency
df['currency'] = [str(price)[-3:] for price in df.price]
df.price = [str(price).replace(',', '.') for price in df.price]
df.price = [str(price)[:-3].replace(' ', '') for price in df.price]
df.price = pd.to_numeric(df.price)

# collect all currencies excluding PLN
currencies = list(df.currency.unique())

if 'PLN' in currencies:
    currencies.remove('PLN')

# Get exchange rates by exchangeratesapi for every currency
rate = {}
for count, currency in enumerate(list(df.currency.unique())):
    rate[currency] = api.get_rates(currency, ['PLN'])['rates']['PLN']

# changing all the prices into PLN and deleting currency feature
for currency in rate:
    dff = df.loc[df.currency == currency, 'price']
    df.loc[df.currency == currency, 'price'] = [rate[currency] * price for price in list(dff)]

df = df.drop('currency', axis=1)

# erase km from mileage
df['mileage'] = [str(mileage)[:-3].replace(' ', '') for mileage in df['mileage']]

df.loc[df.version.isna(), 'version'] = 'Nie podano'
df.loc[df.generation.isna(), 'generation'] = 'Nie podano'
df.loc[df.country_of_origin.isna(), 'country_of_origin'] = 'Nie podano'

df.to_csv('preprocessed_otomoto_data.csv')