import os
import re
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---
HTML_FILE = 'data.html'
TEMPLATE_IMAGE = 'Co..jpg'
OUTPUT_FOLDER = 'output'
FONT_FILE = 'Poppins-Medium.ttf' # Make sure your downloaded font matches this name exactly

# --- COORDINATES & STYLING ---
# IMPORTANT: You still need to find the exact X, Y pixels for your Co..jpg template
COORD_ID = (400, 450)      # (X, Y) Replace with the starting pixel for the User ID
COORD_VOUCHER = (400, 550) # (X, Y) Replace with the starting pixel for the Voucher Number

TEXT_COLOR = (255, 255, 255) # White text to show up on the dark input boxes
FONT_SIZE = 36               # Adjust size if it's too big/small for the boxes

def extract_data_from_html(filepath):
    """Reads the file and extracts IDs and Voucher numbers from the JavaScript array."""
    extracted_data = []
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        
        # This Regex perfectly captures the 'id' and 'user' from your specific code
        # Example target: { id: 1,  user: "al__maz06", text: "RCB- ❤️" }
        matches = re.findall(r'id:\s*(\d+),\s*user:\s*"([^"]+)"', content)
        
        for match in matches:
            voucher_num = match[0]
            ig_id = match[1]
            
            extracted_data.append({
                'id': f"@{ig_id}", # Adds the '@' symbol for a cleaner look
                'voucher': voucher_num
            })
            
    return extracted_data

def generate_cards(data_list):
    """Takes the extracted data, applies it to the theme, and saves it."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    try:
        base_image = Image.open(TEMPLATE_IMAGE)
        font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
    except FileNotFoundError as e:
        print(f"Error: Missing file! {e}")
        print("Make sure 'Co..jpg' and your font file are in the exact same folder as this script.")
        return

    print(f"Successfully found {len(data_list)} users. Starting generation...")

    for item in data_list:
        ig_id = item['id']
        voucher_num = item['voucher']
        
        # Make a fresh copy of the base image
        card = base_image.copy()
        draw = ImageDraw.Draw(card)
        
        # Draw the text onto the image perfectly
        draw.text(COORD_ID, ig_id, font=font, fill=TEXT_COLOR)
        
        # Formats the voucher as a 3-digit number (e.g., "001", "045", "112")
        formatted_voucher = str(voucher_num).zfill(3)
        draw.text(COORD_VOUCHER, formatted_voucher, font=font, fill=TEXT_COLOR)
        
        # Clean up the filename for saving
        safe_filename = f"{formatted_voucher}_{ig_id.replace('@', '')}.jpg"
        save_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        
        card.save(save_path)
        print(f"Saved -> {safe_filename}")

    print("\n✅ Success! All 112 gift cards have been generated perfectly.")

if __name__ == "__main__":
    people_data = extract_data_from_html(HTML_FILE)
    
    if people_data:
        generate_cards(people_data)
    else:
        print("No data found. Please double-check your HTML file.")