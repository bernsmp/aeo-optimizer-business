"""
Crop image to 1200x640px (15:8 aspect ratio) for article hero images.
"""
import sys
from pathlib import Path
from PIL import Image

def crop_to_hero_size(input_path: str, output_path: str = None):
    """
    Crop image to 1200x640px (15:8 aspect ratio) for hero images.
    Uses center crop to maintain composition.
    
    Args:
        input_path: Path to input image
        output_path: Path to save cropped image (default: adds _hero suffix)
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}")
        return None
    
    # Set output path
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_hero{input_path.suffix}"
    else:
        output_path = Path(output_path)
    
    try:
        # Open image
        img = Image.open(input_path)
        original_size = img.size
        print(f"📸 Original size: {original_size[0]}x{original_size[1]}px")
        
        # Target size
        target_width = 1200
        target_height = 640
        target_aspect = target_width / target_height  # 1.875 (15:8)
        
        # Calculate crop box (center crop)
        img_aspect = original_size[0] / original_size[1]
        
        if img_aspect > target_aspect:
            # Image is wider - crop width
            new_width = int(original_size[1] * target_aspect)
            new_height = original_size[1]
            left = (original_size[0] - new_width) // 2
            top = 0
            right = left + new_width
            bottom = new_height
        else:
            # Image is taller - crop height
            new_width = original_size[0]
            new_height = int(original_size[0] / target_aspect)
            left = 0
            top = (original_size[1] - new_height) // 2
            right = new_width
            bottom = top + new_height
        
        # Crop image
        cropped = img.crop((left, top, right, bottom))
        print(f"✂️  Cropped to: {cropped.size[0]}x{cropped.size[1]}px")
        
        # Resize to exact target size
        resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        print(f"📐 Resized to: {target_width}x{target_height}px")
        
        # Save
        resized.save(output_path, quality=90, optimize=True)
        file_size = output_path.stat().st_size / 1024  # KB
        print(f"✅ Saved to: {output_path}")
        print(f"📦 File size: {file_size:.1f} KB")
        
        return str(output_path)
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 crop_hero_image.py <input_image_path> [output_path]")
        print("\nExample:")
        print("  python3 crop_hero_image.py ~/Downloads/dog_image.jpg")
        print("  python3 crop_hero_image.py ~/Downloads/dog_image.jpg ../clients/paworigins/images/article1_hero.jpg")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = crop_to_hero_size(input_path, output_path)
    
    if result:
        print(f"\n🎉 Success! Hero image ready: {result}")
        print(f"💡 Next: Update article-preview-mock.html to use this image")


