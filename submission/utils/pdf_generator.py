# submission/utils/pdf_generator.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from django.utils import timezone
import json
from ..models import FormDataEntry

class PDFGenerator:
    def __init__(self, buffer, submission, version, user):
        self.buffer = buffer
        self.submission = submission
        self.version = version
        self.user = user
        self.canvas = canvas.Canvas(buffer, pagesize=letter)
        self.y = 750
        self.line_height = 20
        self.page_width = letter[0]
        self.left_margin = 100
        self.right_margin = 500
        self.min_y = 100

    def add_header(self):
        """Add header to the current page"""
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawString(self.left_margin, self.y, "intelligent Research Navigator (iRN) report")
        self.y -= self.line_height * 1.5
        
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawString(self.left_margin, self.y, f"{self.submission.title} - Version {self.version}")
        self.y -= self.line_height * 1.5
        
        self.canvas.setFont("Helvetica", 10)
        self.canvas.drawString(self.left_margin, self.y, f"Date of printing: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
        self.y -= self.line_height
        self.canvas.drawString(self.left_margin, self.y, f"Printed by: {self.user.get_full_name()}")
        self.y -= self.line_height * 2

    def add_footer(self):
        """Add footer to the current page"""
        footer_text = (
            "iRN is a property of the Artificial Intelligence and Data Innovation (AIDI) office "
            "in collaboration with the Office of Scientific Affairs (OSAR) office @ King Hussein "
            "Cancer Center, Amman - Jordan. Keep this document confidential."
        )
        
        self.canvas.setFont("Helvetica", 8)
        text_object = self.canvas.beginText()
        text_object.setTextOrigin(self.left_margin, 50)
        
        wrapped_text = simpleSplit(footer_text, "Helvetica", 8, self.right_margin - self.left_margin)
        for line in wrapped_text:
            text_object.textLine(line)
        
        self.canvas.drawText(text_object)

    def check_page_break(self):
        """Check if we need a new page and create one if necessary"""
        if self.y < self.min_y:
            self.add_footer()
            self.canvas.showPage()
            self.y = 750
            self.add_header()
            return True
        return False

    def write_wrapped_text(self, text, x_offset=0, bold=False):
        """Write text with word wrapping"""
        if bold:
            self.canvas.setFont("Helvetica-Bold", 10)
        else:
            self.canvas.setFont("Helvetica", 10)
            
        wrapped_text = simpleSplit(str(text), "Helvetica", 10, self.right_margin - (self.left_margin + x_offset))
        for line in wrapped_text:
            self.check_page_break()
            self.canvas.drawString(self.left_margin + x_offset, self.y, line)
            self.y -= self.line_height

    def add_section_header(self, text):
        """Add a section header"""
        self.check_page_break()
        self.y -= self.line_height
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(self.left_margin, self.y, text)
        self.y -= self.line_height

    def add_basic_info(self):
        """Add basic submission information"""
        self.add_section_header("Basic Information")
        
        basic_info = [
            f"Submission ID: {self.submission.temporary_id}",
            f"Study Type: {self.submission.study_type}",
            f"IRB Number: {self.submission.irb_number or 'Not provided'}",
            f"Status: {self.submission.get_status_display()}",
            f"Date Created: {self.submission.date_created.strftime('%Y-%m-%d')}",
            f"Date Submitted: {self.submission.date_submitted.strftime('%Y-%m-%d') if self.submission.date_submitted else 'Not submitted'}",
        ]

        for info in basic_info:
            self.write_wrapped_text(info)

    def add_research_team(self):
        """Add research team information"""
        self.add_section_header("Research Team")
        
        # Primary Investigator
        self.write_wrapped_text(f"Primary Investigator: {self.submission.primary_investigator.get_full_name()}")
        
        # Co-Investigators
        coinvestigators = self.submission.coinvestigators.all()
        if coinvestigators:
            self.y -= self.line_height/2
            self.write_wrapped_text("Co-Investigators:")
            for ci in coinvestigators:
                self.write_wrapped_text(f"- {ci.user.get_full_name()} (Role: {ci.role_in_study})", x_offset=20)

        # Research Assistants
        research_assistants = self.submission.research_assistants.all()
        if research_assistants:
            self.y -= self.line_height/2
            self.write_wrapped_text("Research Assistants:")
            for ra in research_assistants:
                self.write_wrapped_text(f"- {ra.user.get_full_name()}", x_offset=20)

    def format_field_value(self, value):
        """Format field value, handling special cases like JSON arrays"""
        if isinstance(value, str) and value.startswith('['):
            try:
                value_list = json.loads(value)
                return ", ".join(str(v) for v in value_list)
            except json.JSONDecodeError:
                return value
        return str(value)

    def add_dynamic_forms(self):
        """Add dynamic form data"""
        for dynamic_form in self.submission.study_type.forms.all():
            self.add_section_header(dynamic_form.name)
            
            field_definitions = {
                field.name: field.displayed_name 
                for field in dynamic_form.fields.all()
            }
            
            form_entries = FormDataEntry.objects.filter(
                submission=self.submission,
                form=dynamic_form,
                version=self.version
            )
            
            for entry in form_entries:
                displayed_name = field_definitions.get(entry.field_name, entry.field_name)
                formatted_value = self.format_field_value(entry.value)
                self.write_wrapped_text(f"{displayed_name}:", bold=True)
                self.write_wrapped_text(formatted_value, x_offset=20)

    def add_documents(self):
        """Add attached documents list"""
        self.add_section_header("Attached Documents")
        
        documents = self.submission.documents.all()
        if documents:
            for doc in documents:
                self.write_wrapped_text(
                    f"- {doc.file.name.split('/')[-1]} (Uploaded by: {doc.uploaded_by.get_full_name()})"
                )
        else:
            self.write_wrapped_text("No documents attached")

    def generate(self):
        """Generate the complete PDF"""
        self.add_header()
        self.add_basic_info()
        self.add_research_team()
        self.add_dynamic_forms()
        self.add_documents()
        self.add_footer()
        self.canvas.save()