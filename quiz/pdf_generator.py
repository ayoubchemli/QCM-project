import json
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, Flowable, KeepTogether
from reportlab.lib.units import inch, cm, mm
from reportlab.graphics.shapes import Drawing, Line, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import textwrap
from abc import ABC, abstractmethod

# Data Classes
@dataclass
class Subject:
    course: str
    chapter: str

@dataclass
class Score:
    subject: Subject
    points: float
    date: str

@dataclass
class User:
    fullname: str
    email: str
    scores: List[Score]

class GradientBackground(Flowable):
    def __init__(self, width: float, height: float, start_color: HexColor = HexColor('#3498db'), end_color: HexColor = HexColor('#2980b9')):
        super().__init__()
        self.width = width
        self.height = height
        self.start_color = start_color
        self.end_color = end_color

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        
        steps = 100
        for i in range(steps):
            ratio = i / steps
            color = Color(
                self.start_color.red + (self.end_color.red - self.start_color.red) * ratio,
                self.start_color.green + (self.end_color.green - self.start_color.green) * ratio,
                self.start_color.blue + (self.end_color.blue - self.start_color.blue) * ratio,
                alpha=0.9-i/150
            )
            canvas.setFillColor(color)
            canvas.rect(0, i*(self.height/steps), self.width, self.height/steps + 1, fill=True, stroke=False)
        
        canvas.setFillColor(HexColor('#ffffff'))
        canvas.setFillAlpha(0.05)
        for i in range(0, int(self.width), 20):
            for j in range(0, int(self.height), 20):
                canvas.circle(i, j, 1, fill=True)
                
        canvas.restoreState()

class SectionDivider(Flowable):
    def __init__(self, width):
        Flowable.__init__(self)
        self.width = width
        self.height = 30

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setStrokeColor(HexColor('#3498db'))
        canvas.setLineWidth(2)
        canvas.line(0, 15, self.width, 15)
        canvas.setFillColor(HexColor('#2980b9'))
        canvas.circle(self.width/2, 15, 5, fill=True)
        canvas.setFillColor(HexColor('#3498db'))
        canvas.circle(self.width/2 - 50, 15, 3, fill=True)
        canvas.circle(self.width/2 + 50, 15, 3, fill=True)
        canvas.restoreState()

class PDFStyleManager:
    @staticmethod
    def create_styles() -> Dict[str, ParagraphStyle]:
        styles = getSampleStyleSheet()
        
        styles.add(ParagraphStyle(
            name='CustomReportTitle',
            parent=styles['Title'],
            fontSize=32,
            spaceAfter=30,
            textColor=HexColor('#ffffff'),
            alignment=1,
            leading=36,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='CustomSectionHeader',
            fontSize=20,
            textColor=HexColor('#2c3e50'),
            spaceAfter=20,
            spaceBefore=30,
            bold=True,
            leading=24,
            borderRadius=8,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='CustomBodyText',
            fontSize=11,
            textColor=HexColor('#2c3e50'),
            spaceAfter=12,
            leading=16,
            alignment=0,
            fontName='Helvetica'
        ))
        
        styles.add(ParagraphStyle(
            name='TableCell',
            fontSize=9,
            leading=12,
            alignment=1,
            wordWrap='CJK',
            fontName='Helvetica'
        ))
        
        return styles

