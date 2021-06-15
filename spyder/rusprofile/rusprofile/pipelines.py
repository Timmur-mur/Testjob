from rusprofile.model import Rusprofile
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from rusprofile.model import Rusprofile
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

#класс записи данных в базу 
class DatabsePipeline:

    def __init__(self, db_url):
        self.db_url = db_url
        self.engin = create_engine(self.db_url)

#получение переменной коннекта с базой через settings
    @classmethod
    def from_crawler(cls, crawler):
        print(crawler.settings.get('DB_URI'))
        return cls(
            db_url=crawler.settings.get('DB_URI')
        )
#открытие сесии связи с базой при запуске паука
    def open_spider(self, spider):
        self.session = Session(bind=self.engin)

#сохранение данных в бае закрытие сессии
    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

#добавление нового item в сессию
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        company = Rusprofile(
            org_name = adapter.get('name'),
            ogrn = adapter.get('ogrn'),
            okpo = adapter.get('okpo'),
            status = adapter.get('company_status'),
            registration_date = adapter.get('registration_date'),
            capital = adapter.get('authorized_capital')
        )
        self.session.add(company)   
        return item