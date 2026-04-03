#!/usr/bin/env python3
"""
Slide Manager — Safe HTML manipulation for RevealJS presentations.
Uses BeautifulSoup to parse and modify presentation.html without breaking markup.

Usage (called by slide-manager.sh):
  python3 slide-manager.py list <presentation.html>
  python3 slide-manager.py add-png <presentation.html> <image_path> [--after N]
  python3 slide-manager.py add-template <presentation.html> <template_name> [--after N] [--title "..."] [--image "..."]
  python3 slide-manager.py remove <presentation.html> <slide_number>
  python3 slide-manager.py edit <presentation.html> <slide_number>
  python3 slide-manager.py export-slide <presentation.html> <slide_number>
"""

import sys
import os
import re
import shutil
import argparse
import tempfile
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip3 install beautifulsoup4")
    sys.exit(1)


TEMPLATES_DIR = Path(__file__).parent.parent / "slide-templates"


def load_presentation(path):
    with open(path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')


def save_presentation(soup, path):
    # Backup before writing
    backup = path + '.bak'
    if os.path.exists(path):
        shutil.copy2(path, backup)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify(formatter="html5"))

    # Validate — check for unclosed section tags
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    opens = content.count('<section')
    closes = content.count('</section>')
    if opens != closes:
        print(f"WARNING: Mismatched <section> tags ({opens} opens, {closes} closes). Restoring backup.")
        shutil.copy2(backup, path)
        return False

    # Remove backup on success
    os.remove(backup)
    return True


def get_slides(soup):
    """Get all top-level <section> elements inside .slides container."""
    slides_container = soup.find('div', class_='slides')
    if not slides_container:
        # Try finding the reveal div
        reveal = soup.find('div', class_='reveal')
        if reveal:
            slides_container = reveal.find('div', class_='slides')
    if not slides_container:
        print("ERROR: Cannot find .slides container in presentation.html")
        sys.exit(1)
    return slides_container, [s for s in slides_container.find_all('section', recursive=False)]


def get_slide_title(section):
    """Extract heading text from a slide section."""
    for tag in ['h1', 'h2', 'h3']:
        heading = section.find(tag)
        if heading:
            return heading.get_text(strip=True)
    # Check for image-only slides
    img = section.find('img')
    if img:
        alt = img.get('alt', '')
        src = img.get('src', '')
        return f"[Image: {alt or os.path.basename(src)}]"
    return "(untitled)"


def cmd_list(args):
    soup = load_presentation(args.presentation)
    _, slides = get_slides(soup)
    print(f"Total: {len(slides)} slides\n")
    for i, slide in enumerate(slides, 1):
        title = get_slide_title(slide)
        sid = slide.get('id', '')
        marker = ''
        if '<!-- NLM Review Slides' in str(slide):
            marker = ' [NLM]'
        elif sid:
            marker = f' [{sid}]'
        print(f"  {i:3d}. {title}{marker}")


def cmd_add_png(args):
    soup = load_presentation(args.presentation)
    container, slides = get_slides(soup)

    # Copy image to figures/ or presentation directory
    pres_dir = os.path.dirname(os.path.abspath(args.presentation))
    img_name = os.path.basename(args.image)
    dest_dir = os.path.join(pres_dir, 'extra-slides')
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, img_name)
    shutil.copy2(args.image, dest_path)
    rel_path = f"extra-slides/{img_name}"

    # Build new section
    slide_id = f"slide-extra-{len(slides) + 1}"
    new_html = f'''<section id="{slide_id}">
  <div style="text-align: center;">
    <img src="{rel_path}" style="max-height: 85vh; max-width: 95vw; object-fit: contain;" alt="{img_name}">
  </div>
</section>'''

    new_section = BeautifulSoup(new_html, 'html.parser').find('section')

    # Insert at position
    pos = args.after if args.after else len(slides)
    if pos >= len(slides):
        container.append(new_section)
    else:
        slides[pos].insert_before(new_section)

    if save_presentation(soup, args.presentation):
        print(f"Added PNG slide: {img_name} (after slide {pos if pos > 0 else 'start'})")
        print(f"  Image copied to: {dest_dir}/{img_name}")
    else:
        print("ERROR: Failed to save. Backup restored.")


def cmd_add_template(args):
    soup = load_presentation(args.presentation)
    container, slides = get_slides(soup)

    # Load template
    template_file = TEMPLATES_DIR / f"{args.template}.html"
    if not template_file.exists():
        available = [f.stem for f in TEMPLATES_DIR.glob("*.html")]
        print(f"ERROR: Template '{args.template}' not found. Available: {', '.join(available)}")
        sys.exit(1)

    template_html = template_file.read_text(encoding='utf-8')

    # Replace placeholders
    slide_id = f"slide-{len(slides) + 1}"
    replacements = {
        '{{ID}}': slide_id,
        '{{TITLE}}': args.title or 'New Slide',
        '{{IMAGE_PATH}}': args.image or 'figures/placeholder.png',
        '{{ALT_TEXT}}': args.alt or args.title or 'Slide image',
        '{{CAPTION}}': args.caption or '',
        '{{POINT_1}}': args.point1 or 'First point',
        '{{POINT_2}}': args.point2 or 'Second point',
        '{{POINT_3}}': args.point3 or 'Third point',
        '{{LEFT_HEADING}}': args.left_heading or 'Before',
        '{{RIGHT_HEADING}}': args.right_heading or 'After',
        '{{LEFT_CONTENT}}': args.left_content or 'Left column content',
        '{{RIGHT_CONTENT}}': args.right_content or 'Right column content',
        '{{SUBTITLE}}': args.subtitle or '',
        '{{SPEAKER_NOTES}}': args.notes or '',
    }

    for placeholder, value in replacements.items():
        template_html = template_html.replace(placeholder, value)

    # Warn about any unreplaced placeholders
    remaining = re.findall(r'\{\{[A-Z_]+\}\}', template_html)
    if remaining:
        print(f"WARNING: Unreplaced placeholders in template: {', '.join(remaining)}")

    new_section = BeautifulSoup(template_html, 'html.parser').find('section')

    # Insert at position
    pos = args.after if args.after else len(slides)
    if pos >= len(slides):
        container.append(new_section)
    else:
        slides[pos].insert_before(new_section)

    if save_presentation(soup, args.presentation):
        print(f"Added '{args.template}' slide: \"{args.title or 'New Slide'}\" (after slide {pos})")
    else:
        print("ERROR: Failed to save. Backup restored.")