class PDFGenerator:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.styles = PDFStyleManager.create_styles()

    def generate_pdf(self, user: User) -> None:
        pdf_file = self.output_dir / f"{user.fullname.replace(' ', '_')}_report.pdf"
        
        doc = SimpleDocTemplate(
            str(pdf_file),
            pagesize=A4,
            rightMargin=30*mm,
            leftMargin=30*mm,
            topMargin=30*mm,
            bottomMargin=30*mm
        )
        
        story = []
        
        # Header with gradient
        story.append(GradientBackground(doc.width + 60*mm, 150))
        story.append(Spacer(1, 20))
        
        # Title section
        story.append(Paragraph("Academic Performance Report", self.styles['CustomReportTitle']))
        story.append(Paragraph(
            f"<para alignment='center'><font size='14' color='#ffffff'>{user.fullname}</font></para>",
            self.styles['CustomBodyText']
        ))
        story.append(Spacer(1, 50))
        
        if not user.scores:
            story.append(Paragraph("No scores available.", self.styles['CustomBodyText']))
        else:
            self._add_student_info(story, user, doc.width)
            self._add_performance_summary(story, user, doc.width)
            self._add_score_progression(story, user, doc.width)
            self._add_detailed_scores(story, user, doc.width)
            self._add_recommendations(story, user, doc.width)
            self._add_footer(story, doc.width)
        
        doc.build(story)
        print(f"Enhanced PDF report created: {pdf_file}")

    def _add_student_info(self, story: List[Flowable], user: User, doc_width: float) -> None:
        info_data = [
            ["Student Details", ""],
            ["Full Name:", user.fullname],
            ["Email:", user.email],
            ["Report Date:", datetime.now().strftime('%B %d, %Y')],
        ]
        
        info_table = Table(info_data, colWidths=[doc_width/4, doc_width/1.5])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#ecf0f1')),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(info_table)

    def _add_performance_summary(self, story: List[Flowable], user: User, doc_width: float) -> None:
        story.append(Paragraph("Performance Summary", self.styles['CustomSectionHeader']))
        
        # Calculate statistics
        scores = [score.points for score in user.scores]
        total_scores = len(scores)
        avg_score = sum(scores) / total_scores
        highest_score = max(scores)
        lowest_score = min(scores)
        
        summary_data = [
            ["Total Tests", "Average Score", "Highest Score", "Lowest Score"],
            [
                f"{total_scores}",
                f"{avg_score:.1f}%",
                f"{highest_score:.1f}%",
                f"{lowest_score:.1f}%"
            ]
        ]
        
        summary_table = Table(summary_data, colWidths=[doc_width/4]*4)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#ecf0f1')),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))

    def _add_score_progression(self, story: List[Flowable], user: User, doc_width: float) -> None:
        story.append(Paragraph("Score Progression", self.styles['CustomSectionHeader']))
        
        scores = [score.points for score in user.scores]
        drawing = Drawing(500, 200)
        chart = VerticalBarChart()
        
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 400
        chart.data = [scores]
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = 100
        chart.valueAxis.gridStrokeColor = HexColor('#ecf0f1')
        chart.bars[0].fillColor = HexColor('#3498db')
        chart.barWidth = 35
        chart.groupSpacing = 20
        chart.valueAxis.labels.fontSize = 8
        chart.categoryAxis.labels.fontSize = 8
        
        drawing.add(chart)
        story.append(drawing)
        story.append(Spacer(1, 20))

    def _add_detailed_scores(self, story: List[Flowable], user: User, doc_width: float) -> None:
        story.append(Paragraph("Detailed Score Analysis", self.styles['CustomSectionHeader']))
        
        table_style = self.styles['TableCell']
        headers = ["Subject", "Chapter", "Score", "Date & Time", "Performance Level"]
        data = [[Paragraph(header, table_style) for header in headers]]
        
        for score in user.scores:
            subject = Paragraph(score.subject.course, table_style)
            chapter = Paragraph(score.subject.chapter, table_style)
            points = Paragraph(f"{score.points:.1f}%", table_style)
            date = Paragraph(score.date, table_style)
            
            if score.points >= 90:
                level = "Excellent"
                level_color = '#27ae60'
            elif score.points >= 75:
                level = "Good"
                level_color = '#2980b9'
            elif score.points >= 60:
                level = "Satisfactory"
                level_color = '#f39c12'
            else:
                level = "Needs Improvement"
                level_color = '#c0392b'
                
            level_cell = Paragraph(f'<font color="{level_color}">{level}</font>', table_style)
            data.append([subject, chapter, points, date, level_cell])
        
        col_widths = [doc_width/4, doc_width/4, doc_width/8, doc_width/4, doc_width/6]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#ecf0f1')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, HexColor('#2c3e50')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), colors.white]),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(table)

    def _add_recommendations(self, story: List[Flowable], user: User, doc_width: float) -> None:
        story.append(Paragraph("Personalized Recommendations", self.styles['CustomSectionHeader']))
        
        scores = [score.points for score in user.scores]
        avg_score = sum(scores) / len(scores)
        
        if avg_score >= 90:
            recommendations = [
                "Continue your excellent performance by exploring advanced topics",
                "Consider mentoring peers in challenging subjects",
                "Explore additional learning resources to maintain your high standards"
            ]
        elif avg_score >= 75:
            recommendations = [
                "Focus on improving specific areas where scores were lower",
                "Develop a structured study plan for challenging topics",
                "Regular review of previous materials to maintain consistency"
            ]
        else:
            recommendations = [
                "Schedule regular review sessions for core concepts",
                "Seek additional help for challenging topics",
                "Focus on understanding fundamentals before advancing"
            ]
        
        rec_data = [[Paragraph(f"• {rec}", self.styles['CustomBodyText'])] for rec in recommendations]
        rec_table = Table(rec_data, colWidths=[doc_width - 50])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8f9fa')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#ecf0f1')),
        ]))
        story.append(rec_table)

    def _add_footer(self, story: List[Flowable], doc_width: float) -> None:
        story.append(Spacer(1, 30))
        story.append(SectionDivider(doc_width))
        
        footer_data = [
            [
                Paragraph(
                    f'''<para alignment="center">
                        <font size="8" color="#7f8c8d">Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}</font>
                    </para>''',
                    self.styles['CustomBodyText']
                )
            ],
            [
                Paragraph(
                    f'''<para alignment="center">
                        <font size="8" color="#7f8c8d">This report is automatically generated and is valid as of the date shown above.</font>
                    </para>''',
                    self.styles['CustomBodyText']
                )
            ],
            [
                Paragraph(
                    f'''<para alignment="center">
                        <font size="8" color="#7f8c8d">Academic Performance Report • Page 1 of 1</font>
                    </para>''',
                    self.styles['CustomBodyText']
                )
            ]
        ]
        
        footer_table = Table(footer_data, colWidths=[doc_width])
        footer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        story.append(footer_table)


