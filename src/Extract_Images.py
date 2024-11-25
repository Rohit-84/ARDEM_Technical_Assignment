import fitz  # PyMuPDF

def extract_images_from_pdf(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    for page_number in range(len(doc)):
        page = doc[page_number]
        pix = page.get_pixmap()
        pix.save(f"{output_folder}/page_{page_number + 1}.png")
