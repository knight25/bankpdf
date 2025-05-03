from flask import Flask, render_template, request, send_file
from utils.converter import convert_pdf_to_excel
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".pdf"):
            pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(pdf_path)
            output_filename = f"{uuid.uuid4().hex}.xlsx"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            convert_pdf_to_excel(pdf_path, output_path)

            return send_file(output_path, as_attachment=True)

    return render_template("index.html")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

