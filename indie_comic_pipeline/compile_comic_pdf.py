"""
COMIC BOOK PDF COMPILER
Assembles all generated page layout grids into a single PDF document
"""

import os
import sys
from PIL import Image
import re
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config_helper import load_settings, get_output_path

def compile_pdf(layout_style='sdxl_lora_grid'):
    settings = load_settings()
    comics_dir = settings.get("outputs", {}).get("comics_dir", "outputs/comics")
    
    print("=" * 70)
    print("COMIC BOOK PDF COMPILER")
    print("=" * 70)
    print(f"Scanning '{comics_dir}' for pages matching pattern: *layout*{layout_style}*")
    
    # Get all files in comics dir
    if not os.path.exists(comics_dir):
        print(f"Error: Comics output directory not found at: {comics_dir}")
        return False
        
    files = os.listdir(comics_dir)
    
    # We want to match page_X_layout_<style>.png
    page_files = []
    for f in files:
        if "layout" in f and layout_style in f and f.endswith(".png"):
            # Extract page number
            match = re.search(r'page_(\d+)', f)
            if match:
                page_num = int(match.group(1))
                page_files.append((page_num, os.path.join(comics_dir, f)))
                
    if not page_files:
        print(f"\nWarning: No page grid layouts found with style '{layout_style}' in {comics_dir}.")
        print("Available styles in output folder:")
        styles = set()
        for f in files:
            if "layout_" in f and f.endswith(".png"):
                parts = f.replace("page_", "").split("_layout_")
                if len(parts) > 1:
                    styles.add(parts[1].replace(".png", ""))
        for s in styles:
            print(f"  - {s}")
            
        print("\nTo generate pages first, run:")
        print("  python run_everything.py")
        return False
        
    # Sort pages numerically
    page_files.sort(key=lambda x: x[0])
    
    print(f"\nFound {len(page_files)} pages to compile:")
    for num, path in page_files:
        print(f"  - Page {num}: {os.path.basename(path)}")
        
    # Load images and convert to RGB
    images = []
    try:
        for num, path in page_files:
            img = Image.open(path)
            # PDF requires RGB mode
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
    except Exception as e:
        print(f"Error loading images: {e}")
        return False
        
    output_pdf = get_output_path(comics_dir, f"comic_book_{layout_style}.pdf")
    
    try:
        # Save as PDF
        images[0].save(
            output_pdf,
            save_all=True,
            append_images=images[1:]
        )
        print(f"\n[SUCCESS] Comic PDF successfully compiled and saved to:")
        print(f"  -> {output_pdf}")
        print("=" * 70)
        return True
    except Exception as e:
        print(f"Error saving PDF: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile generated comic pages into a PDF.")
    parser.add_argument("--style", type=str, default="sdxl_lora_grid", 
                        help="The layout style grid to search for (e.g. sdxl_base_grid, sdxl_lora_grid, sd15_lora_grid, doodle_grid).")
    args = parser.parse_args()
    
    # Try the user specified style. If not found, try common fallbacks
    success = compile_pdf(args.style)
    if not success and args.style == "sdxl_lora_grid":
        # Fallback check
        for fallback in ["sdxl_base_grid", "sd15_lora_grid", "doodle_grid", "grid"]:
            print(f"\nTrying fallback style: {fallback}...")
            if compile_pdf(fallback):
                break
