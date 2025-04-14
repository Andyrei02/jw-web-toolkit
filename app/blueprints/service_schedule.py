from flask import current_app, Blueprint, render_template, request, jsonify, send_file
import json
from io import BytesIO
from app.utils.generator_workbook import Service_Workbook_PDF_Generator
from app.models import WorkbooksList, Workbook


service_schedule_bp = Blueprint("service_schedule", __name__)

@service_schedule_bp.route("/service_schedule")
def service_schedule():
    workbooks = WorkbooksList.query.all()
    return render_template("service_schedule/service_schedule.html", workbooks=workbooks)    


@service_schedule_bp.route("/generate_service_schedule_pdf", methods=["POST"])
def generate_service_schedule_pdf():
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

