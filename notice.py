from selenium import webdriver
from functools import reduce

from sanic import Sanic
from sanic.response import json, html

BEST_NEWS_URL = "https://news.ycombinator.com/best"
ACTIVE_NEWS_URL = "https://news.ycombinator.com/active"
NEWS_TABLE_XPATH = """//*[@id="hnmain"]/tbody/tr[3]/td/table/tbody"""
HTML_FORMAT = "<li><a href='{url}'>{title}</a><li>"
history = []


def create_webdriver(path="./chromedriver.exe", wait=3):
    driver = webdriver.Chrome(path)
    driver.implicitly_wait(wait)
    return driver


def processing_title(title):
    words = title.split()[1:-1]
    return reduce(lambda x, y: x + " " + y, words)


def get_best_news(driver):
    links = dict()
    driver.get(BEST_NEWS_URL)
    body = driver.find_element_by_xpath(NEWS_TABLE_XPATH)
    titles = body.find_elements_by_class_name("athing")
    article_links = body.find_elements_by_class_name("storylink")
    for i in range(len(titles)):
        title = processing_title(titles[i].text)
        link = article_links[i].get_attribute('href')
        if not link in history:
            title = "[NEW]" + title
        history.append(link)
        links[title] = link
    return links


def get_active_news(driver):
    links = dict()
    driver.get(ACTIVE_NEWS_URL)
    body = driver.find_element_by_xpath(NEWS_TABLE_XPATH)
    titles = body.find_elements_by_class_name("athing")
    article_links = body.find_elements_by_class_name("storylink")
    for i in range(len(titles)):
        title = processing_title(titles[i].text)
        link = article_links[i].get_attribute('href')
        if not link in history:
            title = "[NEW]" + title
        history.append(link)
        links[title] = link
    return links


def dict_to_html(articles):
    keys = articles.keys()
    result_html = ""
    for key in keys:
        result_html += HTML_FORMAT.format(
            title=key, url=articles[key])
    return "<ol>{html}</ol>".format(html=result_html)


app = Sanic()
dr = create_webdriver()
l = get_best_news(dr)


@app.route('/')
async def main_news(request):
    return html(dict_to_html(l))


@app.route('/reload')
async def reload_news(request):
    global l
    l = get_best_news(dr)
    l.update(get_active_news(dr))
    return json(
        {"reload news": "seccess"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
