from flask import Blueprint, render_template
from app.models import Workbook

workbook_bp = Blueprint("workbook", __name__)

@workbook_bp.route("/workbook")
def home():
    workbooks = Workbook.query.all()
    for w in workbooks:
        print(w.title, w.link, w.img)

    return render_template("workbook/workbook.html", workbooks=workbooks)
