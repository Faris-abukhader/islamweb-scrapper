import asyncio
import aiohttp
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json


class IslamWeb:

    def __init__(self, chunk_length=2000):
        self.url = 'https://www.islamweb.net'
        self.spider_links = []
        self.scraped_entities = []
        self.categories = []
        self.chunk_length = chunk_length
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
        self.article_page_number = 0
        self.qAa_page_number = 0
        self.counter = 1

    async def get_article_categories(self):
        url = f'{self.url}/ar/articles'

        content = get(url).content
        soup = BeautifulSoup(content, 'html.parser')

        tasks = []
        total_timeout = aiohttp.ClientTimeout(total=60 * 2)
        connector = aiohttp.TCPConnector(limit=99)
        semaphore = asyncio.Semaphore(150)
        async with semaphore:
            async with aiohttp.ClientSession(connector=connector, timeout=total_timeout) as session:
                try:
                    for category in soup.find('div', {'class': 'fatCatleft'}).find_all('li'):
                        tasks.append(asyncio.create_task(
                            self.get_article_category_page_number(category.find('a')['href'], session)))
                    await asyncio.gather(*tasks)
                except Exception as e:
                    print(e)

    async def get_article_category_page_number(self, target_path, session):
        url = f'{self.url}/{target_path}'
        print(f'scrapping : {url}')

        try:
            do_it = True
            counter = 0
            while do_it:
                if counter == 7:
                    break
                async with session.get(url) as r:
                    if r.status != 200:
                        r.raise_for_status()

                    website = await r.read()  # .text() # r.text(encoding='windows-1251')#gzip
                    soup = BeautifulSoup(website, 'lxml')

                    try:

                        pages_num = soup.find('div', {'class': 'Page-navigation'}).find('ul', {'class': 'pagination'}).find_all(
                            'li')[-2].find_next('a')['href'].split('=')[1]

                        print(f'total pages under {target_path} path is : {pages_num} pages')

                        self.categories.append({'category': target_path, 'page_number': pages_num, 'links': []})
                        do_it = False
                    except Exception as e:
                        do_it = True
                        counter += 1
                        print(url, e)
        except Exception as e:
            print(e)

    async def get_articles_page_articles(self, page_index, session, category):
        url = f'{self.url}/{category}?pageno={str(page_index)}'
        do_it = True
        counter = 1
        try:
            while do_it:
                if counter == 7:
                    break
                async with session.get(url) as r:
                    if r.status != 200:
                        r.raise_for_status()

                    try:
                        website = await r.read()  # .text() # r.text(encoding='windows-1251')#gzip
                        soup = BeautifulSoup(website, 'html.parser')

                        for article in soup.find('ul', {'class': 'oneitems'}).find_all('li'):
                            link = article.find_next('a')['href']

                            if r.get_encoding() == 'ptcp154':
                                link = link.encode('iso-8859-5')

                            print(counter,url, category, link)
                            self.spider_links.append({'category': category, 'link': link})
                            do_it = False
                    except Exception as e:
                        print(e)
                        do_it = True
                        counter += 1
        except Exception as e:
            print(e)

    async def get_question_links(self):
        url = f'{self.url}/ar/fatwa/loadmoreisti.php?startno='
        tasks = []
        total_timeout = aiohttp.ClientTimeout(total=60 * 2)
        connector = aiohttp.TCPConnector(limit=99)
        semaphore = asyncio.Semaphore(150)
        async with semaphore:
            async with aiohttp.ClientSession(connector=connector, timeout=total_timeout) as session:
                try:
                    for num in range(30,4000,30):
                        tasks.append(asyncio.create_task(self.get_question_page_questions(url+f'{num}', session)))
                    await asyncio.gather(*tasks)
                except Exception as e:
                    print(e)
        with open(f'{(int(time.time() * 1000))}_islamweb_fatwa.json','w') as file:
            json.dump(self.spider_links,file,ensure_ascii=False)

    async def get_question_page_questions(self, url, session):

        try:
            async with session.get(url) as r:
                if r.status != 200:
                    r.raise_for_status()

                try:
                    website = await r.read()  # .text() # r.text(encoding='windows-1251')#gzip
                    soup = BeautifulSoup(website, 'html.parser')

                    for article in soup.find_all('li'):
                        link = article.find_next('a')['href']

                        if r.get_encoding() == 'ptcp154':
                            link = link.encode('iso-8859-5')

                        print(url, link)
                        self.spider_links.append(link)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    async def get_consult_links(self):
        url = f'{self.url}/ar/consult/loadmoreisti.php?startno='
        tasks = []
        total_timeout = aiohttp.ClientTimeout(total=60 * 2)
        connector = aiohttp.TCPConnector(limit=99)
        semaphore = asyncio.Semaphore(150)
        async with semaphore:
            async with aiohttp.ClientSession(connector=connector, timeout=total_timeout) as session:
                try:
                    for num in range(30,4000,30):
                        tasks.append(asyncio.create_task(self.get_consult_page_consults(url+f'{num}', session)))
                    await asyncio.gather(*tasks)
                except Exception as e:
                    print(e)
        with open(f'{(int(time.time() * 1000))}_islamweb_consult.json','w') as file:
            json.dump(self.spider_links,file,ensure_ascii=False)

    async def get_consult_page_consults(self, url, session):

        try:
            async with session.get(url) as r:
                if r.status != 200:
                    r.raise_for_status()

                try:
                    website = await r.read()  # .text() # r.text(encoding='windows-1251')#gzip
                    soup = BeautifulSoup(website, 'html.parser')

                    for article in soup.find_all('li'):
                        link = article.find_next('a')['href']

                        if r.get_encoding() == 'ptcp154':
                            link = link.encode('iso-8859-5')

                        print(url, link)
                        self.spider_links.append(link)
                except Exception as e:
                    print('alooo ',e)
        except Exception as e:
            print(e)

    async def send_spider(self, path, page_index, session, category=''):
        if path == 'fatwa':
            await self.get_question_page_questions(page_index, session,category)
        elif path == 'articles':
            await self.get_articles_page_articles(page_index, session, category)

    async def save_questions_link(self):
        await self.get_question_links()

    async def save_consult_link(self):
        await self.get_consult_links()

    async def save_articles_link(self, file_name=f'{(int(time.time() * 1000))}_islamweb_articles_url.json'):
        await self.get_article_categories()
        await self.create_spider_tasks(file_name, 'articles')

    async def create_spider_tasks(self, file_name, path):

        tasks = []
        total_timeout = aiohttp.ClientTimeout(total=60 * 10)
        connector = aiohttp.TCPConnector(limit=50)
        semaphore = asyncio.Semaphore(150)
        async with semaphore:
            async with aiohttp.ClientSession(connector=connector, timeout=total_timeout) as session:
                try:

                    for category in self.categories:
                        for index in range(1, int(category['page_number']) + 1):
                            tasks.append(
                                asyncio.create_task(self.send_spider(path, index, session, category['category'])))
                    await asyncio.gather(*tasks)
                except Exception as e:
                    print(e)

        with open(file_name, 'w') as file:
            json.dump(self.spider_links, file, ensure_ascii=False)
            self.spider_links = []

    async def save_entities(self, entity_name, file_name):
        with open(file_name) as json_file:
            links = json.load(json_file)
            tasks = []
            total_timeout = aiohttp.ClientTimeout(total=60 * 5)
            connector = aiohttp.TCPConnector(limit=99)
            semaphore = asyncio.Semaphore(150)
            async with semaphore:
                async with aiohttp.ClientSession(connector=connector, timeout=total_timeout) as session:
                    do_it = True
                    while do_it:
                        try:
                            if entity_name == 'articles':
                                for article in links:
                                    tasks.append(asyncio.create_task(self.parse_entity(entity_name, article['link'], session)))
                            elif entity_name == 'questions':
                                for link in links:
                                    tasks.append(asyncio.create_task(self.parse_entity(entity_name, link, session)))
                            elif entity_name == 'consults':
                                for link in links:
                                    tasks.append(asyncio.create_task(self.parse_entity(entity_name, link, session)))
                            do_it = False
                            await asyncio.gather(*tasks)
                        except Exception as e:
                            with open(f'{(int(time.time() * 1000))}_islamweb_{entity_name}.json', 'w') as json_file:
                                json.dump(self.scraped_entities, json_file, ensure_ascii=False)
                            self.scraped_entities = []
                            print(e)
            if len(self.scraped_entities) > 0:
                with open(f'{(int(time.time() * 1000))}_islamweb_{entity_name}.json', 'w') as json_file:
                    json.dump(self.scraped_entities, json_file, ensure_ascii=False)
                self.scraped_entities = []

    async def parse_entity(self, entity_name, link, session):
        if entity_name == 'questions':
            await self.get_target_question(link, session)
        elif entity_name == 'articles':
            await self.get_target_article(link, session)
        elif entity_name == 'consults':
            await self.get_target_consult(link,session)

    async def get_target_question(self, link, session):
        url = f'{self.url}{link}'
        try:
            async with session.get(url) as r:
                if r.status != 200:
                    r.raise_for_status()
                website = await r.read()
                content = BeautifulSoup(website, 'lxml')
                try:
                    question = content.find_all('div',{'class':'mainitem'})[1].find('div').text
                    answer = content.find_all('div',{'class':'mainitem'})[2].find('div').text
                    qAa_dict = {"question": question, "answer": answer}
                    self.scraped_entities.append(qAa_dict)
                    print(self.counter, qAa_dict)
                    self.counter += 1
                except Exception as e:
                    print('no question found.', e)
                if len(self.scraped_entities) == self.chunk_length:
                    with open(f'{(int(time.time() * 1000))}_islamweb_questions.json', 'w') as json_file:
                        json.dump(self.scraped_entities, json_file, ensure_ascii=False)
                    self.scraped_entities = []
        except Exception as e:
            print(e)

    async def get_target_consult(self, link, session):
        url = f'{self.url}/ar/consult/{link}'
        try:
            async with session.get(url) as r:
                if r.status != 200:
                    r.raise_for_status()
                website = await r.read()
                content = BeautifulSoup(website, 'lxml')
                try:
                    question = content.find_all('div',{'class':'mainitem'})[1].find('div').text
                    answer = content.find_all('div',{'class':'mainitem'})[2].find('div').text
                    qAa_dict = {"question": question, "answer": answer}
                    self.scraped_entities.append(qAa_dict)
                    print(self.counter, qAa_dict)
                    self.counter += 1
                except Exception as e:
                    print('no question found.', e)
                if len(self.scraped_entities) == self.chunk_length:
                    with open(f'{(int(time.time() * 1000))}_islamweb_consult.json', 'w') as json_file:
                        json.dump(self.scraped_entities, json_file, ensure_ascii=False)
                    self.scraped_entities = []
        except Exception as e:
            print(e)

    async def get_target_article(self, link, session):
        url = f'{self.url}{link}'

        try:
            async with session.get(url) as r:
                if r.status != 200:
                    r.raise_for_status()
                try:
                    website = await r.read()
                    content = BeautifulSoup(website, 'lxml')

                    category = ''
                    sub_category = ''
                    title = ''
                    article_content = ''

                    try:
                        category = content.find('div',{'class':'portalheader'}).find_next('ol').find_all('li')[1].text
                    except:
                        print('error from category')
                    try:
                        sub_category = content.find('div', {'class': 'mainitemdetails'}).find_next('ul').find_all('li')[
                            2].find_next('a').text
                    except:
                        print('error from sub category')
                    try:
                        title = content.find('div', {'class': 'mainitem'}).find_next('h1').text
                    except:
                        print('error from title')
                    try:
                        article_content = content.find('div', {'class': 'articletxt'}).get_text(separator=' ').strip()
                    except:
                        print('error from category content')

                    new_article = {"category": category, "sub_category": sub_category, "title": title,
                                   "content": article_content}
                    print(self.counter, new_article)
                    self.counter += 1
                    self.scraped_entities.append(new_article)
                except Exception as e:
                    print('no article found.', e)
                if len(self.scraped_entities) == self.chunk_length:
                    with open(f'{(int(time.time() * 1000))}_islamweb_articles.json', 'w') as json_file:
                        json.dump(self.scraped_entities, json_file, ensure_ascii=False)
                    self.scraped_entities = []
        except Exception as e:
            print(e)

