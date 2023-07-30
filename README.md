# markdown-toc-numbering

## What it does
- Number headings in markdown files:
    - Before:
        ```markdown
        # society
        ## politics
        ## economics
        # to do
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
        # 1 society
        ## 1.1 politics
        ## 1.2 economics
        # 2 to do
        # 3 academic
        ## 3.1 math
        ## 3.2 physics
        # 4 language
        ## 4.1 japanese
        ## 4.3 english
        ## 4.4 french
        ```
- Make tables of contents in markdown files
    - Before:
        ```markdown
        Title
        ===

        # 1 society
        ## 1.1 politics
        ## 1.2 economics
        # 2 to do
        # 3 academic
        ## 3.1 math
        ## 3.2 physics
        # 4 language
        ## 4.1 japanese
        ## 4.3 english
        ## 4.4 french
        ```
    - After:
        ```markdown
        Title
        ===
        <!-- Table of contents -->
        - [1 society](#1-society)
            - [1.1 politics](#1.1-politics)
            - [1.2 economics](#1.2-economics)
        - [2 to do](#2-to-do)
        - [3 academic](#3-academic)
            - [3.1 math](#3.1-math)
            - [3.2 physics](#3.2-physics)
        - [4 language](#4-language)
            - [4.1 japanese](#4.1-japanese)
            - [4.3 english](#4.3-english)
            - [4.4 french](#4.4-french)
        <!-- Table of contents -->

        # 1 society
        ## 1.1 politics
        ## 1.2 economics
        # 2 to do
        # 3 academic
        ## 3.1 math
        ## 3.2 physics
        # 4 language
        ## 4.1 japanese
        ## 4.3 english
        ## 4.4 french
        ```

## How to use
- Install
    ```bash
    pip install markdown beautifulsoup4
    ```
- `numbering.py` will number headings in all markdown files in the directory.
    ```bash
    python numbering.py add /path/to/directory
    ```
    - `add`: add numbers to headings
    - `remove`: remove numbers from headings

- `toc.py` will add tables of contents to all markdown files in the directory.
    ```bash
    python toc.py add /path/to/directory
    ```
    - `add`: add tables of contents
    - `remove`: remove tables of contents

## Note
This script assumes that the title is written in the first line using `===` as follows.
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


The table of contents will be added below the title using `<!-- Table of contents -->` and `<!-- Table of contents -->`.

## References:
- [vscode-markdown-header](https://github.com/panchaoxin/vscode-markdown-header/tree/master)