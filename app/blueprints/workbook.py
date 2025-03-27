from flask import Blueprint, render_template
from app.models import WorkbooksList

workbooks_bp = Blueprint("workbooks", __name__)

@workbooks_bp.route("/workbooks")
def home():
    workbooks = WorkbooksList.query.all()

    return render_template("workbook/workbook.html", workbooks=workbooks)
