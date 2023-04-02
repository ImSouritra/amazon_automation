import requests
import random
from bs4 import BeautifulSoup
import lxml

with open("amazon_links.txt", "r") as link_data:
    lines = link_data.readlines()
    link_list = [i.strip("\n") for i in lines if i != "\n" and i != " \n"]
    random.shuffle(link_list)
headers = {
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
}

count = 1


for i in link_list:
    response = requests.get(url=i, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    try:
        product_title = soup.find(name="span", id="productTitle").getText()
    except AttributeError:
        product_title=soup.select_one(".ProductShowcase__title__3eXnB")
    print(product_title)
    if "," in product_title:
        product_title = product_title.split(",")[0]
    elif "|" in product_title:
        product_title = product_title.split("|")[0]
    elif "-" in product_title:
        product_title = product_title.split("-")[0]
    try:
        product_image = soup.select_one(selector="#imgTagWrapperId .a-dynamic-image")
        img_address = product_image.get("data-a-dynamic-image").split("{")[1].split(":[")[0]
    except AttributeError:
        product_image = soup.select_one(selector="#img-canvas .a-dynamic-image")
        img_address = product_image.get("src")

    try:
        product_price = soup.select_one(selector=".a-size-medium .a-offscreen").getText()
    except AttributeError:
        product_price = ""

    old_price = soup.select_one(selector=".a-size-base .a-offscreen").getText()
    print(old_price)
    product_description = [i.getText() for i in soup.select(selector="#feature-bullets .a-unordered-list .a-list-item")]
    with open("new-file.txt", "a",encoding="utf-8") as data:
        try:
            data.write(
            f"\n\n\n<h2>{count}. {product_title}</h2>\n\n<a href='{i}'><img class='aligncenter' src={img_address} alt='' style='max-width:70%'/></a>\n\n <strong>About This Product </strong>\n <ul>\n<li>{product_description[0]}</li> \n<li>{product_description[1]}</li>\n<li>{product_description[2]}</li>\n<li>{product_description[3]}</li>\n</ul>\n\n<p> Buy now on <a href='{i}'><strong>Amazon</strong></a> for only <span style='text-decoration:line-through'>{old_price}</span> <span style='color:red;'>{product_price}</span></p>")
        except AttributeError:
            data.write(f"\n\n\n<h2>{count}. {product_title}</h2>\n\n<a href='{i}'><img class='aligncenter' src={img_address} alt='' style='max-width:70%'/></a>\n\n <strong>About This Product </strong>\n<ul><li>{product_description[0]}</li> \n <li>{product_description[1]}</li>\n<li>{product_description[2]}</li>\n</ul>\n\n<p> Buy now on <a href='{i}'><strong>Amazon</strong></a> for only <span style='text-decoration:line-through'>{old_price}</span> <span style='color:red;'>{product_price}</span></p>")
        except IndexError:
            data.write(f"\n\n\n<h2>{count}. {product_title}</h2>\n\n<a href='{i}'><img class='aligncenter' src={img_address} alt='' style='max-width:70%'/></a>\n\n <p> Buy now on <a href='{i}'><strong>Amazon</strong></a> for only <span style='text-decoration:line-through'>{old_price}</span> <span style='color:red;'>{product_price}</span></p>")
        except UnicodeError:
            data.write(f"\n\n\n<h2>{count}. {product_title}</h2>\n\n<a href='{i}'><img class='aligncenter' src={img_address} alt='' style='max-width:70%'/></a>\n\n <p> Buy now on <a href='{i}'><strong>Amazon</strong></a> for only <span style='text-decoration:line-through'>{old_price}</span> <span style='color:red;'>{product_price}</span></p>")

        count += 1

