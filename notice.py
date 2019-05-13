from selenium import webdriver
from functools import reduce

BEST_NEWS_URL = "https://news.ycombinator.com/best"
NEWS_TABLE_XPATH = """'//*[@id="hnmain"]/tbody/tr[3]/td/table/tbody'"""

driver = create_webdriver()
get_best_news(driver)

def create_webdriver(path="./chromedriver.exe", wait=3):
    driver = webdriver.Chrome(path)
    driver.implicitly_wait(wait)
    return driver


def processing_title(title):
    words = title.split()[1:-1]
    return reduce(lambda x, y: x + " " + y, words, "")


def get_best_news(driver):
    links = dict()
    driver.get(BEST_NEWS_URL)
    body = driver.find_element_by_xpath(NEWS_TABLE_XPATH)
    titles = body.find_elements_by_class_name("athing")
    article_links = body.find_elements_by_class_name("storylink")
    for i in range(len(titles)):
        title = processing_title(titles[i].text)
        print(title)
        link = article_links[i].get_attribute('href')
        links[title] = link
    return links