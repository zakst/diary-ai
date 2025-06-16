from pathlib import Path
import easyocr
import asyncio
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# TrOCR (Microsoft handwriting model) setup
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

async def convert_image_to_text_trocr(image_path: str) -> str:
    try:
        image = Image.open(image_path).convert("RGB")
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_text
    except FileNotFoundError:
        return f"Error: The file at {image_path} was not found."
    except Exception as e:
        return f"An error occurred (TrOCR): {e}"

async def main():
    image_file_path = 'sample-handwritten.jpg'
    output_text_path = 'extracted_handwritten_text.txt'

    trocr_text = await convert_image_to_text_trocr(image_file_path)

    print("--- Extracted with TrOCR (handwritten) ---")
    print(trocr_text)

    # Combine and write to file
    with open(output_text_path, 'w', encoding='utf-8') as f:
        f.write("=== TrOCR Output ===\n")
        f.write(trocr_text)

    print(f"Text written to: {output_text_path}")

if __name__ == "__main__":
    asyncio.run(main())
