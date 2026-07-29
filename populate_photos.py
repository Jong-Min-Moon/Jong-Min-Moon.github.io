#!/usr/bin/env python3
import argparse
import os
import glob
import subprocess
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def main():
    parser = argparse.ArgumentParser(description="Automate populating travel photos into Jekyll pages.")
    parser.add_argument('--state', required=True, help="State name (used for filename), e.g., 'kentucky', 'washington-dc'")
    parser.add_argument('--heading', required=True, help="Exact heading title in the markdown file, e.g., 'Galactic Fried Chicken'")
    parser.add_argument('--photo-dir', required=True, help="Absolute path to the directory containing new photos")
    
    args = parser.parse_args()
    
    state_slug = slugify(args.state)
    heading_slug = slugify(args.heading)
    prefix = f"{state_slug}-{heading_slug}"
    
    repo_root = os.path.abspath(os.path.dirname(__file__))
    img_dir = os.path.join(repo_root, "assets", "img", "travel")
    video_dir = os.path.join(repo_root, "assets", "video", "travel")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)
    
    # 1. Find media files
    extensions = {
        'image': ['*.heic', '*.HEIC', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.PNG'],
        'video': ['*.mov', '*.MOV', '*.mp4', '*.MP4']
    }
    
    media_files = []
    for ext in extensions['image']:
        for f in glob.glob(os.path.join(args.photo_dir, ext)):
            media_files.append(('image', f))
            
    for ext in extensions['video']:
        for f in glob.glob(os.path.join(args.photo_dir, ext)):
            media_files.append(('video', f))
    
    # Sort by original filename
    media_files.sort(key=lambda x: os.path.basename(x[1]))
    
    if not media_files:
        print(f"No media found in '{args.photo_dir}'. Please check the directory path.")
        return
    
    print(f"Found {len(media_files)} files in '{args.photo_dir}'. Processing...")
    
    # 2. Process files
    html_snippets = []
    for count, (mtype, file_path) in enumerate(media_files, start=1):
        if mtype == 'image':
            out_full = os.path.join(img_dir, f"{prefix}-{count}.jpg")
            out_thumb = os.path.join(img_dir, f"{prefix}-{count}-thumb.jpg")
            
            # Convert to jpeg
            subprocess.run(['sips', '-s', 'format', 'jpeg', file_path, '--out', out_full], check=True, stdout=subprocess.DEVNULL)
            # Create thumbnail
            subprocess.run(['sips', '-Z', '400', out_full, '--out', out_thumb], check=True, stdout=subprocess.DEVNULL)
            
            html = f'        <img src="{{{{ \'assets/img/travel/{prefix}-{count}-thumb.jpg\' | relative_url }}}}" data-zoom-src="{{{{ \'assets/img/travel/{prefix}-{count}.jpg\' | relative_url }}}}" class="img-fluid rounded z-depth-1" data-zoomable>'
            html_snippets.append(html)
            
        elif mtype == 'video':
            ext = os.path.splitext(file_path)[1].lower()
            out_name = f"{prefix}-{count}{ext}"
            out_full = os.path.join(video_dir, out_name)
            
            # Copy video
            subprocess.run(['cp', file_path, out_full], check=True)
            
            html = f'        {{% include video.html path="assets/video/travel/{out_name}" class="img-fluid rounded z-depth-1" controls=true autoplay=true loop=true muted=true %}}'
            html_snippets.append(html)
            
        print(f"Processed file {count}/{len(media_files)}")
    
    # 3. Generate HTML grid
    html_lines = []
    for i, snippet in enumerate(html_snippets):
        if i % 3 == 0:
            if i > 0:
                html_lines.append("</div>")
            html_lines.append('<div class="row mt-3">')
        
        html_lines.append('    <div class="col-sm mt-3 mt-md-0">')
        html_lines.append(snippet)
        html_lines.append('    </div>')
        
    if media_files:
        html_lines.append("</div>")
        
    html_snippet = "\n" + "\n".join(html_lines) + "\n"
    
    # 4. Insert HTML into the markdown file
    md_path = os.path.join(repo_root, "_pages", "travel", f"{state_slug}.md")
    if not os.path.exists(md_path):
        print(f"Error: Target markdown file not found at '{md_path}'. Ensure the state name is correct.")
        return
        
    with open(md_path, 'r') as f:
        content = f.read()
        
    # Match the exact heading line
    # (e.g. ### Galactic Fried Chicken)
    heading_pattern = re.compile(r"^(#+\s+" + re.escape(args.heading) + r"\s*)$", re.MULTILINE)
    match = heading_pattern.search(content)
    
    if not match:
        print(f"Error: Heading '{args.heading}' not found in '{md_path}'.")
        return
        
    insert_pos = match.end()
    new_content = content[:insert_pos] + html_snippet + content[insert_pos:]
    
    with open(md_path, 'w') as f:
        f.write(new_content)
        
    print(f"\nSuccessfully added responsive photo grid to {md_path} under '{args.heading}'!")

if __name__ == "__main__":
    main()
