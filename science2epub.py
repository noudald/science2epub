"""Convert current Science magazine to epub."""

import datetime
import os

from tempfile import mkdtemp

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

tempdir = mkdtemp()
date = datetime.date.today().strftime('%Y%m%d')
with open(f'{tempdir}/science-{date}.md', 'w') as f:
    f.write(f'% Science Magazine {date}\n')
    f.write('% Science\n\n')
    for title, author, url in tqdm(articles):
        driver.get(url)

        f.write(f'# {title}\n\n')
        f.write(f'{author}\n\n')
        cores = driver.find_elements_by_class_name('core-container')
        if len(cores) == 0:
            cores = driver.find_elements_by_class_name('bodySection')
        for core in cores:
            sections = core.find_elements_by_xpath('.//h2 | .//div[@role="paragraph"] | .//p | .//figure')
            for section in sections:
                if section.tag_name == 'h2':
                    f.write(f'## {section.text}\n\n')
                elif section.tag_name == 'div' or section.tag_name == 'p':
                    f.write(f'{section.text}\n\n')
                elif section.tag_name == 'figure':
                    try:
                        img_src = section.find_element_by_xpath('.//img').get_attribute('src')
                    except:
                        print(f'Could not extract image from: {url}')
                        continue
                    try:
                        fn_caption = section.find_element_by_xpath('.//div[@class="caption"]').text
                    except:
                        fn_caption = ''
                    try:
                        fn_notes = section.find_element_by_xpath('.//div[@class="notes"]').text
                    except:
                        fn_notes = ''
                    os.system(f'wget {img_src} --directory-prefix={tempdir}')
                    img_path = img_src.split('/')[-1]
                    f.write(f'![{fn_caption}: {fn_notes}]({tempdir}/{img_path})\n\n')

print('Converting images to correct sizes.')
os.system(f'for file in $(find {tempdir}/*.jpg -type f); do echo $file; convert -resize 500x500\\> $file $file; done')
os.system(f'for file in $(find {tempdir}/*.svg -type f); do echo $file; convert -resize 500x500\\> $file $file; done')
print('Create epub')
os.system(f'pandoc --number-sections -s {tempdir}/science-{date}.md -o ./science-{date}.epub')
