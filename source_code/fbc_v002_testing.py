import subprocess
import os
import time
import requests
import shutil

# ASCII Art Logo
print(r"""
      
    _______                         ____        _ __    __   ________                               
   / ____(_)   _____  ____ ___     / __ )__  __(_) /___/ /  / ____/ /_  ____ _____  ____ ____  _____
  / /_  / / | / / _ \/ __ `__ \   / __  / / / / / / __  /  / /   / __ \/ __ `/ __ \/ __ `/ _ \/ ___/
 / __/ / /| |/ /  __/ / / / / /  / /_/ / /_/ / / / /_/ /  / /___/ / / / /_/ / / / / /_/ /  __/ /    
/_/   /_/ |___/\___/_/ /_/ /_/  /_____/\__,_/_/_/\__,_/   \____/_/ /_/\__,_/_/ /_/\__, /\___/_/     
                                                                                 /____/             

      """)

# GitHub repo information
GITHUB_OWNER = "mihaivsp"
GITHUB_REPO = "FivemBuildChanger"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"

# Hardcoded local version of the app
LOCAL_VERSION = "v0.0.2_testing"  # Replace with your current app version

def clear_console():
    """ Clears the console screen for Windows and Unix-based systems."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_latest_version():
    """ Fetches the latest version information from the GitHub releases API."""
    try:
        response = requests.get(GITHUB_API_URL, timeout=10)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        release_data = response.json()
        return release_data.get("tag_name"), release_data.get("assets", [])
    except requests.exceptions.RequestException as e:
        print(f"[-] Failed to fetch the latest release: {e}")
        return None, None

def download_asset(asset_url, asset_name):
    """ Downloads the release asset to the user's Downloads folder."""
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_folder, asset_name)
    
    try:
        print(f"[+] Downloading {asset_name} to {downloads_folder} ...")
        with requests.get(asset_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print(f"[+] Successfully downloaded {asset_name}")
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"[-] Failed to download {asset_name}: {e}")
        return None

def compare_versions_and_update(local_version, latest_version, assets):
    """ Compares local and latest versions. If outdated, downloads the latest version."""
    if local_version == latest_version:
        print("[+] Your app is up to date!")
        time.sleep(2)
        clear_console()
    else:
        print(f"[*] A new version is available: {latest_version}")
        if assets:
            asset = assets[0]  # Assuming the first asset is the main download
            asset_url = asset['browser_download_url']
            asset_name = asset['name']
            print(f"[*] Downloading the latest release: {asset_name}")
            download_path = download_asset(asset_url, asset_name)
            if download_path:
                print(f"[*] Update downloaded to: {download_path}")
            else:
                print("[-] Failed to download the latest version.")
        else:
            print("[-] No downloadable assets found for this release.")
        time.sleep(2)
        exit()

def find_fivem_path():
    """ Attempt to find the FiveM installation path."""
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
    user_provided_path = input(r"""[/] FiveM executable not found. Please enter the full path to your FiveM executable: """)
    if os.path.exists(user_provided_path) and os.path.isfile(user_provided_path):
        return user_provided_path
    else:
        print("[-] The provided path is not valid or the file does not exist.")
        return None

def launch_fivem_with_build_and_pure_mode(build_number, pure_mode):
    """ Launch FiveM with the specified build number and pure mode."""
    fivem_path = find_fivem_path()
    if fivem_path is None:
        print("[-] Could not find the FiveM installation. Please check if it's installed correctly.")
        return

    command = [fivem_path, f"-b{build_number}", f"-pure_{pure_mode}"]
    print("[+] Fivem is Launching, Have Fun!")

    time.sleep(1)

    try:
        subprocess.Popen(command)
    except (subprocess.CalledProcessError, OSError) as e:
        print(f"[-] Failed to launch FiveM: {e}")

def main():
    """ Main function that checks for updates and optionally launches FiveM."""
    print(f"[*] Local version: {LOCAL_VERSION}")
    latest_version, assets = get_latest_version()
    if latest_version:
        print(f"[*] Latest version: {latest_version}")
        compare_versions_and_update(LOCAL_VERSION, latest_version, assets)

if __name__ == "__main__":
    main()

    # Get the build number from the user
    build = input(r"""[/] Enter the build number you want to launch: """)
    pure_mode = input(r"""[/] Enter the pure mode you want to use: """)
    
    # Validate the build input and launch FiveM
    if not build.isdigit():
        print("[-] Invalid build number. Please enter a valid number.")
    else:
        launch_fivem_with_build_and_pure_mode(build, pure_mode)

    time.sleep(2)
