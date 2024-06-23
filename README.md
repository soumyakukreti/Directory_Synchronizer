# Directory_Synchronizer

Directory Synchronizer is a Python-based tool designed to synchronize directories between a local filesystem and an FTP server. It provides a user-friendly interface built with Streamlit, allowing users to perform various operations such as listing directory contents, uploading files, renaming files and directories, deleting files and directories, and synchronizing changes between the local and FTP directories.

## Features

- **List Directory Contents**: View the contents of directories both locally and on the FTP server.
- **Upload Files**: Select and upload files from the local directory to the FTP server.
- **Rename Files and Directories**: Easily rename files and directories both locally and on the FTP server.
- **Delete Files and Directories**: Remove files and directories that are no longer needed.
- **Synchronize Directories**: Keep the local and FTP directories in sync with the click of a button.

## Installation

To use Directory Synchronizer, you need to have Python installed on your system. If you do not have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

After installing Python, follow these steps to set up the Directory Synchronizer:

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required dependencies by running:

```sh
pip install -r requirements.txt
``` 
4. Start the Streamlit application:
```sh
streamlit run client.py
```
### Usage 
Upon launching the Directory Synchronizer, you will be greeted with a user-friendly interface where you can select the operation you wish to perform from a dropdown menu. The available options are:

- List directory contents
- Copy to local Directory
- Rename file
- Delete file
- Rename directory
- Delete directory
- Select the desired operation and follow the on-screen instructions to perform it.
