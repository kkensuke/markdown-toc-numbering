import argparse
import os
import re
from pathlib import Path

import markdown
from bs4 import BeautifulSoup


def generate_unique_anchor(heading_text):
    # Generate a unique anchor link based on the heading text
    anchor = re.sub(r'[^\w\-]+', '', heading_text.lower())
    return anchor


def generate_table_of_contents(md_content):
    # Convert Markdown to HTML
    md_html = markdown.markdown(md_content)
    
    # Parse the HTML content
    soup = BeautifulSoup(md_html, 'html.parser')
    
    toc_lines = []
    
    # Keep track of whether the first heading has been encountered
    first_heading_encountered = False
    
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        # Skip the first heading
        if not first_heading_encountered:
            first_heading_encountered = True
            continue
        
        # Get the heading level (h1, h2, etc.)
        heading_level = int(heading.name[1])
        
        # Get the text of the heading
        heading_text = heading.get_text(strip=True)
        
        # Create a unique anchor link for the heading
        anchor = generate_unique_anchor(heading_text)
        
        # Create the table of contents entry with appropriate indentation
        toc_entry = f"{' ' * (heading_level - 1) * 2}- [{heading_text}](#{anchor})"
        toc_lines.append(toc_entry)
        
        # Add the unique anchor link to the heading
        heading['id'] = anchor
    
    return "\n".join(toc_lines)


def add_table_of_contents(md_content, toc_marker):
    # Check if the table of contents already exists between markers
    if toc_marker in md_content:
        print("Table of contents already exists between markers. Skipping...")
        return md_content

    # Find the pattern for the title, e.g., "title\n==="
    title_pattern = r"^(.+)\n===$"
    title_match = re.search(title_pattern, md_content, re.MULTILINE)

    if title_match:
        # Use the custom title and insert the table of contents below it
        custom_title = title_match.group(1).strip()
        toc = generate_table_of_contents(md_content)
        title_end = title_match.end()
        updated_content = f"{md_content[:title_end]}\n{toc_marker}\n{toc}\n{toc_marker}{md_content[title_end:]}"
    else:
        # Use the default title and insert the table of contents
        default_title = "Title"
        toc = generate_table_of_contents(md_content)
        updated_content = f"{default_title}\n===\n{toc_marker}\n{toc}\n{toc_marker}{md_content}"

    return updated_content


def remove_table_of_contents(md_content, toc_marker):
    # Check if the table of contents exists between markers
    if toc_marker in md_content:
        # Find the start and end positions of the table of contents
        toc_start = md_content.find(toc_marker)
        toc_end = md_content.find(toc_marker, toc_start + len(toc_marker))
        
        if toc_end != -1:
            # Remove the table of contents along with the markers
            updated_content = md_content[:toc_start].strip() + md_content[toc_end + len(toc_marker):]
        else:
            print("Table of contents markers found, but not in pair. Skipping removal.")
            return md_content
    else:
        print("Table of contents not found between markers. Nothing to remove.")
        return md_content

    return updated_content


def process_files_in_directory(directory_path, action):
    # Define the table of contents markers
    toc_marker = "<!-- Table of contents -->"

    for file_path in Path(directory_path).rglob('*.md'):
        file_path = str(file_path)  # Convert Path object to string

        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()

        if action == 'add':
            md_content = add_table_of_contents(md_content, toc_marker)
        elif action == 'remove':
            md_content = remove_table_of_contents(md_content, toc_marker)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(md_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add or remove table of contents in Markdown files.")
    parser.add_argument("action_to_perform", choices=["add", "remove"], help="Action to perform: 'add' or 'remove' the table of contents.")
    parser.add_argument("directory_path", help="Path to the directory containing the Markdown files.")
    args = parser.parse_args()

    action_to_perform = args.action_to_perform
    directory_path = args.directory_path

    # Define the table of contents markers
    toc_marker = "<!-- Table of contents -->"

    if action_to_perform == 'add':
        process_files_in_directory(directory_path, action_to_perform)
        print("Table of contents added successfully to all Markdown files in the directory and its subdirectories.")
    elif action_to_perform == 'remove':
        process_files_in_directory(directory_path, action_to_perform)
        print("Table of contents removed successfully from all Markdown files in the directory and its subdirectories.")


# Usage:
# python main.py add /path/to/your/directory
# python main.py remove /path/to/your/directory