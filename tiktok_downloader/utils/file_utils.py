import os
import json
import shutil # thư viện shutil để sao chép và xóa tệp
from datetime import datetime

def ensure_directory_exists(directory):
    """Tạo thư mục nếu chưa tồn tại."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

def load_json_file(file_path,defautl_value=None):
    """Tải dữ liệu từ file JSON."""
    if defautl_value is None:
        defautl_value = []
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Không thể tải file JSON: {e}.Sử dụng giá trị mặc đinh")
    
    return defautl_value

def save_json_file(file_path, data):
    """Lưu dữ liệu vào file JSON."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Không thể lưu file JSON: {e}")
        return False
    
def format_file_size(size_in_bytes):
    """Định dạng kích thước file theo MB"""
    return f"{size_in_bytes / (1024 * 1024):.2f} MB"

def generate_filename(author, video_id):
    """Tạo tên file từ thông tin video"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{author}_{video_id}_{timestamp}.mp4"
    