import argparse
import re
from pathlib import Path

HEADER_MARK = "#"
HEADER_PATTERN = f"^{HEADER_MARK}+\\s+(([\\d,\\.])+\\s+)?"


def generate_unique_anchor(heading_text):
    # Generate a unique anchor link based on the heading text
    # Remove non-word characters, convert to lowercase, and replace spaces with hyphens
    anchor = re.sub(r'[\s]+', '-', heading_text.lower())
    # Remove any trailing hyphens
    anchor = anchor.strip('-')
    return anchor


def count_header_mark(line):
    count = 0
    for c in line:
        if c == HEADER_MARK:
            count += 1
        else:
            break
    return count


def generate_table_of_contents(md_content):
    lines = md_content.split("\n")
    
    toc_lines = []
    
    is_in_code_area = False

    for i, line in enumerate(lines):
        if line.startswith("```"):
            is_in_code_area = not is_in_code_area
            continue
            
        if not is_in_code_area and line.startswith(HEADER_MARK):
            header_match = re.match(HEADER_PATTERN, line)
            if header_match:
                header_level = count_header_mark(line)
                header_text = line[header_level:].strip()
                anchor = generate_unique_anchor(header_text)
                toc_entry = f"{' ' * (header_level - 1) * 4}- [{header_text}](#{anchor})"
                toc_lines.append(toc_entry)
            
    return "\n".join(toc_lines)


def add_table_of_contents(md_content, toc_marker):
    # Check if the table of contents already exists between markers
    if toc_marker in md_content:
        print("Table of contents already exists between markers. Skipping...")
        return md_content

    # Find the pattern for the title, e.g., "title\n==="
    title_pattern = r"^(.*)===$"
    title_match = re.search(title_pattern, md_content, re.MULTILINE)

    if title_match:
        # Use the title from the markdown file and insert the table of contents
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
    parser.add_argument("action_to_perform", choices=["add", "remove", "update"], help="Action to perform: 'add' or 'remove' the table of contents.")
    parser.add_argument("directory_path", help="Path to the directory containing the Markdown files.")
    args = parser.parse_args()

    action_to_perform = args.action_to_perform
    directory_path = args.directory_path

    # Define the table of contents markers
    toc_marker = "<!-- Table of contents -->"

    if action_to_perform == 'add':
        process_files_in_directory(directory_path, action_to_perform)
        print("Table of contents added successfully!")
    elif action_to_perform == 'remove':
        process_files_in_directory(directory_path, action_to_perform)
        print("Table of contents removed successfully!")
    elif action_to_perform == 'update':
        process_files_in_directory(directory_path, 'remove')
        process_files_in_directory(directory_path, 'add')
        print("Table of contents updated successfully!")
    else:
        print("Invalid action. Please specify 'add' or 'remove' or 'update'.")
