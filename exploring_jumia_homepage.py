from scrapy import Selector
from urllib.request import urlopen, Request
import requests
import pandas as pd
import matplotlib.pyplot as plt

jumia ="https://www.jumia.com.ng/?gclid=Cj0KCQjwqPGUBhDwARIsANNwjV5P_Y6h8lGzLQxPsBdWEG3ekyP07gjrteVmf97fR_PXPIqOX6qqvKUaAqjvEALw_wcB"

# getting the jumia html
jumia_html = requests.get(jumia).content
jumia_sel = Selector( text = jumia_html )

jumia_name = jumia_sel.xpath('//div[@class="name"]/text()').extract()
jumia_price = jumia_sel.xpath('//div[@class="prc"]/text()').extract()

# selecting only grocery items
grocery_name = jumia_sel.xpath('//a[contains(@data-category, "Grocery")]/div[@class="name"]/text()').extract()
grocery_price = jumia_sel.xpath('//a[contains(@data-category, "Grocery")]/div[@class="prc"]/text()').extract()

price_list = [int(x.removeprefix('₦ ').replace(',', '')) for x in grocery_price]
cat1 = ["Grocery" for x in grocery_name]

grocery_dict = {'name': grocery_name, 'price': price_list, 'category': cat1}
df = pd.DataFrame(grocery_dict)


# selecting only Health & Beauty items
hnb_name = jumia_sel.xpath('//a[contains(@data-category, "Health & Beauty")]/div[@class="name"]/text()').extract()
hnb_price = jumia_sel.xpath('//a[contains(@data-category, "Health & Beauty")]/div[@class="prc"]/text()').extract()

price_list2 = [int(x.removeprefix('₦ ').replace(',', '')) for x in hnb_price]
cat2 = ["Health & Beauty" for x in hnb_name]

hnb_dict = {'name': hnb_name, 'price': price_list2, 'category': cat2}
df2 = pd.DataFrame(hnb_dict)

# Concatenate the two Dataframes
store = pd.concat([df, df2])

# Getting links
links = jumia_sel.xpath('//a[@class="core"]/@href').extract()
##item_name = jumia_sel.xpath('//a[@class="core"]/div[@class="name"]/text').extract()

link_dict = {"link": links, "item_name": jumia_name}
df3 = pd.DataFrame(link_dict)
