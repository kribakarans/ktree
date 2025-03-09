#!/usr/bin/env python3

import os
import re
import shutil
import subprocess

# Paths for installed resources
KTRACE_HOME = os.path.expanduser("~/.ktree")
RESOURCES_PATH = os.path.join(KTRACE_HOME, "res")
VIEWER_HTML = os.path.join(KTRACE_HOME, "viewer.html")

def generate_index_html(title: str, ignore_patterns: list):
    """Runs the `tree` command and modifies `index.html`."""
    ignore_arg = f"-I '{'|'.join(ignore_patterns)}'" if ignore_patterns else ""
    subprocess.run(f'tree -H . -T "Ktree: {title}" {ignore_arg} --noreport -o index.html', shell=True)

    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # Update footer
    html_content = re.sub(
        r'<p class="VERSION">.*?</p>',
        '<p class="VERSION">Built with Klab HTML Tree View Generator</p>',
        html_content,
        flags=re.DOTALL
    )

    # Inject custom styles (Dark text on light gray background)
    custom_style = """
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root {
                --bg-color: #D3D3D3;
                --text-color: #000000;
                --border-color: #888888;
            }
            body {
                margin: 10px;
                color: var(--text-color);
                font-family: 'Arial', sans-serif;
                background-color: var(--bg-color);
            }
            a { text-decoration: none; }
            a[href$="/"] { color: blue; font-weight: bold; }
            a:not([href$="/"]) { color: black; }
        </style>
    """
    html_content = html_content.replace("<head>", f"<head>\n{custom_style}", 1)

    # Update links to open in `viewer.html` without `../`
    html_content = re.sub(
        r'<a href="([^"]+)"',
        r'<a target="_blank" href="__ktree/viewer.html?file=\1"',
        html_content
    )

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)

def setup_ktree_resources():
    """Creates `__ktree/` and copies required resources."""
    if not os.path.exists("__ktree"):
        os.mkdir("__ktree")

    # Copy `res/` folder
    dest_res_path = os.path.join("__ktree", "res")
    if os.path.exists(dest_res_path):
        shutil.rmtree(dest_res_path)
    shutil.copytree(RESOURCES_PATH, dest_res_path)

    # Copy `viewer.html`
    shutil.copy(VIEWER_HTML, os.path.join("__ktree", "viewer.html"))

def main():
    """Main function to handle arguments and execute tasks."""
    import sys
    args = sys.argv[1:]

    # Use current directory name as title if no arguments are given
    title = os.path.basename(os.getcwd()) if not args else args[0]
    ignore_patterns = args[1:]

    print(f"Generating website ...")
    generate_index_html(title, ignore_patterns)

    setup_ktree_resources()
    print(f"Ktree: Generated HTML treeview. Open 'index.html' to explore.")

if __name__ == "__main__":
    main()
