from flask import Flask, render_template, request as flask_request
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/track_price', methods=['POST'])
def track_price():
    product_asin = flask_request.form.get('product_asin')  # assumindo que você está recebendo o ASIN do formulário

    if not product_asin:
        return render_template('index.html', asin="Error: No product ASIN provided")

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

    if 'job_id' in data:
        job_id = data['job_id']

        # Aqui você faria a segunda solicitação à API usando o 'job_id'
        url = "https://price-analytics.p.rapidapi.com/poll-results"
        payload = {"job_id": job_id}

        # Poll the API until the job is finished
        for _ in range(10):  # limit to 10 attempts
            response = requests.get(url, params=payload, headers=headers)
            data = response.json()

            if data.get('status') == 'finished':
                break

            time.sleep(60)  # wait for 60 seconds before polling again

        if 'results' in data:
            asin = data['results']
        else:
            asin = "Error: 'results' not found in API response"
    else:
        asin = "Error: 'job_id' not found in API response"

    return render_template('index.html', asin=asin)

if __name__ == '__main__':
    app.run(debug=True)