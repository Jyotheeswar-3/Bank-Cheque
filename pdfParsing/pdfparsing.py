import fitz
import os
from PIL import Image
from io import BytesIO

# Constants
INPUT_FOLDER = '/Users/jammubestha/Desktop/Bank_Cheque/inputFolder'  # Folder containing PDF files
OUTPUT_FOLDER = '/Users/jammubestha/Desktop/Bank_Cheque/output_images'  # Folder to save extracted images
OUTPUT_SIZE = (2400, 1100)  # Desired image size (width, height)

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_and_resize_images(pdf_path, output_folder, output_size):
    """
    Extracts and resizes images from a PDF file and saves them to the output folder.

    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Folder to save the extracted images.
        output_size (tuple): Desired size of the output images (width, height).
    """
    doc = fitz.open(pdf_path)

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)

        if not images:
            print(f"No images found on page {page_num + 1} of {os.path.basename(pdf_path)}.")
            continue

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image = Image.open(BytesIO(image_bytes))
            resized_image = image.resize(output_size, Image.Resampling.LANCZOS)

            output_filename = f"{os.path.basename(pdf_path)[:-4]}_page{page_num + 1}_img{img_index + 1}.jpg"
            output_path = os.path.join(output_folder, output_filename)

            resized_image.save(output_path, format="JPEG")
            print(f"Saved: {output_filename}")

    doc.close()

def process_pdfs(input_folder, output_folder, output_size):
    """
    Processes all PDF files in the input folder, extracting and resizing images.

    Args:
        input_folder (str): Folder containing PDF files.
        output_folder (str): Folder to save the extracted images.
        output_size (tuple): Desired size of the output images (width, height).
    """
    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, pdf_file)
            extract_and_resize_images(pdf_path, output_folder, output_size)

# Main Execution
process_pdfs(INPUT_FOLDER, OUTPUT_FOLDER, OUTPUT_SIZE)