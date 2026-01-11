from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import datetime

class NotesFormatter:
    @staticmethod
    def format_markdown(content, examples, quiz_data=None):
        """Format content as markdown"""
        formatted = f"# Study Material\n\n"
        formatted += f"## Explanation\n\n{content}\n\n"
        formatted += f"## Examples\n\n{examples}\n\n"
        
        if quiz_data:
            formatted += "## Quiz Questions\n\n"
            for i, q in enumerate(quiz_data, 1):
                formatted += f"**Q{i}: {q['question']}**\n\n"
                for j, opt in enumerate(q['options'], 1):
                    formatted += f"{j}. {opt}\n"
                formatted += f"\n*Correct Answer: {q['correct'] + 1}*\n"
                formatted += f"*Explanation: {q.get('explanation', 'N/A')}*\n\n"
        
        return formatted
    
    @staticmethod
    def export_to_pdf(topic, level, content, examples, quiz_data, filename):
        """Export study material to PDF"""
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#2C3E50',
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor='#34495E',
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Title
            story.append(Paragraph("AI Study Material Generator", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Topic and Level
            story.append(Paragraph(f"<b>Topic:</b> {topic}", styles['Normal']))
            story.append(Paragraph(f"<b>Difficulty Level:</b> {level}", styles['Normal']))
            story.append(Paragraph(f"<b>Generated:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Content
            story.append(Paragraph("Explanation", heading_style))
            for para in content.split('\n\n'):
                if para.strip():
                    story.append(Paragraph(para.replace('\n', '<br/>'), styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))
            
            story.append(Spacer(1, 0.2*inch))
            
            # Examples
            story.append(Paragraph("Real-World Examples", heading_style))
            for para in examples.split('\n\n'):
                if para.strip():
                    story.append(Paragraph(para.replace('\n', '<br/>'), styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))
            
            # Quiz
            if quiz_data:
                story.append(PageBreak())
                story.append(Paragraph("Quiz Questions", heading_style))
                
                for i, q in enumerate(quiz_data, 1):
                    story.append(Paragraph(f"<b>Question {i}:</b> {q['question']}", styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))
                    
                    for j, opt in enumerate(q['options'], 1):
                        story.append(Paragraph(f"   {j}. {opt}", styles['Normal']))
                    
                    story.append(Spacer(1, 0.05*inch))
                    story.append(Paragraph(f"<i>Correct Answer: Option {q['correct'] + 1}</i>", styles['Normal']))
                    story.append(Paragraph(f"<i>Explanation: {q.get('explanation', 'N/A')}</i>", styles['Normal']))
                    story.append(Spacer(1, 0.2*inch))
            
            doc.build(story)
            return True
        except Exception as e:
            print(f"PDF generation error: {e}")
            return False