def cmd_remove(args):
    soup = load_presentation(args.presentation)
    container, slides = get_slides(soup)

    idx = args.slide_number - 1
    if idx < 0 or idx >= len(slides):
        print(f"ERROR: Slide {args.slide_number} out of range (1-{len(slides)})")
        sys.exit(1)

    title = get_slide_title(slides[idx])
    slides[idx].decompose()

    if save_presentation(soup, args.presentation):
        print(f"Removed slide {args.slide_number}: \"{title}\"")
    else:
        print("ERROR: Failed to save. Backup restored.")


def cmd_edit(args):
    soup = load_presentation(args.presentation)
    _, slides = get_slides(soup)

    idx = args.slide_number - 1
    if idx < 0 or idx >= len(slides):
        print(f"ERROR: Slide {args.slide_number} out of range (1-{len(slides)})")
        sys.exit(1)

    # Export slide HTML to temp file for editing
    slide_html = slides[idx].prettify()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, prefix='slide_') as f:
        f.write(slide_html)
        tmp_path = f.name

    editor = os.environ.get('EDITOR', 'nano')
    print(f"Opening slide {args.slide_number} in {editor}...")
    os.system(f'{editor} "{tmp_path}"')

    # Read back and replace
    with open(tmp_path, 'r', encoding='utf-8') as f:
        edited_html = f.read()
    os.unlink(tmp_path)

    new_section = BeautifulSoup(edited_html, 'html.parser').find('section')
    if not new_section:
        print("ERROR: Edited content has no <section> tag. Aborting.")
        return

    slides[idx].replace_with(new_section)

    if save_presentation(soup, args.presentation):
        print(f"Updated slide {args.slide_number}")
    else:
        print("ERROR: Failed to save. Backup restored.")


def cmd_export_slide(args):
    """Export a single slide's HTML for inspection."""
    soup = load_presentation(args.presentation)
    _, slides = get_slides(soup)

    idx = args.slide_number - 1
    if idx < 0 or idx >= len(slides):
        print(f"ERROR: Slide {args.slide_number} out of range (1-{len(slides)})")
        sys.exit(1)

    print(slides[idx].prettify())


def main():
    parser = argparse.ArgumentParser(description='Slide Manager for RevealJS')
    sub = parser.add_subparsers(dest='command', required=True)

    # list
    p_list = sub.add_parser('list', help='List all slides')
    p_list.add_argument('presentation')

    # add-png
    p_png = sub.add_parser('add-png', help='Add a PNG as a new slide')
    p_png.add_argument('presentation')
    p_png.add_argument('image')
    p_png.add_argument('--after', type=int, default=None, help='Insert after slide N')

    # add-template
    p_tmpl = sub.add_parser('add-template', help='Add a slide from template')
    p_tmpl.add_argument('presentation')
    p_tmpl.add_argument('template', choices=['content-figure', 'full-figure', 'two-column', 'section-divider'])
    p_tmpl.add_argument('--after', type=int, default=None)
    p_tmpl.add_argument('--title', default=None)
    p_tmpl.add_argument('--image', default=None)
    p_tmpl.add_argument('--alt', default=None)
    p_tmpl.add_argument('--caption', default=None)
    p_tmpl.add_argument('--point1', default=None)
    p_tmpl.add_argument('--point2', default=None)
    p_tmpl.add_argument('--point3', default=None)
    p_tmpl.add_argument('--left-heading', default=None)
    p_tmpl.add_argument('--right-heading', default=None)
    p_tmpl.add_argument('--left-content', default=None)
    p_tmpl.add_argument('--right-content', default=None)
    p_tmpl.add_argument('--subtitle', default=None)
    p_tmpl.add_argument('--notes', default=None)

    # remove
    p_rm = sub.add_parser('remove', help='Remove a slide by number')
    p_rm.add_argument('presentation')
    p_rm.add_argument('slide_number', type=int)

    # edit
    p_edit = sub.add_parser('edit', help='Edit a slide in $EDITOR')
    p_edit.add_argument('presentation')
    p_edit.add_argument('slide_number', type=int)

    # export-slide
    p_export = sub.add_parser('export-slide', help='Print slide HTML')
    p_export.add_argument('presentation')
    p_export.add_argument('slide_number', type=int)

    args = parser.parse_args()

    commands = {
        'list': cmd_list,
        'add-png': cmd_add_png,
        'add-template': cmd_add_template,
        'remove': cmd_remove,
        'edit': cmd_edit,
        'export-slide': cmd_export_slide,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
