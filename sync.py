import os
from ftplib import FTP


local_path = ""
ftp_path = ""

def get_ftp_connection():
    ftp = FTP()
    ftp.connect("127.0.0.1", 2121)
    ftp.login("user", "password")
    return ftp


def list_local_directory(path):
    return os.listdir(path)


def list_ftp_directory(path, ftp):
    ftp.cwd(path)
    return ftp.nlst()


def upload_file(file_path, ftp_path, ftp):
    with open(file_path, 'rb') as f:
        ftp.storbinary(f'STOR {ftp_path}', f)


def upload_directory(local_path, ftp_path, ftp):
    try:
        ftp.mkd(ftp_path)
    except:
        pass
    for file_name in os.listdir(local_path):
        local_file_path = os.path.join(local_path, file_name)
        ftp_file_path = os.path.join(ftp_path, file_name)
        if os.path.isfile(local_file_path):
            upload_file(local_file_path, ftp_file_path, ftp)
        else:
            upload_directory(local_file_path, ftp_file_path, ftp)


def sync_directories(local_path, ftp_path):
    ftp = get_ftp_connection()
    local_files = set(list_local_directory(local_path))
    ftp_files = set(list_ftp_directory(ftp_path, ftp))
    # upload new files to FTP server
    for file_name in local_files - ftp_files:
        local_file_path = os.path.join(local_path, file_name)
        ftp_file_path = os.path.join(ftp_path, file_name)
        if os.path.isfile(local_file_path):
            upload_file(local_file_path, ftp_file_path, ftp)
        else:
            upload_directory(local_file_path, ftp_file_path, ftp)
    # delete removed files from FTP server
    for file_name in ftp_files - local_files:
        ftp_file_path = os.path.join(ftp_path, file_name)
        try:
            ftp.delete(ftp_file_path)
        except:
            ftp.rmd(ftp_file_path)
    # rename files on FTP server
    for file_name in local_files.intersection(ftp_files):
        local_file_path = os.path.join(local_path, file_name)
        ftp_file_path = os.path.join(ftp_path, file_name)
        if os.path.isdir(local_file_path):
            sync_directories(local_file_path, ftp_file_path)
        else:
            try:
                old_file_name = get_old_file_name(local_file_path, ftp_path, ftp)
                ftp.rename(old_file_name, ftp_file_path)
            except:
                upload_file(local_file_path, ftp_file_path, ftp)
    ftp.quit()


def get_old_file_name(local_file_path, ftp_path, ftp):
    file_name = os.path.basename(local_file_path)
    for ftp_file_name in list_ftp_directory(ftp_path, ftp):
        if ftp_file_name.lower() == file_name.lower():
            return os.path.join(ftp_path, ftp_file_name)
    raise Exception(f'Could not find old file name for {local_file_path}')


