import pdfplumber
import pandas as pd

def convert_pdf_to_excel(pdf_path, output_path):
    all_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_data.append(df)

    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        result.to_excel(output_path, index=False)
