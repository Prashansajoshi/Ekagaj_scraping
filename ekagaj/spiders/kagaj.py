import scrapy
import re
import json
from datetime import datetime, timedelta
from config import categories ,start_date_str,end_date_str, convert_to_english
class eKagaj(scrapy.Spider):
    name = "eKagaj"
    page_number = 2
    #start_urls = ['https://ekagaj.com/']
    allowed_domain = ["ekagaj.com"]


    # # Convert start_date_str and end_date_str to datetime objects
    # start_date = datetime.strptime(start_date_str, date_format)
    # end_date = datetime.strptime(end_date_str, date_format)
    # current_date = start_date

     # read the data file
    try:
        with open('news1.json', 'r', encoding='utf-8') as file:
            ekagaj_data_list = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        ekagaj_data_list = []


    def start_requests(self):
        for indv_category in categories:
            yield scrapy.Request(f"https://ekagaj.com/category/{indv_category}", callback=self.parse, meta={'news_cat': indv_category})


    # helper function: extracts date using regex
    def parse_date(self,text):
        pattern = re.compile(r'(\S+)\s([०-९]+),\s([०-९]+)\b')
        match = re.search(pattern, text)
        if match:
                day_of_week = match.group(1)
                day = match.group(2)
                year = match.group(3)
                return match.group(0)
        else:
                return None


    def parse(self, response):
            # print(response.text)
            print('%%%%%')
            links = response.css('a::attr(href)')
            pattern = re.compile(
            r'/article/(society|party|politics|environment|infrastructure|tourism|finance|corporate|crime|world|cricket|parliament|health)/\.*')
            next = response.css("li.next a::attr(href)").get()

            print('$$$$$')
            for indv_link in links:
                href = indv_link.get()
                
                pattern = r'/article/(tourism|finance|party|corporate|crime|world|cricket|society|parliament|infrastructure|politics|environment|health)/\d+/'

                # Check if the link matches the article pattern
                match = re.search(pattern, href)
                if match:
                    captured_href = match.group()
                    # print(captured_href)
                    yield response.follow(f"{captured_href}", callback=self.parse_news, meta={'link' : captured_href, 'news_cat': response.meta['news_cat']})

            
            #Pagination Logic
            next_page = f'https://ekagaj.com/category/{response.meta["news_cat"]}/' 
            if next is not None:
                    yield response.follow(next_page+next, callback=self.parse, meta={'news_cat': response.meta['news_cat']})


    def parse_news(self,response):
                print("###")
                details = []
                news_link = response.meta['link']
                title = response.css('header.pb-25 h1::text').get()
                author_name = response.css('span.authorname a::text').get()
                paragraph = response.css('p::text').extract()
                image = response.css('figure a img::attr(src)').get()
                date = response.css('.detail .time::text').get()
                print("%%%%%%")

                
                for indv_p in paragraph:
                    details.append(indv_p)

                #if self.start_date <= parsed_date <=  self.end_date:
                #if self.current_date <= self.end_date:
                    yield {
                        "TITLE": title,
                        "author": author_name,
                        "paragraph" : paragraph,
                        "image" : image,
                        "date" : self.parse_date(date),
                        "link": news_link,
                        "category": response.meta["news_cat"],
                        "english_date":convert_to_english(self.parse_date(date))
                    }
                    
               

                
   
                 