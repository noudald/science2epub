"""Convert current Science magazine to epub."""

import datetime

from selenium import webdriver
from tqdm import tqdm

driver = webdriver.Firefox()
driver.get('https://www.science.org/toc/science/current')

elem = driver.find_element_by_class_name('toc')
articles = []
for card in elem.find_elements_by_class_name('card-content'):
    title = card.find_element_by_class_name('article-title [href]')
    author = card.find_element_by_class_name('card-meta')
    print(title.text, author.text, title.get_attribute('href'))
    articles.append((title.text, author.text, title.get_attribute('href')))

input('Press enter after login')

date = datetime.date.today().strftime('%Y%m%d')
with open(f'science-{date}.md', 'w') as f:
    f.write('% Science\n')
    f.write('% {date}\n\n')
    for title, author, url in tqdm(articles):
        driver.get(url)

        f.write(f'# {title}\n\n')
        f.write(f'{author}\n\n')
        try:
            elem = driver.find_element_by_xpath('.//section[@id="bodymatter"]')
            sections = elem.find_elements_by_xpath('.//section')
            for section in sections:
                ptitle = section.find_element_by_xpath('.//h2').text
                ptext = section.find_element_by_xpath('.//div[@role="paragraph"]').text
                f.write(f'## {ptitle}\n\n')
                f.write(f'{ptext}\n\n')
        except:
            try:
                elem = driver.find_element_by_class_name('bodySection')
            except:
                elem = driver.find_element_by_class_name('core-container')

            paragraphs = (elem.find_elements_by_xpath('.//p')
                + driver.find_elements_by_xpath('.//div[@role="paragraph"]'))
            for paragraph in paragraphs:
                if len(paragraph.text) > 10:
                    f.write(paragraph.text + '\n\n')
