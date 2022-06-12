
import ftplib
import socket
import time
import os
from win32api import *
import re

startTime = time.time()

# TODO: 
#     pywinauto = Shutdown current running version of software
#     Run installer
#     Logging

def check_environment_variables() -> list[str]:
    """check if environment variables are set up
    """
    if os.getenv('ViperUser') != None and os.getenv('ViperAccess') != None:
        env_vars = [os.getenv('ViperHost'), os.getenv('ViperUser'), os.getenv('ViperAccess')]
        
        return env_vars
    
    print("Environment vars aren't set up properly")
    return []


def check_version_numbers(file_path: str, viper_installer: str) -> bool:
    """ Prints a version number that is installed
    """
    version = ".".join(get_version_number(file_path))
    
    print("Currently installed version: ", version)
    
    result = re.search(r"([a-zA-Z]{1}\d{1,2}\.\d{1,2}\.\d{1,3}\.\d{1,3})", viper_installer)
    
    print(viper_installer, result.group()[1:])
    print("version comparison checking...")
    
    if version != None:
        if version != result.group()[1:]:
            print(viper_installer)
            return True
        
        print("Already up to date")
    
    return False
    
      
def get_version_number(file_path) -> list[str]:
    """_summary_

    Args:
        file_path (_type_): requires path to exe for ex: C:\Program Files\My_App\myapp.exe

    Returns:
        list[str]: Version number in correct format
    """
    File_information = GetFileVersionInfo(file_path, "\\")
  
    if File_information != None:
        ms_file_version = File_information['FileVersionMS']
        ls_file_version = File_information['FileVersionLS']
  
        return [str(HIWORD(ms_file_version)), str(LOWORD(ms_file_version)),
                str(HIWORD(ls_file_version)), str(LOWORD(ls_file_version))]
    

def connect_to_ftp_server(ftp_server: ftplib.FTP) -> str:
    """_summary_

    Args:
        viper_installer (str): sets the string value to be the same as the current available for download

    Returns:
        ftplib.FTP: returns the current ftp connection.
    """
    env_vars = check_environment_variables()
    if env_vars != []:
        socket.getaddrinfo(env_vars[0], 8080)
        ftp_server = ftplib.FTP(env_vars[0], env_vars[1], env_vars[2])

        ftp_server.encoding = "utf-8"
    
        ftp_server.cwd("ViperVisionVersion4")
        
        listed = []
        ftp_server.dir(listed.append)
        
        viper_installer_name = listed[-1].split(' ')[-1].rstrip()
        
        print("Connected to server.")
        return viper_installer_name
    

def download_latest_version_vipervision(ftp_server: ftplib.FTP, viper_installer: str) -> str:
    """_summary_

    Args:
        ftp_server (ftplib.FTP): takes an ftp connection

    Returns:
        str: Starts download of the latest version of vipervision.
    """
    write_file_as_binary(ftp_server, viper_installer)
           
    return "Starting Download of: "


def write_file_as_binary(ftp_server: ftplib.FTP, filename: str):
    """_summary_

    Args:
        ftp_server (ftplib.FTP): current ftp connnection.
        filename (str): file name of version to be downloaded.
    """
    if ftp_server.pwd() != "ViperVisionVersion4":
        ftp_server.cwd("ViperVisionVersion4")
        with open(filename, "wb") as file:
            ftp_server.retrbinary(f"RETR {filename}", file.write)


def initialize_sequence():
    """Starts script/program
    """
    viper_vision_installer = ""
    file_path = r'C:\Program Files\Viper Imaging\ViperVision\ViperVision.exe'
    env_vars = check_environment_variables()
    
    if env_vars != []:
        socket.getaddrinfo(env_vars[0], 8080)
        ftp_server = ftplib.FTP(env_vars[0], env_vars[1], env_vars[2])
        
        viper_vision_installer = connect_to_ftp_server(ftp_server)
        if os.path.exists(file_path):
            if check_version_numbers(file_path, viper_vision_installer):
                print(download_latest_version_vipervision(ftp_server, viper_vision_installer), viper_vision_installer)
        else:
            print("Download for fresh install")
            print(viper_vision_installer)
            download_latest_version_vipervision(ftp_server, viper_vision_installer)   
        
        ftp_server.quit()


initialize_sequence()
executionTime = (time.time() - startTime)
print("completed in", executionTime)


