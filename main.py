from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections

excel_data = (pandas.read_excel("wine3.xlsx", na_values=['N/A', 'NA'], keep_default_na=False)).to_dict(orient="record")
cards_of_wines = collections.defaultdict(list)
for card in excel_data:
    cards_of_wines[card["Категория"]].append(card)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    age_of_company=int((datetime.datetime.now() - datetime.datetime(year=1920, month=1, day=1)).days / 365),
    cards_of_wines=cards_of_wines,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()