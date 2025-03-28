from flask import Blueprint, render_template, request, jsonify, send_file
import json
from io import BytesIO
from app.utils.generator_workbook import Service_Workbook_PDF_Generator
from app.models import WorkbooksList, Workbook


workbooks_bp = Blueprint("workbooks", __name__)

@workbooks_bp.route("/workbooks")
def workbooks():
    workbooks = WorkbooksList.query.all()
    return render_template("workbook/workbook.html", workbooks=workbooks)


@workbooks_bp.route("/complete_workbook/<path:link>")
def complete_workbook(link):
    # Retrieve the workbook data based on the link
    workbook = WorkbooksList.query.filter_by(link=link).first()
    if not workbook:
        return "Workbook not found", 404

    workbook_data = Workbook.query.filter_by(title=workbook.title).first()
    
    return render_template(
        "workbook/complete_workbook.html", 
        workbook=workbook, 
        data=workbook_data.data if workbook_data else {}
    )


@workbooks_bp.route("/generate_workbook_pdf", methods=["POST"])
def generate_workbook_pdf():
    print("generate")
    try:
        output_pdf = "output.pdf"
        generator = Service_Workbook_PDF_Generator()
        data = request.get_json()  # Receive JSON data
        generator.generate_pdf(data, output_pdf=output_pdf)
        pdf_content = generator_workbook(data)  # Convert modified data into a PDF
        pdf_io = BytesIO(pdf_content)
        
        return send_file(pdf_io, mimetype="application/pdf", as_attachment=True, download_name="workbook.pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

