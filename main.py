from fastapi import FastAPI, UploadFile, File
from io import BytesIO
import fitz  # for PDF handling
import PIL.Image
import easyocr
from transformers import AutoTokenizer, AutoModelWithLMHead

app = FastAPI()

# Function to extract text from an image using OCR
def extract_text_from_image(image_path, language='en'):
    reader = easyocr.Reader([language])
    result = reader.readtext(image_path)
    text = ' '.join([item[1] for item in result])
    return text

# Function to summarize text using T5 model
def summarize_text(text):
    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)
    inputs = tokenizer.encode("summarize: " + text, return_tensors='pt', max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2)
    summary = tokenizer.decode(summary_ids[0])
    return summary

@app.post("/process_file/")
async def process_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_extension = file.filename.split(".")[-1]

    if file_extension.lower() == "pdf":
        # Extract images from the PDF
        pdf = fitz.open(stream=contents, filetype="pdf")
        extracted_images = []
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            images = page.get_images()
            for img_index, img in enumerate(images):
                base_img = pdf.extract_image(img[0])
                image_data = base_img["image"]
                img_pil = PIL.Image.open(BytesIO(image_data))
                img_byte_array = BytesIO()
                img_pil.save(img_byte_array, format="PNG")
                extracted_images.append(img_byte_array.getvalue())

        # Process each extracted image and summarize text
        summarized_texts = []
        for img_data in extracted_images:
            text_from_image = extract_text_from_image(BytesIO(img_data))
            summarized_text = summarize_text(text_from_image)
            summarized_texts.append(summarized_text)

        return {"summaries": summarized_texts}

    elif file_extension.lower() in ["jpg", "jpeg", "png"]:
        # Extract text from the image and summarize
        text_from_image = extract_text_from_image(BytesIO(contents))
        summarized_text = summarize_text(text_from_image)
        return {"summary": summarized_text}

    else:
        return {"error": "Unsupported file format. Please provide a PDF or an image (JPG, JPEG, PNG)."}