from app import create_app
from app.utils.parse_workbook import parse_workbook_list


app = create_app()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)