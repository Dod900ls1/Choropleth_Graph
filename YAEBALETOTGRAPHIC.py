import pandas as pd
import plotly.express as px
import json
from Encoder import NpEncoder
import re

with open('data.json') as json_data:
    data = json.load(json_data)

df = pd.DataFrame(data['data'])
df = df[['lc', 'unique']]
df = df.dropna(subset=['lc'])
df = df.groupby(['lc'], as_index=False).count()
# all files that i was needed
country = pd.read_excel('Code1.xlsx')
country2 = pd.read_excel('Code2.xlsx')
countries = pd.read_excel('countries.xlsx')
countryToCode = pd.read_excel('contryToCode.xlsx')[['Cname', '3lCode']]
Nations = pd.read_excel('Nation.xlsx')
countryToCode.dropna(inplace=True)
countryToCode.reset_index(inplace=True, drop=True)

# Data manipulation
CodeList = []
AllCountries = []

for i in range(len(df)):

    for j in range(len(country['code'])):  # making from country code - country
        if df['lc'][i] == country['code'][j]:
            df.replace(df['lc'][i], country['name'][j], inplace=True)
        elif j == len(country['code']) - 1:
            for l in range(len(country2)):
                if df['lc'][i] == country2['code'][j]:
                    df.replace(df['lc'][i], country2['name'][j], inplace=True)

    for k in range(len(countries)):
        x = re.sub(r'^\W*\w+\W*|\(|\)', '', df['lc'][i])
        if x == countries['country'][k]:
            df.replace(df['lc'][i], x, inplace=True)
            AllCountries.append(x)
            break
        elif k == len(countries) - 1:
            df.replace(df['lc'][i], df['lc'][i].split()[0], inplace=True)

    for p in range(len(Nations)):
        if df['lc'][i] == Nations['Nationality'][p]:
            df.replace(df['lc'][i], Nations['Country'][p], inplace=True)
            AllCountries.append(Nations['Country'][p])

df = df[df['lc'].isin(AllCountries)] # deleting all missing data

df = df.groupby(['lc'], as_index=False).sum()

for i in range(len(df)):  # making new bar which have  ISO 3166 country code for graph
    for j in range(len(countryToCode)):
        if df['lc'][i] == countryToCode['Cname'][j]:
            CodeList.append(countryToCode['3lCode'][j])
            break
        elif j == len(countryToCode) - 1:
            df.drop(i, inplace=True)

df.reset_index(drop=True)
df['CityCode'] = CodeList
# Graph scetching
fig = px.choropleth(df, locations='CityCode', hover_name='lc', color='unique')
fig.show()

columns = list(df.columns)
data_columns = [list(df[columns[i]]) for i in range(len(columns))]


print(data_columns)

def process_data(columns, data_columns):
    return dict(zip(columns, data_columns))  # making dictionary


sample = process_data(columns, data_columns)

with open('ChoroplethData.json', 'w') as fp:
    json.dump(sample, fp=fp, cls=NpEncoder)  # making JSON file which include date occurences


