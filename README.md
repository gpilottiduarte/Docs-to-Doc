# Documentation Migration and Conversion Tools

This repository contains three useful scripts for documentation migration and conversion, developed to facilitate content transition and file standardization in projects. All scripts are distributed under the MIT license, including the source code and the executable (.exe) releases.

## Table of Contents

- [General Description](#general-description)
- [Included Scripts](#included-scripts)
    - [1. Migration from Document360 to Docusaurus](#1-migration-from-document360-to-docusaurus)
    - [2. Cleaning Markdown Files](#2-cleaning-markdown-files)
    - [3. HTML to Markdown Conversion](#3-html-to-markdown-conversion)
- [Installation and Usage](#installation-and-usage)
    - [Prerequisites](#prerequisites)
    - [Running the Executables](#running-the-executables)
    - [Running the Python Scripts](#running-the-python-scripts)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)
- [Contributions](#contributions)
- [Version History](#version-history)
- [Issues](#issues)
- [Screenshots](#screenshots)
    - [Migration from Document360 to Docusaurus](#migration-from-document360-to-docusaurus)
    - [Cleaning Markdown Files](#cleaning-markdown-files)
    - [HTML to Markdown Conversion](#html-to-markdown-conversion)
- [FAQs](#faqs)
- [Dependencies Used](#dependencies-used)
- [Best Practices](#best-practices)
- [Author](#author)

---

## General Description

The scripts in this repository assist with common documentation-related tasks, such as migrating structures, cleaning metadata, and converting formats. They are designed to be user-friendly, with intuitive graphical interfaces that allow interaction without the need for advanced programming knowledge.

---

## Included Scripts

### 1. Migration from Document360 to Docusaurus

**File:** `migracao_documentacao.py`

This script facilitates the migration of documentation from **Document360** to **Docusaurus**. It:

- **Extracts** the ZIP file exported from Document360.
- **Locates** and loads the JSON file with the structure of categories and articles.
- **Creates** the corresponding directory structure in the format expected by Docusaurus.
- **Moves** the articles to the appropriate folders as defined in the JSON.
- **Presents** a progress bar to monitor the process.

**How to use:**

1. **Select the ZIP file** exported from Document360.
2. **Choose the destination directory** where the new structure will be created.
3. **Start the migration** and wait for completion.

### 2. Cleaning Markdown Files

**File:** `limpar_markdown_gui.py`

This script processes Markdown files to remove a specific header (frontmatter) and add an H1 title based on the title value extracted from the header.

- **Removes** the metadata block between `## Metadata_Start` and `## Metadata_End`.
- **Extracts** the value of the `title:` tag from the header.
- **Adds** an H1 title at the beginning of the file with the extracted value.
- **Processes** all Markdown files in a selected directory, including subdirectories.

**How to use:**

1. **Select the folder** containing the Markdown files to be processed.
2. **Start the cleaning** and monitor the progress via the progress bar.

### 3. HTML to Markdown Conversion

**File:** `converter_html_para_markdown.py`

This script converts HTML files into Markdown files while preserving all the original formatting, including lists, bold text, tables, etc. It also removes commented metadata blocks.

- **Removes** the commented metadata block between `<!-- ## Metadata_Start` and `## Metadata_End -->`.
- **Converts** the HTML content to Markdown, maintaining formatting.
- **Generates** corresponding Markdown files, keeping the original HTML files intact.
- **Processes** all HTML files in a selected directory, including subdirectories.

**How to use:**

1. **Select the folder** containing the HTML files to be converted.
2. **Start the conversion** and monitor the progress via the progress bar.

---

## Installation and Usage

### Prerequisites

To run the **executables** (.exe):

- **Windows 7** or higher.
- No additional installation is required.

To run the **Python scripts**:

- **Python 3.6** or higher installed.
- Install the necessary dependencies (see below).

### Running the Executables

1. **Download** the executables (.exe) from the releases section of this repository.
2. **Run** the downloaded file corresponding to the script you wish to use.
3. **Follow** the instructions presented in the graphical interface.

### Running the Python Scripts

1. **Clone** this repository or download the individual scripts.
2. **Install** the necessary dependencies: ``pip install -r requirements.txt
3. **Run** the desired script: `python script_name.py`
***
## Acknowledgments

Thank you for using these tools. If you have any questions or encounter any issues, feel free to open an issue or contribute improvements.

---

## Contact

- **Author:** Your Name
- **Email:** paulo@paulogpd.com.br
- **Website:** [paulogpd.com.br](http://www.paulogpd.com.br)

---

## Contributions

Contributions are welcome! Feel free to open pull requests with improvements, bug fixes, or new features.

---

## Version History

See the version history in the releases section of this repository for details on changes in each version.

---

## Issues

If you encounter any problems or have suggestions, please open an issue in the repository.

---

## Screenshots

### Migration from Document360 to Docusaurus

![](https://github.com/mtgr18977/Docs-to-Doc/blob/main/mapping_json.png)

### Cleaning Markdown Files

![](https://github.com/mtgr18977/Docs-to-Doc/blob/main/limpa_md.png)

### HTML to Markdown Conversion

![](https://github.com/mtgr18977/Docs-to-Doc/blob/main/convert_hml.png)

---

## FAQs

**1. Do the executables work on operating systems other than Windows?**

Currently, the provided executables are for Windows. For other operating systems, we recommend running the Python scripts directly.

**2. Do I need Python installed to use the executables?**

No, the executables include all the necessary dependencies.

**3. How do I add functionalities to the scripts?**

You can modify the Python scripts as needed. Feel free to contribute improvements via pull requests.

---

## Dependencies Used

- **Python 3**
- **Tkinter**: Python's standard library for graphical interfaces.
- **markdownify**: Used to convert HTML to Markdown.
- **beautifulsoup4**: Used for HTML parsing.
- **logging**: For logging information and errors during execution.

---

## Best Practices

- **Backup**: Always back up your files before performing batch operations.
- **Testing**: Test the scripts on a small set of files before processing large volumes.
- **Virtual Environments**: When running the Python scripts, consider using virtual environments to manage dependencies.

---

## Author

Developed by myself (PauloGPD) ;D
