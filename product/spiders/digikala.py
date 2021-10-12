import scrapy
from unidecode import unidecode
from product.items import ProductItem

class DigikalaSpider(scrapy.Spider):
    name = 'digikala'
    category = ''
    start_urls = []

    def __init__(self, category='', **kwargs):
        super().__init__(**kwargs)
        self.category = category
        self.start_urls.append(self.category)

    def parse(self, response):
        products = response.css('div.o-page__content')
        links = products.css('a.c-product-box__img::attr(href)').getall()
        for link in links:
            yield response.follow("https://www.digikala.com"+link, callback=self.parse_page)


    def parse_page(self, response):
        title = response.css('h1.c-product__title::text').get().strip().replace('\u200c',' ')
        image = response.css('img.js-gallery-img::attr(data-src)').get()
        product_url = response.xpath('/html/head/link[2]/@href').get()
        try:
            prices = response.css('div.c-price__value.js-seller-section-price::text').getall()
            prices_list = []
            for price in prices:
                prices_list.append(unidecode(price.strip().replace(',', '')))
        except:
            prices_list = []
        
        try:
            short_description = response.css('div.c-mask__text.c-mask__text--product-summary.js-mask__text::text').get().strip().replace('\u200c', ' ')
        except:
            short_description = ''


        yield {
            'title': title,
            'prices': prices_list,
            'image': image,
            'short_description': short_description,
            'product url': product_url
        }