from bs4 import BeautifulSoup as Soup
from requests import get
import re, os
from urllib.request import urlretrieve
from urllib.parse import quote

BASE = "https://www.arfonts.net{}"
BASE_PAGE = BASE + "&u={}"
FONT_DL = "https://www.arfonts.net/fontfiles/zips/{}.zip"
IMG_DL = BASE.format("/edits/textpreview.php?text=" +
                     quote("أبجد هوز حطي كلمن سعفص قرشت ثخذ ضظغ") +
                     "&font={}&ctx=000000&cbg=ffffff")
IMG_DL.encode("utf-8")

first_page = get(BASE.format(""))
first_page.encoding = "utf-8"

first_page = Soup(first_page.text, features="lxml")

sidebar = first_page.find('nav', id='mySidebar')

categories = sidebar.find_all('a', {
    'id': re.compile("^[a-z]{3}$"),
    'href': re.compile('^/c:.*')
})

if not os.path.exists("fonts"):
    os.makedirs("fonts")

for cat in categories:
    have_fonts = True
    i = 1
    while have_fonts:
        req = get(BASE_PAGE.format(cat['href'], i))
        req.encoding = "utf-8"
        page_bs = Soup(req.text, "lxml")

        fonts = page_bs.find_all("button", class_='dbutton')
        images = page_bs.find_all("button", class_='dbutton')

        if len(fonts) == 0:
            have_fonts = False

        for f in fonts:
            if not os.path.exists('fonts/' + cat.text):
                os.makedirs('fonts/' + cat.text)
            fontname = f['onclick'][25:].strip("'")
            filename = "fonts/{0}/{1}".format(cat.text, fontname)
            _, headers = urlretrieve(FONT_DL.format(fontname),
                                     filename + '.zip')
            urlretrieve(IMG_DL.format(fontname), filename + '.png')

            print(fontname)

        i += 1
