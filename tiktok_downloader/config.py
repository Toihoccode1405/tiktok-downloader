import os
import json
from datetime import datetime

class Config:
    """Cấu hình cho ứng dụng TikTok Downloader"""
    
    def __init__(self):
        # Tên người dùng từ hệ thống
        self.username = os.getenv('USERNAME') or os.getenv('USER') or 'user'
        
        # Thư mục mặc định cho tải xuống
        self.default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "TikTok")
        
        # Thiết lập tải xuống
        self.chunk_size = 4096  # kích thước chunk khi tải xuống (4KB - thực tế hơn)
        self.max_retries = 3    # số lần thử lại tối đa
        self.timeout = 30       # timeout kết nối (giây)
        
        # Thiết lập ứng dụng
        self._app_settings = {
            'version': '1.2.1',
            'last_updated': '2023-04-12',
            'author': 'Toihoccode1405code',
            'auto_update': True,
            'save_history': True,
            'max_history_items': 100,
            'theme': 'dark',  # 'dark' hoặc 'light'
        }
        
        # Tải cấu hình nếu tồn tại
        self._load_config()
        
    def _load_config(self):
        """Tải cài đặt cấu hình từ file"""
        config_path = os.path.join(os.path.expanduser("~"), ".tiktok_downloader", "config.json")
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    # Cập nhật cài đặt từ file, giữ các giá trị mặc định cho các khóa mới
                    self._app_settings.update(saved_config)
        except Exception as e:
            print(f"Không thể tải cấu hình: {e}")
    
    def save_config(self):
        """Lưu cấu hình hiện tại vào file"""
        config_dir = os.path.join(os.path.expanduser("~"), ".tiktok_downloader")
        config_path = os.path.join(config_dir, "config.json")
        
        try:
            # Tạo thư mục nếu không tồn tại
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self._app_settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Không thể lưu cấu hình: {e}")
            return False
    
    def get_history_file_path(self, download_dir):
        """Trả về đường dẫn đầy đủ đến file lịch sử"""
        return os.path.join(download_dir, "history.json")
    
    def get_setting(self, key, default=None):
        """Lấy giá trị cài đặt"""
        return self._app_settings.get(key, default)
    
    def set_setting(self, key, value):
        """Đặt giá trị cài đặt"""
        self._app_settings[key] = value
        return self.save_config()
    
    def get_app_info(self):
        """Trả về thông tin ứng dụng"""
        return {
            'version': self.get_setting('version'),
            'last_updated': self.get_setting('last_updated'),
            'author': self.get_setting('author'),
            'current_user': self.username,
            'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }   