from flask import Flask, render_template, request
import requests
import re
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/track_price', methods=['POST'])
def track_price():
    product_asin = request.form.get('product_asin')  # assumindo que você está recebendo o ASIN do formulário

    url = "https://price-analytics.p.rapidapi.com/search-by-term"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Host": "price-analytics.p.rapidapi.com",
        "X-RapidAPI-Key": "099d3e35fdmshf5d7bec1f8d47f4p11d405jsne2b10d2b9df4"
    }
    payload = {
        "source": "amazon",
        "country": "de",
        "key": "asin",
        "values": product_asin
    }

    response = requests.post(url, data=payload, headers=headers)

    data = response.json()
    print(data)  # Imprima a resposta completa da API

    if 'price' in data:
        price = data['price']
    else:
        price = "Error: 'price' not found in API response"

    return render_template('index.html', price=price)

if __name__ == '__main__':
    app.run(debug=True)