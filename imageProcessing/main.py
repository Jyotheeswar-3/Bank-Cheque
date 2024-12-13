import os
import google.generativeai as genai
from PIL import Image
genai.configure(api_key="AIzaSyBiZE6lwvZP5YcHYBM5h6O13S2PJEI3BI4")
# Initialize the generative model
model = genai.GenerativeModel("gemini-1.5-flash")

def process_image(image_path):
    """
    Process a single image to extract cheque details.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: Extracted cheque details.
    """
    try:
        # Open the image
        image = Image.open(image_path)

        # Generate content from the image
        prompt = ["Extract cheque details: bank name, date, payee name, amount in words, amount in numbers, account number, cheque number.", image]
        response = model.generate_content(prompt)

        # Parse the response
        # Assuming the response contains structured text in the required format
        extracted_data = response.text
        return {
            "image": os.path.basename(image_path),
            "details": extracted_data,
        }

    except Exception as e:
        return {
            "image": os.path.basename(image_path),
            "error": str(e),
        }

def process_folder(folder_path):
    """
    Process all images in a folder and extract details from each image.

    Args:
        folder_path (str): Path to the folder containing ima
    Returns:
        list: List of dictionaries containing cheque details for each image.
    """
    results = []

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff")):
            print(f"Processing image: {file_path}")
            result = process_image(file_path)
            results.append(result)

    return results

def save_results(results, output_file):
    """
    Save extracted results to a file.

    Args:
        results (list): List of extracted details.
        output_file (str): Path to the output file.
    """
    with open(output_file, "w") as f:
        for result in results:
            if "error" in result:
                f.write(f"Image: {result['image']}\nError: {result['error']}\n\n")
            else:
                f.write(f"Image: {result['image']}\nDetails: {result['details']}\n\n")

if __name__ == "__main__":
    # Path to the folder containing cheque images
    folder_path = "/Users/jammubestha/Desktop/Bank_Cheque/output_images"

    # Output file to save extracted results
    output_file = "/Users/jammubestha/Desktop/Bank_Cheque/imageProcessing/FinalOutput/extracted_cheque_details.txt"

    # Process the folder
    results = process_folder(folder_path)

    # Save the results to a file
    save_results(results, output_file)

    print(f"Results saved to {output_file}")
