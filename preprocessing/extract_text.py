import os
import json
import docx
import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text

def split_into_paragraphs(text):
    # Basic split using double newlines or line breaks
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
    return paragraphs

def extract_and_save(file_path, output_json="../data/extracted_text.json"):
    if not os.path.exists("data"):
        os.makedirs("data")
    
    file_type = os.path.splitext(file_path)[1].lower()
    if file_type == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif file_type == ".docx":
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please use PDF or DOCX.")
    
    paragraphs = split_into_paragraphs(raw_text)

    data = {
        "filename": os.path.basename(file_path),
        "num_paragraphs": len(paragraphs),
        "paragraphs": paragraphs
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"[✓] Extracted and saved {len(paragraphs)} paragraphs from {file_path}")

# Example usage (you can delete this later):
if __name__ == "__main__":
    # Drop your sample PDF or DOCX in the root or data folder
    test_file = "../data/sample.pdf"  # or sample.docx
    extract_and_save(test_file)
