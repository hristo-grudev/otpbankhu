import json

import scrapy

from scrapy.loader import ItemLoader

from ..items import OtpbankhuItem
from itemloaders.processors import TakeFirst


class OtpbankhuSpider(scrapy.Spider):
	name = 'otpbankhu'
	start_urls = ['https://www.otpbank.hu/apps/composite/api/news?start=0&rows=999999&segment=H']

	def parse(self, response):
		data = json.loads(response.text)
		for post in data['hits']:
			date = post['date']
			title = post['title']
			url = post['url']
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, date, title):
		description = response.xpath('//section[@class="a11y mhte"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=OtpbankhuItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
