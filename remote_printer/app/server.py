from flask import Flask, request, jsonify, render_template
import cups
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

conn = cups.Connection()
printers = conn.getPrinters()
printer_name = list(printers.keys())[0] if printers else None

@app.route("/")
def index():
    return render_template("index.html", printers=printers.keys())

@app.route("/print", methods=["POST"])
def print_file():
    file = request.files.get("file")
    printer = request.form.get("printer", printer_name)
    if not file or not printer:
        return jsonify({"error": "Brak pliku lub drukarki"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        job_id = conn.printFile(printer, filepath, "Druk z HA", {})
        return jsonify({"message": f"Wysłano do druku (ID: {job_id})"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500