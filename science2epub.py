"""Convert current Science magazine to epub."""

import datetime
import os

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
    f.write(f'% {date}\n\n')
    for title, author, url in tqdm(articles):
        driver.get(url)

        f.write(f'# {title}\n\n')
        f.write(f'{author}\n\n')
        try:
            cores = driver.find_elements_by_class_name('core-container')
            for core in cores:
                sections = core.find_elements_by_xpath('.//h2 | .//div[@role="paragraph"] | .//p')
                for section in sections:
                    if section.tag_name == 'h2':
                        f.write(f'## {section.text}\n\n')
                    elif section.tag_name == 'div' or section.tag_name == 'p':
                        f.write(f'{section.text}\n\n')
        except:
            print(f'Could not crawl data for {title}: {url}')

os.system(f'pandoc -s science-{date}.md -o science-{date}.epub')
