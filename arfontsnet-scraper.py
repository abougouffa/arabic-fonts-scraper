from bs4 import BeautifulSoup as Soup
from requests import get
import re, os
from urllib import request
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

            # SPECIFIC MESSAGE:
            # I know there is someone (let's call him "Mr. X") from ARFONTS.NET who keep tracking this script,
            # and changes their code just to make this script useless! hahaha
            # So "Mr. X" if you are reading my comment, let me thank you for your website and for the content
            # you provides.
            # But if I have to download some fonts from your website, I don't have to take one day clicking
            # on every individual link!, so I will keep maintaining this script just because I'm a lazy person!
            # The last time, I had to rewrite some parts of the script, but this time I added just 3 lines of code.
            # Thank you for making it easy for me, have a good day "Mr. X"!!
            opener = request.build_opener()
            opener.addheaders = [(
                'User-agent',
                'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
            )]
            request.install_opener(opener)

            _, headers = urlretrieve(FONT_DL.format(fontname),
                                     filename + '.zip')
            urlretrieve(IMG_DL.format(fontname), filename + '.png')

            print(fontname)

        i += 1
