import requests
import shutil
import bs4
import ssl
import os
import urllib

# SSL証明が正しくないサイトのスクレイピング
ssl._create_default_https_context = ssl._create_unverified_context

def image(keyword, page) :
    # params = urllib.parse.urlencode(
    #     {"q": keyword, "tbm": "isch", "ijn": str(page)}
    # )
    # res = requests.get("https://www.google.com/search?" + params)
    res = requests.get("https://www.google.com/search?hl=jp&q=" + keyword + "&btnG=Google+Search&tbs=0&safe=off&tbm=isch")
    html = res.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    links = soup.find_all("img")
    return links

def download(link, file_name, dir_name) :
    url = link.get("src")
    req = requests.get(url, stream=True)
    if req.status_code == 200 :
        os.makedirs("out/" + dir_name, exist_ok=True)
        with open("out/" + dir_name + "/" + file_name, "wb") as f :
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, f)

if __name__ == "__main__":
    # dir = "/Users/rkouhei/Desktop/Python/pict_scraping"
    # if dir != os.getcwd() :
    #     os.chdir(dir)
    #     print("change working directory")

    word = input("検索ワード : ")
    iter_num = int(input("保存数 : "))
    iter_num = 20 if iter_num > 20 else iter_num
    page = 1
    links = image(word, page)

    for i in range(1, iter_num + 1) :
        if len(links) < iter_num :
            page += 1
            links += image(word, page)

        fname = str(i) + ".jpeg"
        download(links[i], fname, word)

        if i % 10 == 0 and i != 1 :
            print(str(i) + "images downloaded")

