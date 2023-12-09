from transformers import AutoTokenizer, AutoModelWithLMHead
import easyocr
import fitz
import PIL.Image
import io
from fastapi import FastAPI, UploadFile, File
import fitz
import io
import easyocr
import PIL.Image
import requests
import tools

app = FastAPI()

output = "default"


@app.post("/")
async def extract_text(file: UploadFile = File(...)):
    global output
    file_extension = file.filename.split(".")[-1]
    if file_extension.lower() == "pdf":
        with open("temp_file.pdf", "wb") as f:
            f.write(file.file.read())
        extracted_summary = extract_images_from_pdf("temp_file.pdf")
    else:
        with open("temp_image.jpg", "wb") as f:
            f.write(file.file.read())
        img = PIL.Image.open("temp_image.jpg")
        extracted_summary = only_image_to_text(img)
    output = extracted_summary
    return {"extracted_summary": extracted_summary}


@app.get("/")
async def getdata():
    return output


def extract_images_from_pdf(pdf_path):
    pdf = fitz.open(pdf_path)
    extracted_text = ""
    for page in pdf:
        images = page.get_images()
        for image in images:
            base_img = pdf.extract_image(image[0])
            image_data = base_img["image"]
            img = PIL.Image.open(io.BytesIO(image_data))
            extracted_text += image_to_text(img)

    return TextToSummary(extracted_text)


def image_to_text(image):
    reader = easyocr.Reader(["en"])
    result = reader.readtext(image)
    text = " ".join([item[1] for item in result])
    return text


def only_image_to_text(image):
    reader = easyocr.Reader(["en"])
    result = reader.readtext(image)
    text = " ".join([item[1] for item in result])
    return TextToSummary(text)


def TextToSummary(text):
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    model = AutoModelWithLMHead.from_pretrained("t5-base", return_dict=True)
    inputs = tokenizer.encode(
        "summarize: " + text, return_tensors="pt", max_length=512, truncation=True
    )
    summary_ids = model.generate(
        inputs, max_length=50, min_length=8, length_penalty=5.0, num_beams=2
    )
    summary = tokenizer.decode(summary_ids[0])
    # print(summary)
    return summary