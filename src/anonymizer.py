import io
import PyPDF2
from typing import Tuple, List
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class PDFAnonymizer:
    @staticmethod
    def extract_text(pdf_file) -> str:
        """Extract text content from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")

    @staticmethod
    def create_anonymized_pdf(text: str) -> bytes:
        """Create a new PDF with anonymized text"""
        try:
            # Create a buffer for the PDF
            buffer = io.BytesIO()

            # Create the PDF with reportlab
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            # Write text to PDF
            y = height - 40  # Start 40 points down from top
            for line in text.split('\n'):
                if y > 40:  # Stop if we get too close to bottom margin
                    c.drawString(40, y, line)
                    y -= 15  # Move 15 points down
                else:
                    # Add new page if needed
                    c.showPage()
                    y = height - 40
                    c.drawString(40, y, line)
                    y -= 15

            c.save()
            buffer.seek(0)
            return buffer.getvalue()

        except Exception as e:
            raise Exception(f"Error creating anonymized PDF: {str(e)}")