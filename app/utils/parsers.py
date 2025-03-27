import logging

import aiohttp
import asyncio
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Parse_List_Meeting_WorkBooks:
    def __init__(self, domain, url, headers=None):
        super().__init__()
        self.domain = domain
        self.site_url = url
        self.headers = headers or {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",}

    async def fetch(self, session, url):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()

    async def get_site_page(self, session, url):
        html = await self.fetch(session, url)
        return BeautifulSoup(html, "lxml")

    async def get_article(self, soup):
        article = soup.find("article", {"id": "article"})
        return article

    async def get_synopsis_list(self, soup):
        section = soup.find("div", {"id": "pubsViewResults"})
        divs = section.find_all("div", {"class": "synopsis"})
        return divs

    async def get_syn_img(self, div):
        syn_img = div.find("div", {"class": "syn-img"})
        img = syn_img.find("span")['data-img-size-md']
        return img

    async def get_syn_body(self, div):
        syn_body = div.find("div", {"class": "syn-body"})
        pub_desc = syn_body.find("div", {"class": "publicationDesc"})
        title = pub_desc.find("h3").text
        link = pub_desc.find("a")['href']
        return [title.strip(), link]

    async def get_dict_data(self):
        data_dict = {}
        logging.info(f"Parse Workbook list: {self.site_url}\n")
        async with aiohttp.ClientSession() as session:
            soup = await self.get_site_page(session, self.site_url)
            syn_list = await self.get_synopsis_list(soup)

            for publication in syn_list:
                try:
                    syn_img_link = await self.get_syn_img(publication)
                    title, link = await self.get_syn_body(publication)

                    data_dict[title] = [self.domain+link, syn_img_link]
                except:
                    pass
        logging.info(f"Successfully Parsed Workbook list: {self.site_url}\n")
        
        return data_dict


from datetime import datetime
import re


class Parse_Meeting_WorkBook():
    def __init__(self, domain):
        super().__init__()
        self.domain = domain
        self.site_url = ''

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_site_page(self, session, url):
        html = await self.fetch(session, url)
        return BeautifulSoup(html, "lxml")

    async def get_article(self, soup):
        article = soup.find("article", {"id": "article"})
        return article

    async def get_synopsis_list(self, soup):
        synoplis_list = soup.find_all("div", {"class": "syn-body sqs"})
        return synoplis_list

    async def get_date_and_link_list(self, soup):
        date_link_list = []
        for synopsis in soup:
            date_link_list.append([(synopsis.find("a").text).strip(), synopsis.find("a")['href']])
        return date_link_list

    async def get_pages_list(self, session):
        soup = await self.get_site_page(session, self.site_url)
        soup_article = await self.get_article(soup)
        synopsis_list = await self.get_synopsis_list(soup_article)
        date_link_list = await self.get_date_and_link_list(synopsis_list)
        return date_link_list

    async def get_article_header(self, soup):
        header = soup.find("header")
        header_title = header.find("h1", {"id": "p1"})
        header_verses = header.find("h2", {"id": "p2"})
        return [header_title.text.strip(), header_verses.text.strip()]

    async def get_section_list(self, soup):
        body = soup.find("div", {"class": "bodyTxt"})

        # Section 1
        # section 1 Text
        section_1_text = body.find("div", {"class": "dc-icon--gem"})
        # items
        s1_items = body.find_all("h3", {"class": "du-color--teal-700"}, recursive=True)
        s1_items = [i.text for i in s1_items]

        # Section 2
        section_2_text = body.find("div", {"class": "dc-icon--wheat"})
        # items
        s2_items = body.find_all("h3", {"class": "du-color--gold-700"})
        s2_items = [i.text for i in s2_items]

        # Section 3
        section_3_text = body.find("div", {"class": "dc-icon--sheep"})
        # items
        s3_items = body.find_all("h3", {"class": "du-color--maroon-600"})
        s3_items = [i.text for i in  s3_items]

        return body

    async def increment_id(self, id_value):
        match = re.match(r'\D*(\d+)', id_value)

        if match:
            numeric_part = int(match.group(1))
            modified_id = f'p{numeric_part + 1}'
            return modified_id
        else:
            return None

    async def get_section_data(self, soup, section_class, item_class):
        section_text = soup.find("div", {"class": section_class}).text
        items = soup.find_all("h3", {"class": item_class})
        row_list = []
        for item in items:
            current_id = item.get('id')
            hour = soup.find('p', {'id': await self.increment_id(current_id)})
            hour = await self.find_time_from_p_tag(hour)
            row_list.append([str(hour), item.text.strip()])
        return row_list

    async def get_data_list_section_1(self, soup):
        # return await self.get_section_data(soup, "dc-icon--gem", "du-color--teal-700")
        dc_music = soup.find("h3", {"class": "dc-icon--music"})
        dc_music = dc_music.text.split('|')
        intro_text = dc_music[1].strip()
        time = await self.find_time_from_p_tag(intro_text)
        pattern = r'\(\d+\xa0min\.\)'
        format_intro = re.sub(pattern, '', intro_text)
        row_list = [["5", dc_music[0].strip()], [str(time), format_intro]]
        return row_list

    async def get_data_list_section_2(self, soup):
        return await self.get_section_data(soup, "dc-icon--gem", "du-color--teal-700")

    async def get_data_list_section_3(self, soup):
        return await self.get_section_data(soup, "dc-icon--wheat", "du-color--gold-700")

    async def get_data_list_section_4(self, soup, music_list):
        dc_music = soup.find_all("h3", {"class": "dc-icon--music"})
        dc_music.append(soup.find("span", {"class": "dc-icon--music"}))

        section_3_text = soup.find("div", {"class": "dc-icon--sheep"})
        title = section_3_text.text
        # items
        s3_items = soup.find_all("h3", {"class": "du-color--maroon-600"})
        row_list = []
        row_list.append(["5", music_list[1]])
        for i in s3_items:
            current_id = i.get('id')
            hour = soup.find('p', {'id': await self.increment_id(current_id)})
            hour = await self.find_time_from_p_tag(hour)
            text = re.match(r'^\d+\.\s.*$', i.text.strip())
            if text:
                row_list.append([str(hour), text.group()])

        row_list.append(["5", "Cuvinte de încheiere"])
        row_list.append(["5", music_list[2]])
        return row_list

    async def find_time_from_p_tag(self, text):
        if type(text) != str:
            text = text.get_text()
        match = re.search(r'\((\d+)\s+min\.\)', text)
        if match:
            time_str = match.group(1)
            return int(time_str)
        return 0

    async def download_page(self, session, page):
        url = self.domain + page[1]
        logging.info(f"Downloading page: {url}\n")
        try:
            soup = await self.get_site_page(session, url)
            soup_article = await self.get_article(soup)
            body = await self.get_section_list(soup_article)
            date, header = await self.get_article_header(soup_article)

            dc_music = body.find_all(class_="dc-icon--music")
            music_list = []
            for i in dc_music:
                music = i.find("a")
                if music:
                    music_list.append(music.text.strip())
                else:
                    music_list.append(i.text.strip())
            
            intro = {}
            for item in await self.get_data_list_section_1(body):
                intro[item[1]] = [item[0], '']

            section_1 = {}
            for item in await self.get_data_list_section_2(body):
                section_1[item[1]] = [item[0], '']

            section_2 = {}
            for item in await self.get_data_list_section_3(body):
                section_2[item[1]] = [item[0], '']

            section_3 = {}
            for item in await self.get_data_list_section_4(body, music_list):
                section_3[item[1]] = [item[0], '']

            logging.info(f"Successfully downloaded page: {url}\n")
        except Exception as e:
            logging.error(f"Error downloading page {url}: {e}\n")
            raise

        return date, {"header": {header: [0, '']}, "intro": intro, "section_1": section_1, "section_2": section_2, "section_3": section_3}

    async def sort_dict_by_dates(self, date_dict):
        def convert_month_to_number(month_word):
            month_mapping = {
                'ianuarie': '01',
                'februarie': '02',
                'martie': '03',
                'aprilie': '04',
                'mai': '05',
                'iunie': '06',
                'iulie': '07',
                'august': '08',
                'septembrie': '09',
                'octombrie': '10',
                'noiembrie': '11',
                'decembrie': '12'
            }
            return month_mapping.get(month_word, '00')

        def custom_sort(date_str):
            date_parts = date_str.split(' ')
            day, month_word = date_parts[:2]
            day = day.split('-')[0]
            month = convert_month_to_number(month_word)
            return datetime.strptime(f'{day}.{month}', '%d.%m').date()

        sorted_items = dict(sorted(date_dict.items(), key=lambda item: custom_sort(item[0])))
        return sorted_items
        
    async def get_dict_data(self, url):
        self.site_url = url
        
        async with aiohttp.ClientSession() as session:
            page_list = await self.get_pages_list(session)
            total_pages = len(page_list)
            downloaded_pages = 0
            data_dict = {}

            async def download_and_process_page(page):
                try:
                    date, page_data = await self.download_page(session, page)
                    data_dict[date] = page_data
                except Exception as e:
                    logging.error(f"Error downloading page: {page}: {e}\n")
                finally:
                    nonlocal downloaded_pages
                    downloaded_pages += 1
                    downloaded_progress = int((downloaded_pages / total_pages) * 100)

            tasks = [download_and_process_page(page) for page in page_list]
            await asyncio.gather(*tasks)

            return await self.sort_dict_by_dates(data_dict)



if __name__ == '__main__':
    domain = 'https://www.jw.org'
    
    url = "https://www.jw.org/ro/biblioteca/caiet-pentru-intrunire/?contentLanguageFilter=ro&pubFilter=mwb&yearFilter="
    parser_list = Parse_List_Meeting_WorkBooks(domain, url)
    data = asyncio.run(parser_list.get_dict_data())
    print(data)
    
    parse_workbook = Parse_Meeting_WorkBook(domain)
    
    for title, data in data.items():
        print(asyncio.run(parse_workbook.get_dict_data(data[0])))
        
