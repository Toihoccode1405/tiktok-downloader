import requests
import os
import time
import base64
import random
import hashlib
import re
import traceback
from datetime import datetime
from tqdm import tqdm
from colorama import Fore, Style
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from .utils.url_utils import extract_video_id, resolve_short_url, get_tiktok_video_info
from .utils.file_utils import ensure_directory_exists, load_json_file, save_json_file, generate_filename
from .config import Config

class TikTokDownloader:
    def __init__(self):
        self.config = Config()
        self.download_history = []
        self.download_folder = self.config.default_download_dir
        self.history_file = self.config.get_history_file_path(self.download_folder)
        
        # Tạo thư mục tải về nếu chưa tồn tại
        ensure_directory_exists(self.download_folder)
            
        # Tải lịch sử tải về
        self.load_history()
        
        # Headers giả lập trình duyệt thực tế hơn
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Referer": "https://www.tiktok.com/",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1"
        }
        
        # Thêm cookie nếu cần thiết
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Rotates user-agents để tránh bị chặn
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1"
        ]

    def _rotate_user_agent(self):
        """Thay đổi User-Agent để tránh bị chặn"""
        self.headers["User-Agent"] = random.choice(self.user_agents)
        self.session.headers.update({"User-Agent": self.headers["User-Agent"]})
    
    def _generate_signature(self, url):
        """
        Tạo chữ ký cho request (giả lập)
        Trong thực tế, TikTok sử dụng thuật toán phức tạp hơn nhiều
        """
        timestamp = int(time.time())
        random_str = hashlib.md5(str(random.random()).encode()).hexdigest()
        signature_base = f"{url}:{timestamp}:{random_str}"
        return base64.b64encode(hashlib.sha256(signature_base.encode()).digest()).decode()

    def get_video_info(self, url):
        """Lấy thông tin video từ URL TikTok"""
        try:
            # Xoay vòng User-Agent 
            self._rotate_user_agent()
            
            # Thêm chữ ký (giả lập) để bypass hạn chế của TikTok
            signature = self._generate_signature(url)
            self.session.headers.update({"X-Signature": signature})
            
            # Sử dụng phương pháp phân tích trang để lấy thông tin video
            video_info = get_tiktok_video_info(url, self.headers)
            
            # Thêm một delay ngẫu nhiên để tránh bị chặn
            time.sleep(random.uniform(1.0, 2.5))
            
            return video_info
            
        except Exception as e:
            print(f"{Fore.RED}Lỗi khi lấy thông tin video: {e}{Style.RESET_ALL}")
            return None

    def download_video(self, url, quality="high"):
        """Tải video TikTok không có logo"""
        try:
            # Làm sạch URL trước
            url = self._clean_url(url)
            
            # Lấy thông tin video
            print(f"{Fore.CYAN}Đang lấy thông tin video...{Style.RESET_ALL}")
            video_info = self.get_video_info(url)
            
            if not video_info or not video_info.get('download_url'):
                print(f"{Fore.RED}Không thể lấy thông tin video từ URL: {url}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Thử phương pháp tải trực tiếp từ API...{Style.RESET_ALL}")
                
                # Trích xuất ID video
                video_id = extract_video_id(url)
                if not video_id:
                    print(f"{Fore.RED}Không thể xác định ID video từ URL.{Style.RESET_ALL}")
                    return False
                    
                # Sử dụng dịch vụ API ngoài để tải video không có logo
                return self._download_using_external_api(url, video_id, quality)
            
            # Nếu trích xuất thành công thì tiếp tục logic cũ
            # Lấy URL tải video dựa trên chất lượng
            download_url = None
            if quality == "high" and "hd_download_url" in video_info:
                download_url = video_info["hd_download_url"]
            elif "download_url" in video_info:
                download_url = video_info["download_url"]
            else:
                print(f"{Fore.RED}Không tìm thấy URL tải xuống video{Style.RESET_ALL}")
                return False
                
            # Tiếp tục tải xuống với URL đã tìm thấy
            return self._download_from_url(download_url, video_info.get('video_id', ''), 
                                         video_info.get('author_name', 'unknown'),
                                         video_info.get('desc', ''), url)
            
        except Exception as e:
            print(f"{Fore.RED}Lỗi tải video: {e}{Style.RESET_ALL}")
            traceback.print_exc()  # In ra chi tiết lỗi để debug
            return False

    def _clean_url(self, url):
        """Làm sạch URL TikTok, loại bỏ các tham số không cần thiết"""
        try:
            # Nếu là URL ngắn, cố gắng resolve trước
            if "vm.tiktok" in url or "vt.tiktok" in url:
                resolved_url = resolve_short_url(url, self.headers)
                if resolved_url and resolved_url != url:
                    return self._clean_url(resolved_url)
            
            # Phân tích URL để giữ lại phần quan trọng
            parsed_url = urlparse(url)
            
            # Giữ lại đường dẫn chính đến video, bỏ tất cả các tham số khác
            # Format tiêu chuẩn: https://www.tiktok.com/@username/video/videoID
            path = parsed_url.path
            
            # Nếu có pattern /video/ trong URL, chỉ giữ phần đó và user
            if '/video/' in path:
                parts = path.split('/video/')
                if len(parts) >= 2:
                    # Tạo URL sạch với format đúng
                    clean_path = f"{parts[0]}/video/{parts[1].split('/')[0]}"
                    return f"{parsed_url.scheme}://{parsed_url.netloc}{clean_path}"
            
            # Nếu không tìm thấy pattern chuẩn, giữ nguyên đường dẫn (không kèm params)
            return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        except Exception as e:
            print(f"Lỗi khi làm sạch URL: {e}")
            # Nếu có lỗi, trả về URL gốc để tránh làm hỏng luồng tải
            return url

    def _download_using_external_api(self, original_url, video_id, quality="high"):
        """Sử dụng các API bên thứ ba để tải video TikTok"""
        # Danh sách các API công khai để thử - thứ tự từ tốt nhất xuống
        # Thử TikWM trước tiên - phương pháp có tỷ lệ thành công cao nhất
        tikwm_result = self._download_from_tikwm(original_url, video_id)
        if tikwm_result:
            return True

        api_endpoints = [
            # Thêm API mới phù hợp với URL đầy đủ (bao gồm các tham số)
            f"https://api.tikdown.org/api/download?url={original_url}",
            f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}",
            f"https://api.tikmate.app/api/lookup?url={original_url}",
            f"https://api.douyin.wtf/api?url={original_url}",
            f"https://www.tikwm.com/api/?url={original_url}",
            f"https://www.tikwm.com/api/old/?url={original_url}",
            f"https://ssstik.io/abc?url={original_url}"
        ]
        
        # Thử từng API cho đến khi thành công
        for api_url in api_endpoints:
            try:
                print(f"{Fore.CYAN}Đang thử API: {api_url.split('?')[0]}{Style.RESET_ALL}")
                
                # Tạo header khác nhau cho mỗi yêu cầu
                api_headers = {
                    "User-Agent": random.choice(self.user_agents),
                    "Referer": "https://www.tiktok.com/",
                    "Accept": "application/json"
                }
                
                response = self.session.get(api_url, headers=api_headers, timeout=15)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Xử lý các định dạng API khác nhau
                        download_url = None
                        author = "unknown"
                        desc = f"TikTok Video {video_id}"
                        
                        # API tikdown.org
                        if "data" in data and "no_watermark_token" in data.get("data", {}):
                            download_url = data["data"]["no_watermark_token"]
                            if "author_nickname" in data["data"]:
                                author = data["data"]["author_nickname"]
                            if "title" in data["data"]:
                                desc = data["data"]["title"]
                        
                        # API tikwm.com
                        elif "data" in data and "play" in data.get("data", {}):
                            download_url = data["data"]["play"]
                            author = data["data"].get("author", {}).get("unique_id", "unknown")
                            desc = data["data"].get("title", desc)
                        
                        # API tikmate.app
                        elif "video_url" in data:
                            download_url = data["video_url"]
                        
                        # API douyin.wtf
                        elif "video_data" in data and "nwm_video_url" in data.get("video_data", {}):
                            download_url = data["video_data"]["nwm_video_url"]
                            author = data["video_data"].get("author", {}).get("unique_id", "unknown")
                            desc = data["video_data"].get("desc", desc)
                        
                        # API TikTok
                        elif "aweme_list" in data and len(data["aweme_list"]) > 0:
                            item = data["aweme_list"][0]
                            download_url = item.get("video", {}).get("play_addr", {}).get("url_list", [None])[0]
                            author = item.get("author", {}).get("unique_id", "unknown")
                            desc = item.get("desc", desc)
                            
                            if not download_url and "download_addr" in item.get("video", {}):
                                download_url = item["video"]["download_addr"].get("url_list", [None])[0]
                        
                        if download_url:
                            print(f"{Fore.GREEN}Tìm thấy URL tải xuống từ API!{Style.RESET_ALL}")
                            return self._download_from_url(download_url, video_id, author, desc, original_url)
                    
                    except Exception as e:
                        print(f"{Fore.YELLOW}Lỗi khi xử lý phản hồi API: {e}{Style.RESET_ALL}")
                        continue
            
            except Exception as e:
                print(f"{Fore.YELLOW}Không thể kết nối tới API: {e}{Style.RESET_ALL}")
                continue
        
        # Nếu không có API nào thành công, thử phương pháp cuối cùng: tải từ SnaptikApp
        try:
            return self._download_from_snaptik(original_url, video_id)
        except Exception as e:
            print(f"{Fore.RED}Tất cả các phương pháp đã thất bại: {e}{Style.RESET_ALL}")
            return False
    
    def _download_from_url(self, download_url, video_id, author="unknown", desc="", original_url=""):
        """Tải video từ URL trực tiếp"""
        try:
            # Tạo tên file từ thông tin video
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Làm sạch tên tác giả (loại bỏ ký tự đặc biệt)
            author = re.sub(r'[\\/*?:"<>|]', "", author)
            filename = f"{author}_{video_id}_{timestamp}.mp4"
            filepath = os.path.join(self.download_folder, filename)
            
            # Tải video
            print(f"{Fore.CYAN}Đang tải video từ URL khác...{Style.RESET_ALL}")
            
            # Tạo headers mới cho yêu cầu tải xuống
            dl_headers = {
                "User-Agent": random.choice(self.user_agents),
                "Accept": "*/*",
                "Accept-Encoding": "identity;q=1, *;q=0",
                "Range": "bytes=0-",
                "Referer": original_url or "https://www.tiktok.com/",
                "Sec-Fetch-Dest": "video"
            }
            
            # Gửi yêu cầu tải xuống với retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(download_url, headers=dl_headers, stream=True, timeout=30)
                    
                    # 200 OK và 206 Partial Content là các mã thành công
                    if response.status_code in (200, 206):
                        # Kiểm tra nhanh xem phản hồi có phải là video không
                        content_type = response.headers.get('Content-Type', '')
                        if not content_type.startswith('video/') and not content_type.startswith('application/octet-stream') and not content_type.startswith('binary/'):
                            if attempt == max_retries - 1:
                                print(f"{Fore.RED}URL không chứa video hợp lệ: {content_type}{Style.RESET_ALL}")
                                return False
                            continue
                            
                        # Kiểm tra kích thước
                        content_length = int(response.headers.get('Content-Length', 0))
                        if content_length < 10000:  # Video nhỏ hơn 10KB có thể là lỗi
                            if attempt == max_retries - 1:
                                print(f"{Fore.YELLOW}Cảnh báo: File video quá nhỏ ({content_length / 1024:.2f} KB){Style.RESET_ALL}")
                            else:
                                time.sleep(2)
                                continue
                        
                        break
                    elif response.status_code == 429:  # Too Many Requests
                        wait_time = 5 * (attempt + 1)
                        print(f"{Fore.YELLOW}Quá nhiều yêu cầu. Đang đợi {wait_time}s và thử lại...{Style.RESET_ALL}")
                        time.sleep(wait_time)
                    else:
                        print(f"{Fore.RED}Lỗi tải video. Mã lỗi: {response.status_code}. Thử lại...{Style.RESET_ALL}")
                        time.sleep(2)
                except Exception as e:
                    print(f"{Fore.YELLOW}Lỗi kết nối: {e}. Thử lại...{Style.RESET_ALL}")
                    time.sleep(2)
                    
            if response.status_code not in (200, 206):
                print(f"{Fore.RED}Không thể tải video sau {max_retries} lần thử.{Style.RESET_ALL}")
                return False
            
            # Tính toán kích thước để hiển thị thanh tiến trình
            total_size = int(response.headers.get('content-length', 0))
            
            # Nếu server trả về partial content (206), có thể cần xử lý khác
            if response.status_code == 206 and 'Content-Range' in response.headers:
                try:
                    # Format: "bytes X-Y/Z" - Z là kích thước đầy đủ
                    content_range = response.headers.get('Content-Range')
                    if content_range:
                        match = re.search(r'bytes \d+-\d+/(\d+)', content_range)
                        if match:
                            total_size = int(match.group(1))
                except:
                    # Nếu không phân tích được, vẫn dùng content-length
                    pass
            
            block_size = self.config.chunk_size
            
            # Hiển thị thanh tiến trình và tải video
            try:
                with open(filepath, 'wb') as file, tqdm(
                    desc=f"{filename[:30]}..." if len(filename) > 30 else filename,
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                    bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Style.RESET_ALL)
                ) as bar:
                    for data in response.iter_content(block_size):
                        if data:  # Đảm bảo không ghi các khối rỗng
                            size = file.write(data)
                            bar.update(size)
            except Exception as e:
                print(f"{Fore.RED}Lỗi khi ghi file: {e}{Style.RESET_ALL}")
                # Xóa file không hoàn chỉnh nếu có lỗi
                if os.path.exists(filepath):
                    os.remove(filepath)
                return False
            
            # Kiểm tra kích thước file đã tải
            actual_size = os.path.getsize(filepath)
            if actual_size < 10000:  # Nếu file nhỏ hơn 10KB
                print(f"{Fore.RED}File tải về không hợp lệ (kích thước quá nhỏ: {actual_size/1024:.2f} KB).{Style.RESET_ALL}")
                os.remove(filepath)
                return False
            
            # Thử mở file video để kiểm tra tính hợp lệ
            try:
                # Đảm bảo file có header MP4 hợp lệ (magic bytes)
                with open(filepath, 'rb') as file:
                    header = file.read(8)  # Đọc 8 bytes đầu tiên
                    # Kiểm tra magic bytes của MP4/MOV (ftyp, mdat, moov, etc.)
                    if not (b'ftyp' in header or b'mdat' in header or b'moov' in header):
                        print(f"{Fore.RED}File tải về không phải là video MP4 hợp lệ.{Style.RESET_ALL}")
                        os.remove(filepath)
                        return False
            except Exception:
                pass  # Nếu không kiểm tra được, vẫn giữ file
                
            if total_size > 0 and actual_size < total_size * 0.95:  # Nếu thiếu hơn 5%
                print(f"{Fore.YELLOW}Cảnh báo: File tải về có thể không hoàn chỉnh. "
                    f"({actual_size/1024/1024:.2f}MB / {total_size/1024/1024:.2f}MB){Style.RESET_ALL}")
            
            # Thêm vào lịch sử
            history_item = {
                "url": original_url,
                "filename": filename,
                "author": author,
                "quality": "direct",
                "timestamp": datetime.now().isoformat(),
                "download_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filepath": filepath,
                "filesize": actual_size,
                "file_size": actual_size,  # Thêm trường này để đảm bảo tương thích
                "description": desc
}
            self.download_history.append(history_item)
            self.save_history()
            
            print(f"{Fore.GREEN}Tải thành công: {filename}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Lưu tại: {filepath}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Lỗi tải video từ URL: {e}{Style.RESET_ALL}")
            traceback.print_exc()
            return False
    
    def _download_from_tikwm(self, original_url, video_id):
        """Phương pháp tối ưu cho TikWM API"""
        try:
            print(f"{Fore.CYAN}Đang thử phương pháp TikWM...{Style.RESET_ALL}")
            
            api_url = f"https://www.tikwm.com/api/?url={original_url}"
            
            # Headers tùy chỉnh cho TikWM
            tikwm_headers = {
                "User-Agent": random.choice(self.user_agents),
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://tikwm.com/",
                "Origin": "https://tikwm.com"
            }
            
            # Thêm cookie giả lập trình duyệt thực
            cookies = {
                "_ga": f"GA1.1.{random.randint(1000000, 9999999)}.{random.randint(1000000, 9999999)}",
                "_ga_XXXXXX": f"GS1.1.{int(time.time())}.1.1.{int(time.time())}.0"
            }
            
            response = requests.get(api_url, headers=tikwm_headers, cookies=cookies, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    if "data" in data and data.get("code") == 0:
                        item = data["data"]
                        
                        # Có nhiều loại URL video có thể sử dụng
                        download_url = None
                        
                        # Thử các URL theo thứ tự ưu tiên
                        if "nwm_video_url" in item:
                            download_url = item["nwm_video_url"]  # Video không watermark
                        elif "play" in item:
                            download_url = item["play"]
                        elif "wmplay" in item:
                            download_url = item["wmplay"]  # Video có watermark (phương án cuối)
                        
                        if download_url:
                            author = item.get("author", {}).get("unique_id", "unknown")
                            desc = item.get("title", f"TikTok Video {video_id}")
                            
                            # Thay đổi một số tham số trong URL để tăng khả năng tải thành công
                            if "tikwmcdn.net" in download_url:
                                download_url = download_url.replace("&format=", f"&d=1&format=")
                            
                            print(f"{Fore.GREEN}TikWM: Tìm thấy URL video không watermark!{Style.RESET_ALL}")
                            return self._download_from_url(download_url, video_id, author, desc, original_url)
                
                except Exception as e:
                    print(f"{Fore.YELLOW}Lỗi khi xử lý dữ liệu TikWM: {e}{Style.RESET_ALL}")
            
            return False
            
        except Exception as e:
            print(f"{Fore.RED}Lỗi khi sử dụng TikWM: {e}{Style.RESET_ALL}")
            return False
            
    def _download_from_snaptik(self, url, video_id):
        """Phương pháp cuối cùng: sử dụng snaptik.app để tải video TikTok"""
        try:
            print(f"{Fore.CYAN}Đang thử phương pháp SnaptikApp...{Style.RESET_ALL}")
            
            # Giả lập yêu cầu đến trang SnaptikApp
            session = requests.Session()
            session.headers.update({
                "User-Agent": random.choice(self.user_agents),
                "Referer": "https://snaptik.app/",
                "Accept-Language": "en-US,en;q=0.9",
                "Origin": "https://snaptik.app"
            })
            
            # Truy cập trang chính để lấy token
            main_page = session.get("https://snaptik.app/en", timeout=10)
            if main_page.status_code != 200:
                return False
                
            # Tìm token
            token_match = re.search(r'name="token" value="([^"]+)"', main_page.text)
            if not token_match:
                print(f"{Fore.RED}Không tìm thấy token SnaptikApp.{Style.RESET_ALL}")
                return False
                
            token = token_match.group(1)
            
            # Gửi yêu cầu tải xuống
            form_data = {
                "url": url,
                "token": token
            }
            
            response = session.post("https://snaptik.app/action.php", data=form_data, timeout=15)
            if response.status_code != 200:
                print(f"{Fore.RED}Lỗi yêu cầu SnaptikApp: {response.status_code}{Style.RESET_ALL}")
                return False
            
            # Tìm URL tải xuống trong phản hồi HTML
            download_match = re.search(r'href="(https?://[^"]+)" class="abutton is-success is-fullwidth" download', response.text)
            if not download_match:
                print(f"{Fore.RED}Không tìm thấy URL tải xuống trong phản hồi SnaptikApp.{Style.RESET_ALL}")
                return False
                
            download_url = download_match.group(1)
            
            # Trích xuất tên tác giả nếu có
            author_match = re.search(r'<h2 class="title is-6">([^<]+)</h2>', response.text)
            author = author_match.group(1).strip() if author_match else "unknown"
            
            # Tải video
            return self._download_from_url(download_url, video_id, author, f"TikTok Video {video_id}", url)
            
        except Exception as e:
            print(f"{Fore.RED}Lỗi khi sử dụng SnaptikApp: {e}{Style.RESET_ALL}")
            return False
    
    def load_history(self):
        """Tải lịch sử tải xuống từ file"""
        try:
            if os.path.exists(self.history_file):
                self.download_history = load_json_file(self.history_file, [])
            else:
                self.download_history = []
        except Exception as e:
            print(f"{Fore.YELLOW}Không thể tải lịch sử tải xuống: {e}{Style.RESET_ALL}")
            self.download_history = []
    
    def save_history(self):
        """Lưu lịch sử tải xuống vào file"""
        try:
            # Giới hạn số lượng mục trong lịch sử (giữ 100 mục mới nhất)
            max_history = 100
            if hasattr(self.config, 'get_setting'):
                max_history = self.config.get_setting('max_history_items', 100)
            
            # Đảm bảo mỗi mục lịch sử đều có đầy đủ thông tin cần thiết
            for item in self.download_history:
                if 'download_time' not in item or not item['download_time']:
                    item['download_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if 'file_size' not in item or not item['file_size']:
                    filepath = item.get('filepath', '')
                    if filepath and os.path.exists(filepath):
                        item['file_size'] = os.path.getsize(filepath)
                    else:
                        item['file_size'] = 0
            
            # Giữ số lượng mục trong giới hạn
            self.download_history = self.download_history[-max_history:]
            save_json_file(self.history_file, self.download_history)
            print(f"{Fore.GREEN}Đã lưu lịch sử tải xuống.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}Không thể lưu lịch sử tải xuống: {e}{Style.RESET_ALL}")

    def show_history(self):
        """Hiển thị lịch sử tải xuống"""
        if not self.download_history:
            print(f"{Fore.YELLOW}Lịch sử tải xuống trống.{Style.RESET_ALL}")
            return
            
        print(f"{Fore.CYAN}Lịch sử tải xuống ({len(self.download_history)} mục):{Style.RESET_ALL}")
        for i, item in enumerate(self.download_history, 1):
            file_size_mb = item.get('file_size', 0) / (1024 * 1024)
            author = item.get('author', 'unknown')
            desc = item.get('description', '')[:50] if item.get('description') else ''
            
            # Hiển thị thông tin tổng quan
            print(f"{Fore.GREEN}{i}. {author} - {desc}...{Style.RESET_ALL}")
            
            # Hiển thị thời gian tải xuống
            download_time = item.get('download_time', 'Không rõ')
            print(f"   {Fore.CYAN}Tải vào: {download_time}{Style.RESET_ALL}")
            
            # Hiển thị kích thước file
            print(f"   {Fore.CYAN}Kích thước: {file_size_mb:.2f} MB{Style.RESET_ALL}")
            
            # Hiển thị đường dẫn file
            filepath = item.get('filepath', 'Không có')
            if os.path.exists(filepath):
                print(f"   {Fore.CYAN}File: {filepath} {Fore.GREEN}[Tồn tại]{Style.RESET_ALL}")
            else:
                print(f"   {Fore.CYAN}File: {filepath} {Fore.RED}[Không tồn tại]{Style.RESET_ALL}")
            
            # Hiển thị URL gốc
            url = item.get('url', 'Không có')
            print(f"   {Fore.CYAN}URL gốc: {url}{Style.RESET_ALL}")
            print()
        
    def add_to_history(self, video_info, file_path):
        """Thêm một mục vào lịch sử tải xuống"""
        history_item = {
            'video_id': video_info.get('video_id', ''),
            'author': video_info.get('author_name', 'unknown'),
            'desc': video_info.get('desc', '')[:100],  # Giới hạn độ dài mô tả
            'file_path': file_path,
            'download_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'file_size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
        }
        self.download_history.append(history_item)
        self.save_history()
    
    def show_history(self):
        """Hiển thị lịch sử tải xuống"""
        if not self.download_history:
            print(f"{Fore.YELLOW}Lịch sử tải xuống trống.{Style.RESET_ALL}")
            return
            
        print(f"{Fore.CYAN}Lịch sử tải xuống ({len(self.download_history)} mục):{Style.RESET_ALL}")
        for i, item in enumerate(self.download_history, 1):
            file_size_mb = item.get('file_size', 0) / (1024 * 1024)
            print(f"{i}. {item.get('author', 'unknown')} - {item.get('desc', '')[:50]}...")
            print(f"   Tải vào: {item.get('download_time', '')}, Kích thước: {file_size_mb:.2f} MB")
            print(f"   File: {item.get('file_path', '')}")
            print()
    
    def export_history(self, output_format="txt"):
        """Xuất lịch sử tải xuống ra file"""
        try:
            if not self.download_history:
                print(f"{Fore.YELLOW}Không có lịch sử tải xuống để xuất.{Style.RESET_ALL}")
                return False
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if output_format.lower() == "csv":
                # Xuất ra file CSV
                export_file = os.path.join(self.config.default_download_dir, f"tiktok_download_history_{timestamp}.csv")
                with open(export_file, 'w', encoding='utf-8', newline='') as file:
                    import csv
                    writer = csv.writer(file)
                    # Viết tiêu đề
                    writer.writerow(["STT", "Thời gian", "Tác giả", "Mô tả", "Kích thước (MB)", "Đường dẫn file", "URL"])
                    
                    # Viết dữ liệu
                    for i, item in enumerate(self.download_history, 1):
                        file_size_mb = item.get('file_size', 0) / (1024 * 1024)
                        writer.writerow([
                            i,
                            item.get('download_time', ''),
                            item.get('author', 'unknown'),
                            item.get('description', '')[:100],
                            f"{file_size_mb:.2f}",
                            item.get('filepath', ''),
                            item.get('url', '')
                        ])
            else:
                # Xuất ra file TXT
                export_file = os.path.join(self.config.default_download_dir, f"tiktok_download_history_{timestamp}.txt")
                with open(export_file, 'w', encoding='utf-8') as file:
                    file.write(f"=== LỊCH SỬ TẢI VIDEO TIKTOK ({len(self.download_history)} MỤC) ===\n")
                    file.write(f"Xuất ngày: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    for i, item in enumerate(self.download_history, 1):
                        file_size_mb = item.get('file_size', 0) / (1024 * 1024)
                        file.write(f"{i}. {item.get('author', 'unknown')} - {item.get('description', '')[:50]}...\n")
                        file.write(f"   Tải vào: {item.get('download_time', '')}\n")
                        file.write(f"   Kích thước: {file_size_mb:.2f} MB\n")
                        file.write(f"   File: {item.get('filepath', '')}\n")
                        file.write(f"   URL: {item.get('url', '')}\n\n")
                    
            print(f"{Fore.GREEN}Đã xuất lịch sử tải xuống sang: {export_file}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Lỗi khi xuất lịch sử: {e}{Style.RESET_ALL}")
            traceback.print_exc()
            return False