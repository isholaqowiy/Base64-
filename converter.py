import base64
import os
from PIL import Image
from config import TEMP_DIR

def encode_image_to_base64(image_path: str, user_id: int) -> tuple:
    """Converts a local image file into an encoded Base64 ASCII string asset."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_bytes = base64.b64encode(image_file.read())
            encoded_str = encoded_bytes.decode('utf-8')
            
        with Image.open(image_path) as img:
            dimensions = f"{img.width}x{img.height}"
            img_format = img.format
            
        txt_output_path = os.path.join(TEMP_DIR, f"encoded_{user_id}.txt")
        with open(txt_output_path, "w") as txt_file:
            txt_file.write(encoded_str)
            
        return encoded_str, txt_output_path, dimensions, img_format
    except Exception as e:
        print(f"Encoding Exception: {e}")
        return None, None, None, None

def decode_base64_to_image(base64_str: str, user_id: int) -> str:
    """Decodes a clean Base64 data block into a viewable physical image asset on disk."""
    try:
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]
            
        base64_str = base64_str.strip()
        decoded_bytes = base64.b64decode(base64_str, validate=True)
        
        output_image_path = os.path.join(TEMP_DIR, f"decoded_{user_id}.png")
        with open(output_image_path, "wb") as img_file:
            img_file.write(decoded_bytes)
            
        with Image.open(output_image_path) as img:
            img.verify()
            
        return output_image_path
    except Exception as e:
        print(f"Decoding Exception: {e}")
        return None

