# ota_updater.py

import requests
import os
import sys
import zipfile
import json
from PySide6.QtWidgets import QProgressDialog
from PySide6.QtCore import Qt

class OTAUpdater:
    def __init__(self, current_version, github_repo):
        self.current_version = current_version
        self.github_repo = github_repo
        self.api_url = f"https://api.github.com/repos/{github_repo}/releases/latest"

    def check_for_update(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release['tag_name'].lstrip('v')
            return self._compare_versions(latest_version, self.current_version), latest_release
        except requests.RequestException as e:
            print(f"Error checking for updates: {e}")
            return False, None

    def _compare_versions(self, version1, version2):
        v1_parts = [int(part) for part in version1.split('.')]
        v2_parts = [int(part) for part in version2.split('.')]
        return v1_parts > v2_parts

    def download_update(self, asset_url, parent_widget=None):
        try:
            response = requests.get(asset_url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB

            progress_dialog = QProgressDialog("Downloading update...", "Cancel", 0, total_size, parent_widget)
            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            progress_dialog.setWindowTitle("Downloading Update")

            with open("update.zip", "wb") as f:
                for data in response.iter_content(block_size):
                    size = f.write(data)
                    progress_dialog.setValue(progress_dialog.value() + size)
                    if progress_dialog.wasCanceled():
                        return False

            progress_dialog.setValue(total_size)
            return True
        except requests.RequestException as e:
            print(f"Error downloading update: {e}")
            return False

    def apply_update(self):
        try:
            with zipfile.ZipFile("update.zip", 'r') as zip_ref:
                zip_ref.extractall("update")
            
            with open("update/update_config.json", 'r') as config_file:
                update_config = json.load(config_file)
            
            for file_update in update_config['file_updates']:
                src = os.path.join("update", file_update['src'])
                dest = file_update['dest']
                os.replace(src, dest)
            
            if 'post_update_script' in update_config:
                subprocess.run([sys.executable, os.path.join("update", update_config['post_update_script'])])
            
            os.remove("update.zip")
            for root, dirs, files in os.walk("update", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir("update")
            
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            print(f"Error applying update: {e}")