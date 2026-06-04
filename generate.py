#!/usr/bin/env python3
import os
import json

def main():
    logos_dir = "logos"
    if not os.path.exists(logos_dir):
        os.makedirs(logos_dir)
        print("Created logos directory.")
        
    supported_extensions = (".png", ".jpg", ".jpeg", ".webp", ".svg")
    logo_files = []
    
    try:
        files = os.listdir(logos_dir)
    except Exception as e:
        print(f"Error reading directory {logos_dir}: {e}")
        return

    for file in files:
        if file.lower().endswith(supported_extensions):
            logo_files.append(file)
            
    # Sort files to ensure stable numerical order (natural sort)
    import re
    logo_files.sort(key=lambda s: [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)])
    
    try:
        with open("logos.json", "w", encoding="utf-8") as f:
            json.dump(logo_files, f, indent=2)
        print(f"Successfully generated logos.json with {len(logo_files)} image files.")
    except Exception as e:
        print(f"Error writing logos.json: {e}")

if __name__ == "__main__":
    main()
