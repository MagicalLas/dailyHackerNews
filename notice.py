from selenium import webdriver

driver = create_webdriver()
links = dict()
driver.get("https://news.ycombinator.com/best")
body = driver.find_element_by_xpath(
    '//*[@id="hnmain"]/tbody/tr[3]/td/table/tbody')
titles = body.find_elements_by_class_name("athing")
article_links = body.find_elements_by_class_name("storylink")
for i in range(len(titles)):
    title = processing_title(titles[i].text)
    print(title)
    link = article_links[i].get_attribute('href')
    links[title] = link


def create_webdriver(path="./chromedriver.exe", wait=3):
    driver = webdriver.Chrome(path)
    driver.implicitly_wait(wait)
    return driver
