from selenium import webdriver
from functools import reduce

from sanic import Sanic
from sanic.response import json, html

BEST_NEWS_URL = "https://news.ycombinator.com/best"
ACTIVE_NEWS_URL = "https://news.ycombinator.com/active"
NEWS_TABLE_XPATH = """//*[@id="hnmain"]/tbody/tr[3]/td/table/tbody"""
HTML_FORMAT = "<li><a href='{url}'>{title}</a><li>"
history = []

dr = create_webdriver()
l = get_news(dr, [BEST_NEWS_URL, ACTIVE_NEWS_URL])


def create_webdriver(path="./chromedriver.exe", wait=3):
    driver = webdriver.Chrome(path)
    driver.implicitly_wait(wait)
    return driver


def get_news(driver, links):
    news = dict()
    for link in links:
        news.update(get_news_from_link(driver, link))
    return news


def get_news_from_link(driver, link):
    titles, article_links = get_title_and_links(driver, link)
    return get_processed_links(titles, article_links)


def get_title_and_links(web_driver, link):
    web_driver.get(link)
    body = web_driver.find_element_by_xpath(NEWS_TABLE_XPATH)
    titles = body.find_elements_by_class_name("athing")
    links = body.find_elements_by_class_name("storylink")
    return titles, links


def get_processed_links(titles, article_links):
    links = dict()
    for i in range(len(titles)):
        title = processing_title(titles[i].text)
        link = get_link_from_eliment(article_links[i])
        if is_new_link(link):
            title = change_new_title(title)
        history.append(link)
        links[title] = link
    return links


def processing_title(title):
    words = title.split()[1:-1]
    return reduce(lambda x, y: x + " " + y, words)


def get_link_from_eliment(el):
    return el.get_attribute('href')


def is_new_link(link):
    return not link in history


def change_new_title(title_text):
    return "[NEW]" + title_text


def dict_to_html(articles):
    keys = articles.keys()
    result_html = ""
    for key in keys:
        result_html += HTML_FORMAT.format(
            title=key, url=articles[key])
    return "<ol>{html}</ol>".format(html=result_html)


## This is WebServer


app = Sanic()


@app.route('/')
async def main_news(request):
    return html(dict_to_html(l))


@app.route('/reload')
async def reload_news(request):
    global l
    l = get_news(dr, [BEST_NEWS_URL, ACTIVE_NEWS_URL])
    return json(
        {"reload news": "seccess"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
