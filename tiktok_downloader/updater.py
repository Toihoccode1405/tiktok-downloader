import requests
import pkg_resources
import time
import os
from colorama import Fore, Style
import subprocess
import sys

class Updater:
    def __init__(self, package_name="tiktok-downloader", github_repo="toihoccode1405/tiktok-downloader", check_interval=86400):
        """
        Khởi tạo trình kiểm tra cập nhật
        :param package_name: Tên package trên PyPI
        :param github_repo: Tên repository trên GitHub (username/repo)
        :param check_interval: Thời gian giữa các lần kiểm tra tính bằng giây (mặc định 1 ngày)
        """
        self.package_name = package_name
        self.github_repo = github_repo
        self.check_interval = check_interval
        self.last_check_file = os.path.join(
            os.path.expanduser("~"), 
            f".{package_name}_update_check"
        )
        
        # Xác định version hiện tại
        try:
            self.current_version = pkg_resources.get_distribution(package_name).version
        except:
            self.current_version = "unknown"
    
    def should_check_update(self):
        """Kiểm tra xem có nên kiểm tra bản cập nhật hay không dựa trên thời gian kiểm tra cuối cùng"""
        try:
            if os.path.exists(self.last_check_file):
                with open(self.last_check_file, 'r') as f:
                    last_check = float(f.read().strip())
                    if time.time() - last_check < self.check_interval:
                        return False
            return True
        except:
            return True
    
    def update_last_check_time(self):
        """Cập nhật thời gian kiểm tra cuối cùng"""
        try:
            with open(self.last_check_file, 'w') as f:
                f.write(str(time.time()))
        except:
            pass
            
    def get_latest_version(self):
        """Lấy phiên bản mới nhất từ PyPI"""
        try:
            response = requests.get(f"https://pypi.org/pypi/{self.package_name}/json", timeout=5)
            if response.status_code == 200:
                return response.json()['info']['version']
        except:
            pass
        
        # Nếu PyPI không hoạt động, thử GitHub
        try:
            response = requests.get(f"https://api.github.com/repos/{self.github_repo}/releases/latest", timeout=5)
            if response.status_code == 200:
                return response.json()['tag_name'].lstrip('v')
        except:
            pass
            
        return None
    
    def check_for_updates(self, auto_update=False):
        """
        Kiểm tra các bản cập nhật có sẵn
        :param auto_update: Tự động cập nhật nếu có phiên bản mới
        :return: (has_update, latest_version)
        """
        if not self.should_check_update():
            return False, self.current_version
            
        self.update_last_check_time()
        latest_version = self.get_latest_version()
        
        if latest_version and latest_version != self.current_version:
            if auto_update:
                self.perform_update()
                return True, latest_version
            else:
                print(f"{Fore.GREEN}Có phiên bản cập nhật mới: {latest_version} (hiện tại: {self.current_version}){Style.RESET_ALL}")
                print(f"{Fore.CYAN}Sử dụng lệnh sau để cập nhật:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}pip install --upgrade {self.package_name}{Style.RESET_ALL}")
                return True, latest_version
        
        return False, self.current_version
    
    def perform_update(self):
        """Tiến hành cập nhật package"""
        try:
            print(f"{Fore.CYAN}Đang cập nhật {self.package_name}...{Style.RESET_ALL}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", self.package_name])
            print(f"{Fore.GREEN}Cập nhật thành công! Vui lòng khởi động lại ứng dụng.{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Lỗi khi cập nhật: {e}{Style.RESET_ALL}")
            return False