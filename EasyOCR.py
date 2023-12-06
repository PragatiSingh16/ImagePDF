import easyocr


def image_to_text(image_path, language='en'):
    reader = easyocr.Reader([language])

    result = reader.readtext(image_path)

    text = ' '.join([item[1] for item in result])
    return text


image_path = 'test.jpg'
result_text = image_to_text(image_path)

print("Text extracted from the image:")
print(result_text)
