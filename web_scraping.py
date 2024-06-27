from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    book_data = []
    for book in books:
        title = book.h3.get_text()
        price = book.find('p', class_='price_color').get_text()
        book_data.append([title, price])
    df = pd.DataFrame(book_data, columns=['Title', 'Price'])
    df.to_csv('books.csv', index=False)
    return render_template('result.html', tables=[df.to_html(classes='data', header="true")], titles=df.columns.values)

if __name__ == '__main__':
    app.run(debug=True)