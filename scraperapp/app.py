from flask import Flask, request, jsonify, send_from_directory
from scraper import BFSScraper
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/scrape', methods=['POST'])
def scrape_route():
    data = request.get_json() or {}
    api_key = data.get('api_key')
    domain = data.get('domain')
    workers = int(data.get('workers', 5))
    if not api_key or not domain:
        return jsonify({'message': 'api_key and domain required'}), 400

    scraper = BFSScraper(api_key, domain, workers=workers)
    if not api_key or not domain:
        return jsonify({'message': 'api_key and domain required'}), 400

    scraper = BFSScraper(api_key, domain)
    scraper.run()
    return jsonify({'message': 'scraping finished'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
