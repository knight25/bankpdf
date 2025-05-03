from flask import Flask, request, send_file, render_template
import pdfplumber
import pandas as pd
import io
import os
import traceback

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    try:
        file = request.files.get("file")
        if not file:
            return "No file uploaded", 400

        with pdfplumber.open(file) as pdf:
            all_data = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    all_data.extend(table)

        if not all_data:
            return "No tables found in the PDF.", 400

        # Convert to DataFrame and remove the header row from data
        df = pd.DataFrame(all_data[1:], columns=all_data[0])

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="converted.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        # Log the error to Render logs
        traceback.print_exc()
        return f"An error occurred while converting the PDF: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
