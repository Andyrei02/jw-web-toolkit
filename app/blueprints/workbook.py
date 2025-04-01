from flask import current_app, Blueprint, render_template, request, jsonify, send_file
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
    
    data_json = json.dumps(workbook_data.data, ensure_ascii=False) if workbook_data else "{}"

    return render_template(
        "workbook/complete_workbook.html", 
        workbook=workbook, 
        data=workbook_data.data if workbook_data else {},
        data_json=data_json,
    )
    


@workbooks_bp.route("/generate_workbook_pdf", methods=["POST"])
def generate_workbook_pdf():
    print("generate_workbook_pdf called")
    try:
        template_path = current_app.root_path + "/templates"
        static_path = current_app.root_path + "/static/css"

        generator = Service_Workbook_PDF_Generator(template_dir=template_path, css_path=static_path)
        data = request.get_json()  # Receive JSON data
        pdf_content = generator.generate_pdf(data)
        pdf_io = BytesIO(pdf_content)
        
        return send_file(pdf_io, mimetype="application/pdf", as_attachment=True, download_name="workbook.pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

