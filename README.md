# markdown-toc-numbering

## What it does
- Number headings in markdown files:
    - Before:
        ```markdown
        # society
        ## politics
        ## economics
        # to Do
        # academic
        ## math
        ## physics
        # language
        ## japanese
        ## english
        ## french
        ```
    - After:
        ```markdown
        # 1. society
        ## 1.1. politics
        ## 1.2. economics
        # 2. to do
        # 3. academic
        ## 3.1. math
        ## 3.2. physics
        # 4. language
        ## 4.1. japanese
        ## 4.3. english
        ## 4.4. french
        ```
- Make a table of contents in markdown files
    - Before:
        ```markdown
        Title
        ===

        # 1. society
        ## 1.1. politics
        ## 1.2. economics
        # 2. to do
        # 3. academic
        ## 3.1. math
        ## 3.2. physics
        # 4. language
        ## 4.1. japanese
        ## 4.3. english
        ## 4.4. french
        ```
    - After:
        ```markdown
        Title
        ===
        <!-- Table of contents -->
        - [1. society](#1society)
            - [1.1. politics](#11politics)
            - [1.2. economics](#12economics)
        - [2. to do](#2todo)
        - [3. academic](#3academic)
            - [3.1. math](#31math)
            - [3.2. physics](#32physics)
        - [4. language](#4language)
            - [4.1. japanese](#41japanese)
            - [4.3. english](#43english)
            - [4.4. french](#44french)
        <!-- Table of contents -->

        # 1. society
        ## 1.1. politics
        ## 1.2. economics
        # 2. to do
        # 3. academic
        ## 3.1. math
        ## 3.2. physics
        # 4. language
        ## 4.1. japanese
        ## 4.3. english
        ## 4.4. french
        ```

## How to use
- Install
    ```bash
    pip install markdown beautifulsoup4
    ```
- Add numbering to headings. This script will add numbering to headings in all markdown files in the directory.
    ```bash
    python numbering.py add /path/to/directory
    ```
    - `add`: add numbering to headings
    - `remove`: remove numbering from headings

- Add table of contents. This script will add table of contents to all markdown files in the directory.
    ```bash
    python toc.py add /path/to/directory
    ```
    - `add`: add table of contents
    - `remove`: remove table of contents

## Note
This script assumes that markdown files has the following format:
```markdown
Title
===

# heading1
## heading1.1
## heading1.2
# heading2
## heading2.1
## heading2.2
```

The title is written in the first line using `===`.

The table of contents is written below the title using `<!-- Table of contents -->` and `<!-- Table of contents -->`.

References:
- [vscode-markdown-header](https://github.com/panchaoxin/vscode-markdown-header/tree/master)