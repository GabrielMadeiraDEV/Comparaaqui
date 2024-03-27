from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def search_amazon(product):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    url = f"https://www.amazon.com/s?k={product}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    price_element = soup.find("span", attrs={"class":'a-offscreen'})
    if price_element is not None:
        return price_element.string, url
    else:
        return "Price not found", None

def search_ebay(product):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    url = f"https://www.ebay.com/sch/i.html?_nkw={product}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    price_element = soup.find("span", attrs={"class":'s-item__price'})
    if price_element is not None:
        return price_element.string, url
    else:
        return "Price not found", None

def parse_price(price):
    if price is None or price == "Price not found":
        return None
    return float(price.replace("$", "").replace(",", ""))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product = request.form.get('product')

        # Pesquisa na Amazon e eBay
        amazon_price, amazon_link = search_amazon(product)
        ebay_price, ebay_link = search_ebay(product)

        # Converte os preços para números
        amazon_price = parse_price(amazon_price)
        ebay_price = parse_price(ebay_price)

        # Compara os preços e retorna o menor
        if amazon_price is None:
            return render_template('index.html', price=ebay_price, link=ebay_link)
        elif ebay_price is None:
            return render_template('index.html', price=amazon_price, link=amazon_link)
        elif amazon_price < ebay_price:
            return render_template('index.html', price=amazon_price, link=amazon_link)
        else:
            return render_template('index.html', price=ebay_price, link=ebay_link)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)