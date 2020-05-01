from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse


def get_parser():
    parser = argparse.ArgumentParser(
	  description='Скрипт предназначен для запуска сайта на localhost')
    parser.add_argument('data_file', help='База данных для карточек вин', nargs="?", const=1, default="wine.xlsx")
    return parser


args = get_parser().parse_args()
data_file = args.data_file

wine_data = (pandas.read_excel(data_file, na_values=['N/A', 'NA'], keep_default_na=False))
wine_data = wine_data.to_dict(orient="record")
cards_of_wines = collections.defaultdict(list)

for card in wine_data:
    cards_of_wines[card["Категория"]].append(card)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

age_of_company_in_days = (datetime.datetime.now() - datetime.datetime(year=1920, month=1, day=1)).days
days_in_year = 365
age_of_company_in_years = age_of_company_in_days // days_in_year

rendered_page = template.render(
    age_of_company=age_of_company_in_years,
    cards_of_wines=cards_of_wines,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()