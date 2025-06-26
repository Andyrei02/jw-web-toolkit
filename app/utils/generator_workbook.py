import os
import copy
import json 

import pikepdf

from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from io import BytesIO


class MeetingSchedule:
    def __init__(self, start_time):
        self.start_time = datetime.strptime(start_time, "%H:%M")

    def calculate_times(self, data):
        data_copy = copy.deepcopy(data)

        for header_date, sections in data_copy.items():
            current_time = self.start_time
            for section, items in sections.items():
                for item, item_data in items.items():
                    try:
                        next_time = int(item_data[0])
                    except:
                        print(f"Invalid time format: {item_data[0]}")
                    item_data[0] = current_time.strftime("%H:%M")
                    current_time = current_time + timedelta(minutes=next_time)
        return data_copy


class Service_Workbook_PDF_Generator:
    def __init__(self, bg=None, template_dir='templates', css_path=None):
        self.schedule = MeetingSchedule("18:00")
        self.bg = bg
        
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = "template.html"
        self.css_path = os.path.join(css_path, 'template_style.css')
    
    def embed_json_metadata(self, pdf_bytes, json_data):
        # Load PDF from bytes
        pdf = pikepdf.Pdf.open(BytesIO(pdf_bytes))

        # Convert dictionary to string
        json_str = json.dumps(json_data, ensure_ascii=False)

        # Add custom metadata
        pdf.docinfo["/WorkbookData"] = json_str

        # Save to BytesIO
        output = BytesIO()
        pdf.save(output)
        output.seek(0)
        return output.getvalue()

    def generate_pdf(self, data):
        template = self.env.get_template(self.template)
        processed_data = self.schedule.calculate_times(data)
        
        html_content = template.render(schedule=processed_data, css_path=self.css_path, bg=self.bg)
        pdf_io = BytesIO()
                    
        # Generate PDF
        HTML(string=html_content, base_url=".").write_pdf(pdf_io)
        
        pdf_io.seek(0)
        
        return self.embed_json_metadata(pdf_io.getvalue(), data)


def extract_json_metadata(file_storage):
    try:
        with pikepdf.open(file_storage.stream) as pdf:
            metadata = pdf.docinfo
            if "/WorkbookData" in metadata:
                json_raw = metadata["/WorkbookData"]
                return json.loads(str(json_raw))
    except Exception as e:
        print("Metadata extraction error:", e)
    return None