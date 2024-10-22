# Document360 to Docusaurus Migration Tool

This project provides a migration tool that helps you migrate documentation from Document360 to Docusaurus. The tool extracts, restructures, and converts documentation, enabling a seamless transition while maintaining the organization and content quality.

## Features
- Graphical User Interface (GUI): Easily select the export file and output directory through an interactive GUI using Tkinter.
- File Extraction and Restructuring: Extracts ZIP files exported from Document360, organizes content according to the specified structure.
- HTML to Markdown Conversion: Converts HTML articles into Markdown format for Docusaurus compatibility using BeautifulSoup.
- Content Sanitization: Cleans up the Markdown files by removing unnecessary tags and metadata to create a clean and well-structured documentation set.
- Progress Tracking: The tool provides a progress bar to track the migration process from start to finish.

## How to Use
- Select Document360 Export File: Upload the ZIP file exported from Document360.
- Choose Output Directory: Choose where you want the migrated documentation to be saved.
- Start Migration: Click the "Start Migration" button and monitor the progress via the progress bar.

## Requirements
- Python 3.7+

### Dependencies:
- BeautifulSoup4
- tkinter (included in standard Python library)
- PyInstaller (for building an executable, if needed)

## Installation

To run the script locally, clone the repository: `git clone https://github.com/yourusername/document360-to-docusaurus.git`

## Install dependencies:

`pip install -r requirements.txt`

## Run the migration tool:

`python migration_tool.py`

Building an Executable

To distribute this tool as an executable, use PyInstaller:

`pyinstaller --onefile --windowed migration_tool.py`

This will create a standalone executable that can be run on any compatible machine without needing Python.
Contributing

***

Contributions are welcome! If you have ideas for features or improvements, feel free to fork the repository and submit a pull request.
License

***

This project is licensed under the MIT License

This project is licensed under the MIT License.
