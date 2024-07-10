import os
from pdf2image import convert_from_path
import http.server
import socketserver

def pdf_to_images(pdf_path, output_folder, poppler_path):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    image_paths = []
    for i, page in enumerate(pages):
        image_path = os.path.join(output_folder, f'page_{i + 1}.png')
        page.save(image_path, 'PNG')
        image_paths.append(image_path)
        print(f"Saved image: {image_path}")
    return image_paths

def generate_html(image_paths, output_html):
    if not image_paths:
        print("No images found to include in the HTML.")
        return
    
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flipbook</title>
    <style>
        body { text-align: center; background-color: #f0f0f0; }
        #flipbook { width: 800px; height: 600px; margin: 50px auto; }
        .page { width: 100%; height: 100%; background-color: white; }
        .page img { width: 100%; height: 100%; }
        #startButton {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            margin: 20px;
        }
        #startButtonContainer {
            text-align: center;
            margin-top: 50px;
        }
    </style>
</head>
<body>
    <div id="startButtonContainer">
        <button id="startButton">Start Flipbook</button>
    </div>
    <div id="flipbook" style="display:none;">
'''

    # Add the cover page
    cover_page = image_paths[0]
    relative_cover_path = os.path.relpath(cover_page, os.path.dirname(output_html))
    html_content += f'<div class="page"><img src="{relative_cover_path}" alt="Cover Page"></div>\n'
    print(f"Added cover image to HTML: {relative_cover_path}")

    # Add the rest of the pages
    for image_path in image_paths[1:]:
        relative_image_path = os.path.relpath(image_path, os.path.dirname(output_html))
        html_content += f'<div class="page"><img src="{relative_image_path}" alt="Page"></div>\n'
        print(f"Added image to HTML: {relative_image_path}")

    html_content += '''
    </div>
    <audio id="flip-sound" src="sounds/flip.mp3"></audio>
    <script src="node_modules/jquery/dist/jquery.min.js"></script>
    <script src="node_modules/turn.js/turn.js"></script>
    <script>
        document.getElementById('startButton').addEventListener('click', function() {
            document.getElementById('startButtonContainer').style.display = 'none';
            document.getElementById('flipbook').style.display = 'block';

            $('#flipbook').turn({
                width: 800,
                height: 600,
                autoCenter: true,
                when: {
                    turning: function(e, page, view) {
                        console.log("Turning to page " + page);
                        var flipSound = document.getElementById('flip-sound');
                        if (flipSound) {
                            flipSound.play().catch(error => {
                                console.log("Audio play prevented: " + error);
                            });
                        }
                    }
                }
            });

            // Additional debugging
            if ($('#flipbook').turn('is')) {
                console.log('Turn.js is initialized');
            } else {
                console.log('Turn.js failed to initialize');
            }
        });
    </script>
</body>
</html>
'''

    with open(output_html, 'w') as f:
        f.write(html_content)
    print(f"HTML content written to {output_html}")

def create_flipbook(pdf_path, output_folder, output_html, poppler_path):
    image_paths = pdf_to_images(pdf_path, output_folder, poppler_path)
    generate_html(image_paths, output_html)

    # Serve the directory with HTTP server
    os.chdir(os.path.dirname(output_html))
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# Example usage
pdf_path = r'D:\ostad jafary\Binder1.pdf'
output_folder = r'D:\ostad jafary\output_images'
output_html = r'D:\ostad jafary\flipbook.html'
poppler_path = r'C:\Program Files (x86)\poppler-24.02.0\Library\bin'  # Specify the full path to the poppler bin directory

create_flipbook(pdf_path, output_folder, output_html, poppler_path)
