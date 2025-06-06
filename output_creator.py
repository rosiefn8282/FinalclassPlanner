import pandas as pd
from fpdf import FPDF

def save_schedule_excel(schedule, filename="output_schedule.xlsx"):
    df = pd.DataFrame(schedule)
    df.to_excel(filename, index=False)

def save_schedule_pdf(schedule, filename="output_schedule.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "برنامه زمان‌بندی کلاس‌ها", ln=True, align='C')

    for item in schedule:
        line = f"{item['course']} - {item['teacher']} - {item['day']} - {item['time_slot'][0]} تا {item['time_slot'][1]} - کلاس {item['room']}"
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(filename)
