import crochet

crochet.setup()

from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
import time

from scrapy.utils.project import get_project_settings
import os
from product.spiders.digikala import DigikalaSpider

app = Flask(__name__)

output_data = []
project_settings = get_project_settings()
crawl_runner = CrawlerProcess(settings = project_settings)


@app.route('/')
def index():
	return render_template("index.html") 


@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        s = request.form['category_link'] 
        global category
        category = s
        if os.path.exists("output.json"): 
        	os.remove("output.json")
        return redirect(url_for('scrape'))


@app.route("/scrape")
def scrape():
    scrape_with_crochet(category=category)
    time.sleep(20) 
    return jsonify(output_data) 
  

@crochet.run_in_reactor
def scrape_with_crochet(category):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(DigikalaSpider, category = category)
    return eventual


def _crawler_result(item, response, spider):
    output_data.append(dict(item))


if __name__== "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)