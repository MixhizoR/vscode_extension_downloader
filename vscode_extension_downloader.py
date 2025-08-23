import requests
import os
import sys
import platform
from urllib.parse import urlparse

def get_system_platform():
    """Automatically detect system platform"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if system == 'windows':
        if '64' in arch:
            return 'win32-x64'
        else:
            return 'win32-ia32'
    elif system == 'darwin':  # macOS
        if 'arm' in arch or 'aarch64' in arch:
            return 'darwin-arm64'
        else:
            return 'darwin-x64'
    elif system == 'linux':
        if '64' in arch:
            return 'linux-x64'
        else:
            return 'linux-ia32'
    
    return None

def get_extension_versions(unique_identifier):
    """Fetch extension versions from Marketplace API"""
    try:
        publisher, package = unique_identifier.split('.')
        
        # Marketplace API to get extension info
        api_url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{package}/latest"
        
        headers = {
            'User-Agent': 'VSCode Extension Downloader',
            'Accept': 'application/json;api-version=3.0-preview.1'
        }
        
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            versions = [version['version'] for version in data.get('versions', [])]
            return versions[:10]  # Last 10 versions
        else:
            print(f"API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error fetching version info: {e}")
        return None

def get_latest_version(unique_identifier):
    """Automatically get the latest version"""
    try:
        publisher, package = unique_identifier.split('.')
        api_url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{package}/latest"
        
        headers = {
            'User-Agent': 'VSCode Extension Downloader',
            'Accept': 'application/json;api-version=3.0-preview.1'
        }
        
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('versions', [{}])[0].get('version')
        return None
    except:
        return None

def download_vsix(url, filename):
    """Download VSIX file"""
    try:
        print(f"Downloading: {filename}")
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"✓ {filename} downloaded successfully!")
            return True
        else:
            print(f"✗ Download failed! HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error during download: {e}")
        return False

def generate_vscode_extension_url(unique_identifier, version, target_platform=None):
    """Generate VS Code extension download URL"""
    publisher, package = unique_identifier.split('.')
    base_url = (
        f'https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}'
        f'/vsextensions/{package}/{version}/vspackage'
    )
    if target_platform:
        return f"{base_url}?targetPlatform={target_platform}"
    return base_url

def main():
    print("=== VS Code Extension Downloader ===\n")
    
    # Get extension identifier
    unique_identifier = input("Extension identifier (e.g. ms-vscode.cpptools): ").strip()
    if not unique_identifier or '.' not in unique_identifier:
        print("Invalid extension identifier!")
        return
    
    # Version selection
    print("\nFetching version options...")
    versions = get_extension_versions(unique_identifier)
    
    if versions:
        print(f"\nAvailable versions:")
        for i, version in enumerate(versions[:5], 1):
            print(f"{i}. {version}")
        
        choice = input(f"\nSelect a version (1-5) or press Enter for 'latest': ").strip()
        
        if choice == '' or choice.lower() == 'latest':
            version = get_latest_version(unique_identifier)
            if not version:
                version = versions[0]
            print(f"Using latest version: {version}")
        elif choice.isdigit() and 1 <= int(choice) <= 5:
            version = versions[int(choice) - 1]
        else:
            print("Invalid selection!")
            return
    else:
        version = input("Version (e.g. 1.23.5): ").strip()
        if not version:
            print("Version is required!")
            return
    
    # Platform selection
    auto_platform = get_system_platform()
    if auto_platform:
        use_auto = input(f"\nAuto-detected platform: {auto_platform}. Use this? (Y/n): ").strip().lower()
        if use_auto == '' or use_auto == 'y' or use_auto == 'yes':
            target_platform = auto_platform
        else:
            target_platform = input("Target platform (e.g. win32-x64, linux-x64, darwin-arm64): ").strip()
    else:
        target_platform = input("Target platform (e.g. win32-x64, linux-x64, darwin-arm64): ").strip()
    
    # Generate URL
    url = generate_vscode_extension_url(unique_identifier, version, target_platform)
    print(f"\nGenerated URL: {url}")
    
    # Download process
    download_choice = input("\nDownload the extension? (Y/n): ").strip().lower()
    if download_choice == '' or download_choice == 'y' or download_choice == 'yes':
        # Create filename
        publisher, package = unique_identifier.split('.')
        filename = f"{package}-{version}.vsix"
        
        # Download to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)
        
        print(f"\nDownloading... Save location: {filepath}")
        success = download_vsix(url, filepath)
        
        if success:
            print(f"\n✓ Process completed! File: {filepath}")
        else:
            print("\n✗ Download failed!")
    else:
        print("Download cancelled.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess cancelled.")
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")