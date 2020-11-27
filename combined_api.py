from flask import Flask, jsonify, Response
from flask import request
from flask_caching import Cache
from typing import Dict, List, Set
import urllib.request, json
import re
import time
import multiprocessing
import threading
import traceback
import os

app = Flask(__name__, static_folder='build/', static_url_path='/')
cache = {}
lock = threading.Lock()
categories = ['jackets','shirts','accessories']
retries = 3

def cache_worker():
    while True:
        time.sleep(300)
        print("Refreshing cache...")
        load_data()

def get_availabilities(manufacturers: Set) -> Dict:
    availabilities = {}
    for manufacturer in manufacturers:
        print("Requesting availabilities for manufacturer {}".format(manufacturer))
        producer_req = urllib.request.Request("https://bad-api-assignment.reaktor.com/availability/" + manufacturer)
        producer_req.add_header('x-force-error-mode', 'no')
        with urllib.request.urlopen(producer_req) as urlProducer:
            dataProducer = json.loads(urlProducer.read().decode())
            res = dataProducer['response']
            for product in res:
                product_id = str(product['id']).lower()
                m = re.search('<INSTOCKVALUE>(.+?)<\/INSTOCKVALUE>', product['DATAPAYLOAD'])
                if m:
                    availabilities[manufacturer + '_' + product_id] = m.group(1)
    
    return availabilities


def get_products(category: str) -> Dict:
    print("Requesting products for category {}".format(category))
    req = urllib.request.Request('https://bad-api-assignment.reaktor.com/products/' + category)
    req.add_header('x-force-error-mode', 'no')

    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        return data

    raise RuntimeError("Unable to load products")

def load_data():
    availabilities = {}
    manufacturers_done = set()

    for cat in categories:
        for i in range(retries):
            try:
                products = get_products(cat)
            except Exception as e:
                traceback.print_exc()
                print ("Retrying products for category {}".format(cat))
                continue
            else:
                break
        else:
            continue

        manufacturers = set([x['manufacturer'] for x in products])
        missing_manufacturers = manufacturers - manufacturers_done

        for i in range(retries):
            new_availabilities = {}
            try:
                new_availabilities = get_availabilities(missing_manufacturers)
            except Exception as e:
                traceback.print_exc()
                print ("Retrying availabilities")
                continue
            else:
                availabilities.update(new_availabilities)
                manufacturers_done.update(missing_manufacturers)
                break

        for item in products:
            product_id = str(item['id']).lower()
            key = item['manufacturer'] + '_' + product_id

            if key in availabilities:
                item['availability'] = availabilities[key]
            else:
                item['availability'] = 'UNKNOWN'

        with lock:
            cache[cat] = products

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)            

@app.route('/products/<section>', methods={'GET'})
def get(section):
    with lock:
        return jsonify(cache[section])

def run():
    print("Initializing with data")
    # Load initial data
    load_data()

    # Start worker to update data in the background
    p = multiprocessing.Process(target=cache_worker)
    p.start()

    #port = os.getenv('PORT', 5000)
    #app.run(debug=False, host='0.0.0.0', port=port)
    return app

if __name__=="__main__":
    run()
