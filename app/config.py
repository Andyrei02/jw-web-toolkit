import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    jw_domain = 'https://www.jw.org'
    workbooks_url = "https://www.jw.org/ro/biblioteca/caiet-pentru-intrunire/?contentLanguageFilter=ro&pubFilter=mwb&yearFilter="
