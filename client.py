import os
import streamlit as st
from sync import sync_directories, get_ftp_connection

path = "/Users/siddharth/Desktop/news"
ftp_directory = "/"

def list_directory_local(path):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                col1.write("📄 " + entry.name)
            elif entry.is_dir():
                col1.write("📁 " + entry.name)

def list_directory_ftp():
    ftp = get_ftp_connection()
    file_list = ftp.nlst()
    for file in file_list:
        col2.write("📄 " + file)

def upload_file():
    file = st.file_uploader("Choose a file to upload")
    if file is not None:
        file_name = file.name
        with open(os.path.join(path, file_name), "wb") as f:
            f.write(file.getbuffer())
        st.success(f"File '{file_name}' uploaded successfully.")

def rename_file():
    old_name = st.text_input("Enter the old name of the file:")
    new_name = st.text_input("Enter the new name of the file:")
    old_path = os.path.join(path, old_name)
    new_path = os.path.join(path, new_name)
    try:
        os.rename(old_path, new_path)
        st.success(f"File '{old_name}' renamed to '{new_name}' successfully.")
    except IsADirectoryError:
        if new_name == "":
            pass
    except FileNotFoundError:
        st.error(f"File '{old_name}' not found in directory.")

def delete_file():
    file_name = st.text_input("Enter the name of the file to delete:")
    file_path = os.path.join(path, file_name)
    # Check if file path is not empty
    if file_path:
        try:
            os.remove(file_path)
            st.success("File deleted successfully!")
        except PermissionError:
            st.success("Enter the file name with extension.")
        except FileNotFoundError:
            st.error("Error: File not found.")
        except:
            st.error("An unknown error occurred.")

def rename_directory():
    old_name = st.text_input("Enter the old name of the directory:")
    new_name = st.text_input("Enter the new name of the directory:")
    old_path = os.path.join(path, old_name)
    new_path = os.path.join(path, new_name)
    try:
        os.rename(old_path, new_path)
        st.success(f"Directory '{old_name}' renamed to '{new_name}' successfully.")
    except FileNotFoundError:
        st.error(f"Directory '{old_name}' not found in directory.")

def delete_directory():
    dir_name = st.text_input("Enter the name of the directory to delete:")
    dir_path = os.path.join(path, dir_name)
    try:
        os.rmdir(dir_path)
        st.success(f"Directory '{dir_name}' deleted successfully.")
    except FileNotFoundError:
        st.error(f"Directory '{dir_name}' not found in directory.")
    except OSError:
        if dir_name == "":
            st.success("Enter the name of the directory to delete.")
        else:
            st.error(f"Directory '{dir_name}' is not empty.")



def syncButton():
    if st.button('Sync Changes'):
        try:
            sync_directories(path, ftp_directory)
            st.write('Changes synchronized successfully.')
        except Exception as e:
            st.write(f'Error occurred: {str(e)}')


st.header("Welcome User!")
options = ["List directory contents", "Copy to local Directory", "Rename file", "Delete file", "Rename directory", "Delete directory"]

choice = st.selectbox("Select an option:", options)
col1, col2 = st.columns(2)
if choice == "List directory contents":
    col1.success("Local directory: " "📁 " + path)
    col2.success("FTP directory: " "📁 " + ftp_directory)
    list_directory_local(path)
    list_directory_ftp()
    syncButton()

elif choice == "Copy to local Directory":
    upload_file()
    syncButton()
    
elif choice == "Rename file":
    rename_file()
    syncButton()

elif choice == "Delete file":
    delete_file()
    syncButton()

elif choice == "Rename directory":
    rename_directory()
    syncButton()

elif choice == "Delete directory":
    delete_directory()
    syncButton()
    

