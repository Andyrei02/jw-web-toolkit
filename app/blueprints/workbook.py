from flask import current_app, Blueprint, render_template, request, jsonify, send_file
import json
from io import BytesIO
from app.utils.generator_workbook import Service_Workbook_PDF_Generator
from app.utils.email_sender import send_email_with_pdf
from app.models import WorkbooksList, Workbook
from app.config import Config


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
    try:
        template_path = current_app.root_path + "/templates"
        static_path = current_app.root_path + "/static/css"
        bg = None

        data = request.get_json()
        bg = data["background"]
        data.pop("background", None)
        
        email_list = data["email_list"]
        data.pop("email_list", None)
        
        generator = Service_Workbook_PDF_Generator(bg, template_dir=template_path, css_path=static_path)
        pdf_content = generator.generate_pdf(data)
        pdf_io = BytesIO(pdf_content)
        
        sender_email = Config.admin_email
        sender_password = Config.admin_email_pass
        email_subject = "Caiet pentru intrunire"
        email_body = "Luna ..."
        if email_list:
            for email in email_list:
                send_email_with_pdf(
                    sender_email=sender_email,
                    sender_password=sender_password,
                    recipient_email=email,
                    subject=email_subject,
                    body=email_body,
                    pdf_data=pdf_content,
                    filename="Workbook.pdf"
                )
                
        return send_file(pdf_io, mimetype="application/pdf", as_attachment=True, download_name="workbook.pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
