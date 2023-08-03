import argparse
import os
import re
from pathlib import Path

HEADER_MARK = "#"
HEADER_PATTERN = f"^{HEADER_MARK}+\\s+(([\\d,\\.])+\\s+)?"
MAX_LEVEL = 6


# Count the number of header marks at the beginning of a line
def count_header_mark(line):
    count = 0
    for c in line:
        if c == HEADER_MARK:
            count += 1
        else:
            break
    return count


# add number to header line
def generate_number(line, level_order):
    reg = re.compile(HEADER_PATTERN)
    if not reg.search(line):
        return line

    level = count_header_mark(line)
    new_line = '#' * level + ' '
    for i in range(1, level + 1):
        if level_order[i] == 0:
            level_order[i] = 1
        if i != level:
            new_line += f"{level_order[i]}."
        else:
            new_line += f"{level_order[i]}"
    new_line += ' '
    new_line += line[reg.search(line).end():]
    return new_line


# Internal function to add numbered headers to a Markdown file
def generate_header_number_internal(lines):
    is_in_code_area = False
    last_level = -1
    level_order = [0] * (MAX_LEVEL + 1)

    for i, line in enumerate(lines):
        if line.startswith("```"):
            is_in_code_area = not is_in_code_area
            continue

        if not is_in_code_area and line.startswith(HEADER_MARK):
            level = count_header_mark(line)
            if level > MAX_LEVEL:
                raise ValueError(f'"{line[:10]}..." Level of header cannot exceed {MAX_LEVEL}')
            if level < last_level:
                level_order[level + 1:last_level + 1] = [0] * (last_level - level)
            last_level = level
            level_order[level] += 1
            lines[i] = generate_number(line, level_order)


# Internal function to remove numbered headers from a Markdown file
def remove_header_number_internal(lines):
    is_in_code_area = False
    
    for i, line in enumerate(lines):
        if line.startswith("```"):
            is_in_code_area = not is_in_code_area
            continue

        if not is_in_code_area and line.startswith(HEADER_MARK):
            reg = re.compile(HEADER_PATTERN)
            level = count_header_mark(line)
            if level == 0:
                continue
            line = reg.sub('', line)
            prefix = '#' * level + ' '
            lines[i] = prefix + line


# Function to add numbered headers to markdown contents
def generate_header_number(content):
    lines = content.split("\n")
    generate_header_number_internal(lines)
    return "\n".join(lines)


# Function to remove numbered headers from markdown contents
def remove_header_number(content):
    lines = content.split("\n")
    remove_header_number_internal(lines)
    return "\n".join(lines)


# Function to read content from a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# Function to write content to a file
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


# Function to add numbered headers to a Markdown file
def add_header_numbers_to_file(file_path):
    content = read_file(file_path)
    modified_content = generate_header_number(content)
    write_file(file_path, modified_content)


# Function to remove numbered headers from a Markdown file
def remove_header_numbers_from_file(file_path):
    content = read_file(file_path)
    modified_content = remove_header_number(content)
    write_file(file_path, modified_content)


# Function to process all Markdown files in a directory
def process_markdown_files(directory_path, add_header_numbers=True):
    for file_path in Path(directory_path).rglob('*.md'):
        file_path = str(file_path)  # Convert Path object to string
        if not os.path.islink(file_path):
            if add_header_numbers:
                add_header_numbers_to_file(file_path)
            else:
                remove_header_numbers_from_file(file_path)
        else:
            pass


# Function to run the script based on command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Add or remove header numbers from Markdown files.")
    parser.add_argument("action", choices=["add", "remove", "update"],
                        help="Choose the action: 'add_header_numbers' or 'remove_header_numbers'")
    parser.add_argument("directory_path", help="The path to the target directory containing Markdown files.")
    args = parser.parse_args()

    target_directory = args.directory_path

    if args.action == "add":
        process_markdown_files(target_directory, add_header_numbers=True)
        print("Header numbers added successfully!")
    elif args.action == "remove":
        process_markdown_files(target_directory, add_header_numbers=False)
        print("Header numbers removed successfully!")
    elif args.action == "update":
        process_markdown_files(target_directory, add_header_numbers=False)
        process_markdown_files(target_directory, add_header_numbers=True)
        print("Header numbers updated successfully!")
    else:
        print("Invalid action. Please specify 'add' or 'remove' or 'update'.")
        

if __name__ == "__main__":
    main()
