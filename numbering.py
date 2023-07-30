import argparse
import os
import re


class MarkdownHeader:
    HEADER_MARK = "#"
    HEADER_PATTERN = f"^{HEADER_MARK}+\\s+(([\\d,\\.])+\\s+)?"
    MAX_LEVEL = 6

    @staticmethod
    def count_header_mark(line):
        count = 0
        for c in line:
            if c == MarkdownHeader.HEADER_MARK:
                count += 1
            else:
                break
        return count

    @staticmethod
    def generate_number(line, level_order):
        reg = re.compile(MarkdownHeader.HEADER_PATTERN)
        if not reg.search(line):
            return line

        level = MarkdownHeader.count_header_mark(line)
        new_line = '#' * level + ' '
        for i in range(1, level + 1):
            if level_order[i] == 0:
                level_order[i] = 1
            if i != level:
                new_line += f"{level_order[i]}."
            else:
                new_line += f"{level_order[i]}"
        # start with index 0 for level 1
        # if level == 1:
        #     for i in range(1, level + 1):
        #         if level_order[i] == 0:
        #             level_order[i] = 1
        #         new_line += f"{level_order[i]-1}."
        # else:
        #     for i in range(1, level + 1):
        #         if level_order[i] == 0:
        #             level_order[i] = 1
        #         new_line += f"{level_order[i]}."
        new_line += ' '
        new_line += line[reg.search(line).end():]
        return new_line

    @staticmethod
    def remove_number(line):
        reg = re.compile(MarkdownHeader.HEADER_PATTERN)
        level = MarkdownHeader.count_header_mark(line)
        if level == 0:
            return line
        line = reg.sub('', line)
        prefix = '#' * level + ' '
        return prefix + line

    @staticmethod
    def generate_header_number_internal(lines):
        is_in_code_area = False
        last_level = -1
        level_order = [0] * (MarkdownHeader.MAX_LEVEL + 1)

        for i, line in enumerate(lines):
            if line.startswith("```"):
                is_in_code_area = not is_in_code_area
                continue

            if not is_in_code_area and line.startswith(MarkdownHeader.HEADER_MARK):
                level = MarkdownHeader.count_header_mark(line)
                if level > MarkdownHeader.MAX_LEVEL:
                    raise ValueError(f'"{line[:10]}..." Level of header cannot exceed {MarkdownHeader.MAX_LEVEL}')
                if level < last_level:
                    level_order[level + 1:last_level + 1] = [0] * (last_level - level)
                last_level = level
                level_order[level] += 1
                lines[i] = MarkdownHeader.generate_number(line, level_order)

    @staticmethod
    def generate_header_number(content):
        lines = content.split("\n")
        MarkdownHeader.generate_header_number_internal(lines)
        return "\n".join(lines)

    @staticmethod
    def remove_header_number(content):
        lines = content.split("\n")
        for i in range(len(lines)):
            lines[i] = MarkdownHeader.remove_number(lines[i])
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
    modified_content = MarkdownHeader.generate_header_number(content)
    write_file(file_path, modified_content)


# Function to remove numbered headers from a Markdown file
def remove_header_numbers_from_file(file_path):
    content = read_file(file_path)
    modified_content = MarkdownHeader.remove_header_number(content)
    write_file(file_path, modified_content)


# Function to process all Markdown files in a directory
def process_markdown_files(directory_path, add_header_numbers=True):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                if add_header_numbers:
                    add_header_numbers_to_file(file_path)
                else:
                    remove_header_numbers_from_file(file_path)


# Function to run the script based on command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Add or remove header numbers from Markdown files.")
    parser.add_argument("action", choices=["add", "remove"],
                        help="Choose the action: 'add_header_numbers' or 'remove_header_numbers'")
    parser.add_argument("directory_path", help="The path to the target directory containing Markdown files.")
    args = parser.parse_args()

    target_directory = args.directory_path

    if args.action == "add":
        process_markdown_files(target_directory, add_header_numbers=True)
    else:
        process_markdown_files(target_directory, add_header_numbers=False)

if __name__ == "__main__":
    main()
