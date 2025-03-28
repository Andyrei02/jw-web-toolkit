import os
import copy

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
    def __init__(self, template_dir='templates'):
        self.schedule = MeetingSchedule("18:00")
        
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = "template.html"
        self.css_path = os.path.join(template_dir, 'styles.css')
        
    def generate_pdf(self, data):
        template = self.env.get_template(self.template)
        processed_data = self.schedule.calculate_times(data)
        
        html_content = template.render(schedule=processed_data, css_path=self.css_path)
        pdf_io = BytesIO()
                    
        # Generate PDF
        HTML(string=html_content, base_url=".").write_pdf(pdf_io)
        
        pdf_io.seek(0)
        
        return pdf_io.getvalue()


if __name__ == '__main__':
    output_pdf = "output.pdf"
    generator = Service_Workbook_PDF_Generator()
    generator.generate_pdf(data, output_pdf=output_pdf)