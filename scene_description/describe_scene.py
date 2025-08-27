# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
# import torch

# # processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# # model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
# MODEL_DIR = "./models/blip-image-captioning-base"
# processor = BlipProcessor.from_pretrained(MODEL_DIR, local_files_only=True)
# model = BlipForConditionalGeneration.from_pretrained(MODEL_DIR, local_files_only=True)

# def describe_image(image_path: str) -> str:
#     try:
#         # Load image using PIL
#         image = Image.open(image_path).convert('RGB')
        
#         # Preprocess image
#         inputs = processor(images=image, return_tensors="pt")

#         # Forward pass
#         out = model.generate(**inputs)
#         description = processor.decode(out[0], skip_special_tokens=True)

#         return description
#     except Exception as e:
#         print(f"❌ Error in describe_image(): {e}")
#         return "Sorry, I couldn't understand the image."


from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import cv2 
import os
import numpy as np

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def describe_all_parts(image_path: str) -> str:
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    
    # Calculate the width of each part
    part_width = width // 3
    
    # Slice the image into three parts
    left_part = image[:, :part_width]
    center_part = image[:, part_width:part_width*2]
    right_part = image[:, part_width*2:]
    
    # Save the parts temporarily
    cv2.imwrite("temp_left.jpg", left_part)
    cv2.imwrite("temp_center.jpg", center_part)
    cv2.imwrite("temp_right.jpg", right_part)
    
    # Describe each part using the existing function
    desc_left = describe_image("temp_left.jpg")
    desc_center = describe_image("temp_center.jpg")
    desc_right = describe_image("temp_right.jpg")

    # Clean up temporary files
    os.remove("temp_left.jpg")
    os.remove("temp_center.jpg")
    os.remove("temp_right.jpg")
    
    # Combine the descriptions
    combined_description = f"On the left, I see {desc_left}. In the center, I see {desc_center}. On the right, I see {desc_right}."
    
    return combined_description

def describe_image(image_path: str) -> str:
    try:
        # Load image using PIL
        image = Image.open(image_path).convert('RGB')
        
        # Preprocess image
        inputs = processor(images=image, return_tensors="pt")

        # Forward pass
        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)

        return description
    except Exception as e:
        print(f"❌ Error in describe_image(): {e}")
        return "Sorry, I couldn't understand the image."