from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.sqltypes import Float


Base = declarative_base()

# модель таблицы в базе данных

class Rusprofile(Base):
	__tablename__ = 'rusprofile_extracted_data'

	company_id = Column(Integer, primary_key=True)
	org_name = Column(String(700))
	ogrn = Column(String)
	okpo = Column(String)
	status = Column(String(300))
	registration_date = Column(Date)
	capital = Column(Float)

