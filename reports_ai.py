import subprocess
import openai
import pyfiglet
import rich
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import re
from reportlab.platypus import Spacer, Image
from urllib.parse import urlparse
import datetime

title = pyfiglet.figlet_format('AI', font='isometric2')
rich.print(f'[yellow]{title}[/yellow]')

api_key = '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'

def chat_with_gpt(prompt):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()


url = str(input("Enter the target url : "))
vaa = str(input("Enter the name of the Vulnerability : "))
dis = str(input("Enter Description of the Vulnerability : "))

# استخراج الدومين
parsed_url = urlparse(url)
if parsed_url.netloc != "":
    url = parsed_url.netloc
domain_parts= url.split('.')
top_level_domain = domain_parts[-1]

url_r = url

if len(domain_parts) > 2:
    d_url = len(domain_parts) - 2
    urla = f"{domain_parts[d_url]}.{top_level_domain}"
    url_r = urla

question = f'''
Help me just write the bugbounty report

I Found Vulnerability: 
{vaa}

at : 
{url}

more information : 
{dis}


jsut write a report for this vulnerability using this template

(The below is just a template, add and modify it)


Title:

Rating: 
URL: 
Description: 

Proof of Concept:
 




Impact:


Recommendation:



'''

print("...................................................................")

response = chat_with_gpt(question)

print("ChatGPT: \n\n" + response)

url = url_r

pdf_yn = input("do you want pdf (y/n) > ")

while 1:
    if pdf_yn == "y":

        command = f"cutycapt --url={url} --out=./reports_ai/screenshot/{url}.png"

        output = subprocess.check_output(command, shell=True, text=True)

        print(f"\n\n[*] Done - save screenshot ./reports_ai/screenshot/{url}.png")

        # Split the text into paragraphs
        sections = re.split(r'\n(?=Report Title:|Rating:|URL:|Description:|Proof of Concept:|Impact:|Recommendation:)', response)

        # Extract the title section
        title_section = vaa
        sections = sections[0:]

        # Create a PDF document
        pdf_filename = "./reports_ai/report.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Create a list to hold the table data
        data = []

        # Define table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ])

        # Create the title section
        title_paragraph = Paragraph(f'<para alignment="center">{title_section}</para>', getSampleStyleSheet()['Normal'])
        title_data = [[title_paragraph]]
        title_table = Table(title_data, colWidths=450, rowHeights=60)
        title_table.setStyle(table_style)

        # Create a table for each section
        for section in sections:
            section = section.strip()
            if section:
                section_parts = section.split(':', 1)
                if len(section_parts) == 2:
                    title, content = section_parts
                    title_paragraph = Paragraph(title + ":", getSampleStyleSheet()['Normal'])
                    content_paragraph = Paragraph(content.strip(), getSampleStyleSheet()['Normal'])
                    data.append([title_paragraph, content_paragraph, Spacer(1, 10)])

        # Create the main table
        table = Table(data, colWidths=[100, 350, 1], rowHeights=60)
        table.setStyle(table_style)

        # Build the PDF document
        elements = [title_table, Spacer(1, 20), table]

        # Create a new page at the beginning of the document
        first_page = []
        first_page.append(Paragraph("BugBounty Report", getSampleStyleSheet()['Title']))
        today = datetime.date.today().strftime("%Y/%m/%d")
        first_page.append(Paragraph("", getSampleStyleSheet()['Title']))
        first_page.append(Paragraph("", getSampleStyleSheet()['Title']))
        first_page.append(Paragraph(f"{today}", getSampleStyleSheet()['Title']))
        first_page.append(Paragraph("", getSampleStyleSheet()['Title']))
        first_page.append(Paragraph("", getSampleStyleSheet()['Title']))
        first_page.append(Paragraph("", getSampleStyleSheet()['Title']))
        first_page.append(Paragraph("", getSampleStyleSheet()['Title']))

        command = f"rm -rf ./bing;python Bulk-Bing-Image-downloader/bbid/bbid.py {url} --limit 1"

        output = subprocess.check_output(command, shell=True, text=True)

        command = "ls bing"

        output = subprocess.check_output(command, shell=True, text=True)


        img = f"./bing/{output}".strip()
        print(f"\n\n[*] Done - save img {img}")

        screenshot_page = Image(img)

        screenshot_page.drawHeight = 400
        screenshot_page.drawWidth = 600
        first_page.append(screenshot_page)
        first_page.append(PageBreak())

        # Add the title and date page to the elements
        elements = first_page + elements

        # Create an additional page for the screenshot
        screenshot_page = Image(f"./reports_ai/screenshot/{url}.png")
        screenshot_page.drawHeight = 600
        screenshot_page.drawWidth = 300
        elements.append(screenshot_page)

        doc.build(elements)

        print(f"[*] Done - save PDF: {pdf_filename}")

        break
    elif pdf_yn == "n":
        break
    else:
        pdf_yn = input("do you want pdf (y/n) > ")