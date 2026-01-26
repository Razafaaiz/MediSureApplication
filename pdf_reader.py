import pdfplumber
import re

def extract_values_from_pdf(pdf_path):
    data = {}

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    print("PDF TEXT:", text)  # 🔴 DEBUG LINE

    # Example patterns (edit based on your report format)
    patterns = {
        "Age": r"Age\s*[:\-]?\s*(\d+)",
        "Gender": r"Gender\s*[:\-]?\s*(\d+)",
        "BMI": r"BMI\s*[:\-]?\s*(\d+\.?\d*)",
        "Glucose_Level": r"Glucose Level\s*[:\-]?\s*(\d+)",
        "Blood_Pressure": r"Blood Pressure\s*[:\-]?\s*(\d+)",
        "Insulin": r"Insulin\s*[:\-]?\s*(\d+\.?\d*)",
        "Physical_Activity": r"Physical Activity\s*[:\-]?\s*(\d+)",
        "Family_History": r"Family History\s*[:\-]?\s*(\d+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[key] = match.group(1)

    print("EXTRACTED:", data)  # 🔴 DEBUG LINE
    return data

def extract_breast_pdf(pdf):
    from PyPDF2 import PdfReader
    import pdfplumber
    import re

    reader = PdfReader(pdf)
    text = " ".join(page.extract_text() or "" for page in reader.pages)

    # Extract all float numbers
    numbers = re.findall(r"\d+\.\d+", text)

    # Breast cancer model expects EXACT order
    FEATURES = [
        "radius_mean",
        "texture_mean",
        "perimeter_mean",
        "area_mean",
        "smoothness_mean",
    ]

    extracted = {}

    for i, feature in enumerate(FEATURES):
        try:
            extracted[feature] = float(numbers[i])
        except:
            extracted[feature] = None

    return extracted

import pdfplumber
import re

def extract_alzheimer_pdf(pdf_path):
    data = {}

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    print("PDF TEXT:", text)  # 🔴 DEBUG LINE

    # Example patterns (edit based on your report format)
    patterns = {
        "Age": r"Age\s*[:\-]?\s*(\d+)",
        "MMSE": r"MMSE\s*[:\-]?\s*(\d+)",
        "FunctionalAssessment": r"Functional Assessment\s*[:\-]?\s*(\d+)",
        "MemoryComplaints": r"Memory Complaints\s*[:\-]?\s*(\d+)",
        "BehavioralProblems": r"Behavioral Problems\s*[:\-]?\s*(\d+)",
        "ADL": r"ADL\s*[:\-]?\s*(\d+)",
        "Confusion": r"Confusion\s*[:\-]?\s*(\d+)",
        "Disorientation": r"Disorientation\s*[:\-]?\s*(\d+)",
        "DifficultyCompletingTasks": r"Difficulty Completing Tasks\s*[:\-]?\s*(\d+)",
        "Forgetfulness": r"Forgetfulness\s*[:\-]?\s*(\d+)",
        "FamilyHistoryAlzheimers": r"Family History of Alzheimer's\s*[:\-]?\s*(\d+)"

    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[key] = match.group(1)

    print("EXTRACTED:", data)  # 🔴 DEBUG LINE
    return data


import pdfplumber
import re

def extract_heart_pdf(pdf_path):
    data = {}

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    print("PDF TEXT:", text)  # 🔴 DEBUG LINE

    # Example patterns (edit based on your report format)
    patterns = {
        "Age": r"Age\s*[:\-]?\s*(\d+)",
        "Cholesterol_Total": r"Cholesterol\s*[:\-]?\s*(\d+)",
        "Hypertension": r"Hypertension\s*[:\-]?\s*(\d+)",
        "Diabetes": r"Diabetes\s*[:\-]?\s*(\d+)",
        "Previous_Heart_Attack": r"Previous Heart Attack\s*[:\-]?\s*(\d+)",
        "BMI": r"BMI\s*[:\-]?\s*(\d+\.?\d*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[key] = match.group(1)

    print("EXTRACTED:", data)  # 🔴 DEBUG LINE
    return data

import pdfplumber
import re

def extract_migraine_pdf(pdf_path):
    data = {}

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    print("PDF TEXT:", text)  # 🔴 DEBUG LINE

    # Example patterns (edit based on your report format)
    patterns = {
        "Visual": r"Visual\s*[:\-]?\s*(\d+)",
        "Intensity": r"Intensity\s*[:\-]?\s*(\d+)",
        "Age": r"Age\s*[:\-]?\s*(\d+)",
        "Vertigo": r"Vertigo\s*[:\-]?\s*(\d+)",
        "Frequency": r"Frequency\s*[:\-]?\s*(\d+)",
        "Character": r"Character\s*[:\-]?\s*(\d+)",
        "Sensory": r"Sensory\s*[:\-]?\s*(\d+)",
        "Duration": r"Duration\s*[:\-]?\s*(\d+)",
        "Vomit": r"Vomit\s*[:\-]?\s*(\d+)",
        "Nausea": r"Nausea\s*[:\-]?\s*(\d+)",
        "DPF": r"DPF\s*[:\-]?\s*(\d+)"
    }


    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[key] = match.group(1)

    print("EXTRACTED:", data)  # 🔴 DEBUG LINE
    return data

def extract_typhoid_pdf(pdf):
    from PyPDF2 import PdfReader
    import pdfplumber
    import re

    reader = PdfReader(pdf)
    text = " ".join(page.extract_text() or "" for page in reader.pages)

    # Extract all float numbers
    numbers = re.findall(r"\d+\.\d+", text)

    # Breast cancer model expects EXACT order
    FEATURES = [
        "Platelet Count",
        "Age",
        "Hemoglobin (g/dL)",
        "Calcium (mg/dL)",
        "Potassium (mmol/L)",
        "Treatment Duration",
        "Blood Culture Bacteria",
        "Symptoms Severity",
        "Urine Culture Bacteria",
        "Current Medication",
        "Gender"
    ]

    extracted = {}

    for i, feature in enumerate(FEATURES):
        try:
            extracted[feature] = float(numbers[i])
        except:
            extracted[feature] = None

    return extracted