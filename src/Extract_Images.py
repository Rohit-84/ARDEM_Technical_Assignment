import fitz  # PyMuPDF
import os

def pdf_to_png(pdf_files, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pdf_file in pdf_files:
        try:
            doc = fitz.open(pdf_file)
            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=300)  # Adjust DPI if needed
                output_path = os.path.join(output_dir, f"{base_name}_page_{page_num + 1}.png")
                pix.save(output_path)
                print(f"Saved: {output_path}")
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

# Example usage
pdf_files = ["pdf_path/1.pdf", "pdf_path/2.pdf"]  # List of PDF paths
output_dir = "output_images"
pdf_to_png(pdf_files, output_dir)
