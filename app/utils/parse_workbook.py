import asyncio
from flask import current_app

from app.extensions import db
from app.models import WorkbooksList
from app.models import Workbook
from app.utils.parsers import Parse_List_Meeting_WorkBooks, Parse_Meeting_WorkBook
from app.config import Config


def get_list_workbooks():
    current_app.logger.info("Parse workbook list.")
    parser = Parse_List_Meeting_WorkBooks(Config.jw_domain, Config.workbooks_url)
    return asyncio.run(parser.get_dict_data())

def get_workbook_data(title, link):
    current_app.logger.info(f"Parse data from workbok {title}")
    parser = Parse_Meeting_WorkBook(Config.jw_domain)
    return asyncio.run(parser.get_dict_data(link))

def commit_to_db(workbooks_list):
    current_app.logger.info("Commit workbook list to database.")
    try:
        for title, data in workbooks_list.items():
            if not isinstance(data, list) or len(data) < 2:
                current_app.logger.warning(f"Skipping invalid data for {title}: {data}")
                continue  # Skip if the structure is incorrect

            link, img = data  # Extract link and image from list

            # Check if the workbook already exists
            existing = WorkbooksList.query.filter_by(link=link).first()
            if existing:
                current_app.logger.info(f"Workbook {title} already exists in the database.")
                continue  # Skip if it already exists

            wb_data_dict = get_workbook_data(title, link)
            if not isinstance(wb_data_dict, dict):
                current_app.logger.warning(f"Skipping {title}: Invalid workbook data received.")
                continue  # Skip if data is not a valid dictionary
            
            # Create and save new workbook entry
            new_wb = WorkbooksList(title=title, link=link, img=img)
            new_wb_data = Workbook(title=title, data=wb_data_dict)
            
            db.session.add(new_wb)
            db.session.add(new_wb_data)

        db.session.commit()
        current_app.logger.info("Workbooks successfully added to database.")
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error committing workbooks to database: {e}")


def parse_workbook_list():
    workbooks_list = get_list_workbooks()
    commit_to_db(workbooks_list)


if __name__ == '__main__':
    parse_workbook_list()
