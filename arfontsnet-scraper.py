from bs4 import BeautifulSoup as Soup
from requests import get
import re, sys, shutil, os
from urllib.request import urlretrieve

categories = ['kufi', 'naskh', 'thuluth', 'reqa3', 'diwan', 'maghribi', 'farisi', 'e3lan', 'horr', 'bassit', 'mutawar', 'gharib', 'muraba3', 'separate']

BASE = "http://www.arfonts.net/"

base_link = BASE + "?c={0}&t=unicode&p={1}"

for cat in categories:
    have_fonts = True
    i = 1
    while have_fonts:
        req = get(base_link.format(cat, i))
        req.encoding = "utf-8"
        page_bs = Soup(req.text, "lxml")

        fonts = page_bs.find_all('a', class_="downtablink")

        if len(fonts) == 0:
            have_fonts = False
        
        for f in fonts:
            if not os.path.exists(cat):
                os.makedirs(cat)
            filename = cat + '/' + f['href'].split(',')[-1] + '.zip'
            _, headers = urlretrieve(BASE + f['href'], filename)
            print(BASE + f['href'],'===>', filename)
        
        i += 1

