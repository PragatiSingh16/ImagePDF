from PyPDF2 import PdfReader
def extract_images_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page_num in range(0,len(reader.pages)):
            selected_page = reader.pages [page_num]
            for img_file_obj in selected_page.images:
                with open(img_file_obj.name, "wb") as out:
                    out.write(img_file_obj.data)
extract_images_from_pdf("Java_OOPs_Concepts.pdf")