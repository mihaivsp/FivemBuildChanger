import subprocess
import os
import time
import requests


print(r"""
      
    _______                         ____        _ __    __   ________                               
   / ____(_)   _____  ____ ___     / __ )__  __(_) /___/ /  / ____/ /_  ____ _____  ____ ____  _____
  / /_  / / | / / _ \/ __ `__ \   / __  / / / / / / __  /  / /   / __ \/ __ `/ __ \/ __ `/ _ \/ ___/
 / __/ / /| |/ /  __/ / / / / /  / /_/ / /_/ / / / /_/ /  / /___/ / / / /_/ / / / / /_/ /  __/ /    
/_/   /_/ |___/\___/_/ /_/ /_/  /_____/\__,_/_/_/\__,_/   \____/_/ /_/\__,_/_/ /_/\__, /\___/_/     
                                                                                 /____/             

      """)

import requests

import requests

# GitHub repo information
GITHUB_OWNER = "mihaivsp"  # Replace with the GitHub repo owner
GITHUB_REPO = "FivemBuildChanger"    # Replace with the repository name
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"

# Hardcoded local version of the app
LOCAL_VERSION = "v0.0.1"  # Replace with your current app version

def clear_console():
    """
    Clears the console screen for Windows.
    """
    os.system('cls')  # Use 'cls' to clear the console on Windows

def get_latest_version():
    """
    Fetches the latest version information from the GitHub releases API.
    """
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        release_data = response.json()
        latest_version = release_data["tag_name"]
        return latest_version
    else:
        print(f"[-] Failed to fetch the latest release. Status code: {response.status_code}")
        print("")
        time.sleep(2)
        exit()
        return None


def compare_versions(local_version, latest_version):
    """
    Compares the local version with the latest GitHub release version.
    """
    if local_version == latest_version:
        print("[+] Your app is up to date!")
        time.sleep(2    )  # Show the message for 2 seconds
        clear_console()  # Clear the console after the message
        print(r"""
      
    _______                         ____        _ __    __   ________                               
   / ____(_)   _____  ____ ___     / __ )__  __(_) /___/ /  / ____/ /_  ____ _____  ____ ____  _____
  / /_  / / | / / _ \/ __ `__ \   / __  / / / / / / __  /  / /   / __ \/ __ `/ __ \/ __ `/ _ \/ ___/
 / __/ / /| |/ /  __/ / / / / /  / /_/ / /_/ / / / /_/ /  / /___/ / / / /_/ / / / / /_/ /  __/ /    
/_/   /_/ |___/\___/_/ /_/ /_/  /_____/\__,_/_/_/\__,_/   \____/_/ /_/\__,_/_/ /_/\__, /\___/_/     
                                                                                 /____/             

      """)

    else:
        print(f"[*] A new version is available: {latest_version}")
        print("")
        print(f"[*] Please update your app from version {local_version} to {latest_version}")
        print("")
        time.sleep(2)
        exit()


def main():
    # Step 1: Print the current local version of the app
    print(f"[*] Local version: {LOCAL_VERSION}")
    print("")

    # Step 2: Get the latest version from GitHub
    latest_version = get_latest_version()
    if not latest_version:
        return

    print(f"[*] Latest version: {latest_version}")
    print("")

    # Step 3: Compare versions
    compare_versions(LOCAL_VERSION, latest_version)


if __name__ == "__main__":
    main()



def find_fivem_path():
    """
    Attempt to find the FiveM installation path by searching common installation directories.
    If not found, prompt the user for the directory.
    """
    # Common installation directories
    common_paths = [
        r"C:\Program Files\FiveM\FiveM.exe",
        r"C:\Program Files (x86)\FiveM\FiveM.exe",
        r"C:\Fivem\Fivem.exe",
        r"D:\Fivem\Fivem.exe",
        os.path.join(os.getenv('LOCALAPPDATA'), r"FiveM\FiveM.exe")
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    # If not found, ask the user for the directory
    user_provided_path = input(r"""[/] FiveM executable not found. Please enter the full path to your FiveM executable : """)
    
    # Check if the user-provided path exists
    if os.path.exists(user_provided_path) and os.path.isfile(user_provided_path):
        return user_provided_path
    else:
        print(r"""[-] The provided path is not valid or the file does not exist.
                                             """)
        return None

def launch_fivem_with_build_and_pure_mode(build_number, pure_mode):
    # Find FiveM path
    fivem_path = find_fivem_path()

    if fivem_path is None:
        print(r"""[-] Could not find the FiveM installation. Please check if it's installed correctly.
                                                           """)
        return

    # Command to launch FiveM with the specified build number and pure mode
    command = [fivem_path, f"-b{build_number}", f"-pure_{pure_mode}"]
    print("""
[+] Fivem is Launching, Have Fun!""")

    time.sleep(1)

    try:
        # Run the command to launch FiveM
        subprocess.Popen(command)
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to launch FiveM: {e}")

# Get the build number from the user
build = input(r"""                  
[/] Enter the build number you want to launch : """)


# Get the pure mode from the user
pure_mode = input(r"""
[/] Enter the pure mode you want to use : """)

# Call the function to launch FiveM with build and pure mode
launch_fivem_with_build_and_pure_mode(build, pure_mode)

time.sleep(2)
