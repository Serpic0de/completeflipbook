import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_images(pdf_path, output_dir):
    pdf_document = fitz.open(pdf_path)
    images = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        image_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
        pix.save(image_path)
        images.append(image_path)
    return images

def create_html_slider(image_paths, output_html):
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Book Slider</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .slider { position: relative; width: 100%; max-width: 800px; margin: auto; }
        .slides { display: flex; overflow: hidden; width: 100%; }
        .slides img { width: 100%; }
        .nav { display: flex; justify-content: space-between; position: absolute; top: 50%; width: 100%; transform: translateY(-50%); }
        .nav button { background-color: rgba(0,0,0,0.5); color: white; border: none; padding: 10px; cursor: pointer; }
        .nav button:hover { background-color: rgba(0,0,0,0.8); }
    </style>
</head>
<body>

<div class="slider">
    <div class="slides" id="slides">
'''

    for img_path in image_paths:
        html_content += f'        <img src="{img_path}" alt="Page">\n'

    html_content += '''    </div>
    <div class="nav">
        <button onclick="prevSlide()">&#10094;</button>
        <button onclick="nextSlide()">&#10095;</button>
    </div>
</div>

<script>
    let currentSlide = 0;
    const slides = document.getElementById('slides');
    const totalSlides = slides.children.length;

    function showSlide(index) {
        if (index >= totalSlides) {
            currentSlide = 0;
        } else if (index < 0) {
            currentSlide = totalSlides - 1;
        } else {
            currentSlide = index;
        }
        slides.style.transform = 'translateX(' + (-currentSlide * 100) + '%)';
    }

    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    function prevSlide() {
        showSlide(currentSlide - 1);
    }
</script>

</body>
</html>'''

    with open(output_html, 'w') as file:
        file.write(html_content)

def main():
    pdf_path = 'D:\ostad jafary\سوالات-ارشد-MBA-1403.pdf'  # Replace with your PDF file path
    output_dir = 'output_images'
    output_html = 'book_slider.html'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_paths = pdf_to_images(pdf_path, output_dir)
    create_html_slider(image_paths, output_html)
    print(f'HTML slider created: {output_html}')

if __name__ == "__main__":
    main()