import requests
from lxml import html
import json
import os


#Request to https://store.steampowered.com/explore/new/
response = requests.get("https://store.steampowered.com/explore/new/")
#Check status
# if response.ok:
#     print(response.text)
# else:
#     print(f'{response.status_code}')

tree = html.fromstring(response.content)

#scrap data by new release id
new_releases = tree.xpath('//div[@id="tab_newreleases_content"]')[0]
#get title name 
title = new_releases.xpath('.//div[@class="tab_item_name"]/text()')

#print output to terminal
#print(title)

#get price data
prices=new_releases.xpath('.//div[@class="discount_final_price"]/text()')

tag_items = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
tags = []
for div in tag_items:
    tags.append(div.text_content())

for tag in tags:
    tag.split(', ')

#get platform supported data
platform_div = new_releases.xpath('.//div[@class="tab_item_details"]')
total_platforms = []

for game in platform_div:
    temp = game.xpath('.//span[contains(@class, "platform_img")]')
    platforms = [t.get('class').split(' ')[-1] for t in temp]
    if 'hmd_separator' in platforms:
        platforms.remove('hmd_separators')
    total_platforms.append(platforms)

#make dictionary from all of data above
output = []
for info in zip(title, prices, tags, total_platforms):
    resp = {}
    resp['title'] = info[0]
    resp['prices'] = info [1]
    resp['tag_items'] = info[2]
    resp['total_platforms'] = info[3]
    output.append(resp)
    
#print(output)

#give an output with json format
with open(r'D:\Arsip Belajar Mandiri\Python\Project\steam_scarpping\output\output.json', 'w', encoding='utf-8') as save_output:
    json.dump(output, save_output, indent=2, ensure_ascii=False)
