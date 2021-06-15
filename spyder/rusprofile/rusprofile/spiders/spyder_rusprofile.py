import scrapy
from scrapy.http.request import Request
from rusprofile.items import RusprofileItem, remove_currency, remove_tags
from scrapy.loader import ItemLoader
import time



class CompanySpyder(scrapy.Spider):
    name = 'rusprofile_company'


    def start_requests(self):
        urls = [
            'https://www.rusprofile.ru/codes/89220',
            'https://www.rusprofile.ru/codes/429110'
        ]

        for url in urls:
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
#сбор ссылок 
        for link in response.css('div.company-item__title a::attr(href)'):
            yield response.follow('https://www.rusprofile.ru{}'.format(link.get()), callback=self.parse_company)


#поиск следующей страницы в разделе
        next_page = response.css('ul.paging-list li')
        if len(next_page):
            next_page = next_page[-1].css('a::attr(href)')
            yield response.follow('https://www.rusprofile.ru{}'.format(next_page.get()), callback=self.parse)




    def parse_company(self, response):
 
#html маркер обнаружения бота
        flag =  response.xpath('//div[@class="company-requisites"]/div[@class="company-row"][2]//dl[@class="company-col"][2]/dd[@class="company-info__text"]/span/text()').get()
        if flag:
            if len(remove_currency(flag))>= 10:
                print('--------возможно бот отбнаружен--------------')
#попытка понизить приоритет запроса, снятие фильтра на повторные запросы 
                yield Request(url=response.url, priority= -100, dont_filter=True)

#загрузщик модели     
        l = ItemLoader(item = RusprofileItem(), selector=response)

        l.add_css('name', 'div.company-header__row h1')
        l.add_css('ogrn', 'span#clip_ogrn')
        l.add_css('okpo', 'span#clip_okpo')
        l.add_css('company_status', 'div.company-status')
        l.add_xpath('registration_date', '//div[@class="company-requisites"]/div[@class="company-row"][2]//dd[@class="company-info__text"]')
        l.add_xpath('authorized_capital', '//div[@class="company-requisites"]/div[@class="company-row"][2]//dl[@class="company-col"][2]/dd[@class="company-info__text"]')
        

        yield l.load_item()