def generate_pdf(user):
    # Set up paths
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / 'data'
    output_dir = current_dir / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Load data
    try:
        with open(data_dir / 'users.json', 'r') as f:
            users_data = json.load(f)
            
    except FileNotFoundError as e:
        print(f"Error: Could not find required data files in {data_dir}")
        print(f"Detailed error: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in data files")
        print(f"Detailed error: {e}")
        return
    
    # Initialize PDF generator
    pdf_generator = PDFGenerator(output_dir)
    
    # Generate reports
    print(user.username)
    # Generate reports
    for user_data in users_data:
        try:
          if user_data['username'] == user.username :
            # Convert scores data to proper format
            scores = []
            for score_data in user_data.get('scores', []):
                subject = Subject(
                    course=score_data['subject']['course'],
                    chapter=score_data['subject']['chapter']
                )
                score = Score(
                    subject=subject,
                    points=float(score_data['points']),
                    date=score_data['date']
                )
                scores.append(score)
            
            # Create user object
            user = User(
                fullname=user_data['fullname'],
                email=user_data['email'],
                scores=scores
            )
            
            # Generate PDF
            pdf_generator.generate_pdf(user)
            
        except KeyError as e:
            print(f"Error: Missing required field in user data: {e}")
            continue
        except ValueError as e:
            print(f"Error: Invalid data format: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error while processing user {user_data.get('fullname', 'Unknown')}: {e}")
            continue