from scrapy import Selector
from urllib.request import urlopen, Request
import requests
import pandas as pd
import matplotlib.pyplot as plt

url = "https://www.wikipedia.org/"
jumia ="https://www.jumia.com.ng/?gclid=Cj0KCQjwqPGUBhDwARIsANNwjV5P_Y6h8lGzLQxPsBdWEG3ekyP07gjrteVmf97fR_PXPIqOX6qqvKUaAqjvEALw_wcB"

# getting the html using urlopen
req = Request(url)
with urlopen(req) as resp:
    html = resp.read()

# getting the html using requests .text and .content
''' Presumably r.text would be preferred for textual responses,
    such as an HTML or XML document, and r.content would be preferred for
    "binary" filetypes, such as an image or PDF file. (Stackoverflow)
'''
html_doc = requests.get(url).text
html_doc2 = requests.get(url).content

####
# getting all the <p> tags using scrapy xpath selector
sel = Selector( text = html )
p_selector_list = sel.xpath("//p")
p_tags = p_selector_list.extract()

# getting the body of the html code
sel_2 = Selector( text = html )
body_selector_list = sel_2.xpath("//body")
body_tag = body_selector_list.extract()

# getting all div tags from the body tag above
div_sel_list = body_selector_list.xpath(".//div")

####
# using CSS locators
css_1 = sel.css("body div")

### Exploring the Jumia site Home Page
# getting the jumia html
jumia_html = requests.get(jumia).content
jumia_sel = Selector( text = jumia_html )

jumia_name = jumia_sel.xpath('//div[@class="name"]/text()').extract()
jumia_price = jumia_sel.xpath('//div[@class="prc"]/text()').extract()

# selecting only grocery items
grocery_name = jumia_sel.xpath('//a[contains(@data-category, "Grocery")]/div[@class="name"]/text()').extract()
grocery_price = jumia_sel.xpath('//a[contains(@data-category, "Grocery")]/div[@class="prc"]/text()').extract()

price_list = []
for x in grocery_price:
    price_list.append(int(x.removeprefix('₦ ').replace(',', '')))
    
grocery_dict = {'name': grocery_name, 'price': price_list}
df = pd.DataFrame(grocery_dict)

# selecting only Health & Beauty items
hnb_name = jumia_sel.xpath('//a[contains(@data-category, "Health & Beauty")]/div[@class="name"]/text()').extract()
hnb_price = jumia_sel.xpath('//a[contains(@data-category, "Health & Beauty")]/div[@class="prc"]/text()').extract()

price_list2 = []
for x in hnb_price:
    price_list2.append(int(x.removeprefix('₦ ').replace(',', '')))
    
hnb_dict = {'name': hnb_name, 'price': price_list2}
df2 = pd.DataFrame(hnb_dict)









