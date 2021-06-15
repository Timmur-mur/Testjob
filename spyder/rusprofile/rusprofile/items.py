import scrapy
from scrapy.item import Field
import datetime 
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

#функции очистки данных
def remove_currency(value):
    value = value.replace('руб.', '').strip().replace(' ', '')
    return value 

def delete_empty_lines(value):
    return value.strip()

#модель собираемых данных

class RusprofileItem(scrapy.Item):
    name = Field(input_processor = MapCompose(remove_tags, delete_empty_lines), output_processor = TakeFirst())
    ogrn = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    okpo = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    company_status = Field(input_processor = MapCompose(remove_tags, delete_empty_lines), output_processor = TakeFirst())
    registration_date = Field(input_processor = MapCompose(remove_tags, delete_empty_lines), output_processor = TakeFirst())
    authorized_capital = Field(input_processor = MapCompose(remove_tags, remove_currency), output_processor = TakeFirst())