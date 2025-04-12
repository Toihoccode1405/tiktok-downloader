import re
import requests
import time
import json
from bs4 import BeautifulSoup

def extract_video_id(url):
    """Trích xuất ID video từ URL TikTok"""
    try:
        # Pattern 1: URL đầy đủ dạng https://www.tiktok.com/@username/video/1234567890123456789
        match = re.search(r'\/video\/(\d+)', url)
        if match:
            return match.group(1)
            
        # Pattern 2: URL ngắn dạng https://vm.tiktok.com/ABCDEF/
        if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
            resolved_url = resolve_short_url(url)
            if resolved_url:
                return extract_video_id(resolved_url)
                
        # Pattern 3: Nếu URL là chuỗi số thuần túy
        if url.isdigit() and len(url) > 10:
            return url
            
        # Pattern 4: Trích xuất từ tham số aweme_id
        params_match = re.search(r'aweme_id=(\d+)', url)
        if params_match:
            return params_match.group(1)
            
        # Không tìm thấy ID
        return None
    except Exception as e:
        print(f"Lỗi khi trích xuất ID video: {e}")
        return None

def resolve_short_url(url, headers, max_retries=3):
    """Giải quyết URL rút gọn của TikTok với xử lý lỗi và thử lại"""
    for attempt in range(max_retries):
        try:
            response = requests.head(url, allow_redirects=True, timeout=10, headers=headers)
            if response.status_code == 200:
                return response.url
            elif response.status_code == 429:  # Too Many Requests
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
            else:
                break  # Other error, don't retry
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:  # Last attempt
                raise e
            time.sleep(1)  # Wait before retrying
    
    # Nếu không thể giải quyết URL, trả về URL gốc
    return url

# ...existing code...

def get_tiktok_video_info(url, headers):
    """
    Lấy thông tin video TikTok bằng cách phân tích trực tiếp trang web
    Đây là phương pháp thực tế hơn khi không có API chính thức
    """
    try:
        # Giải quyết URL rút gọn nếu cần
        if "vm.tiktok.com" in url or "/t/" in url:
            url = resolve_short_url(url, headers)
            
        # Lấy nội dung trang
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Lỗi khi tải trang: HTTP {response.status_code}")
            return None
            
        # Tìm dữ liệu JSON nhúng trong trang
        content = response.text
        
        # Phương pháp 1: Tìm SIGI_STATE
        sigi_state_match = re.search(r'window\[\'SIGI_STATE\'\]\s*=\s*(\{.*?\});\s*window\[\'SIGI_RETRY\'\]', content, re.DOTALL)
        if sigi_state_match:
            try:
                data = json.loads(sigi_state_match.group(1))
                
                # Phân tích dữ liệu từ cấu trúc JSON
                if 'ItemModule' in data:
                    for key, item in data['ItemModule'].items():
                        video_data = {
                            'author_name': item.get('author', {}).get('nickname', 'unknown'),
                            'video_id': item.get('id', ''),
                            'desc': item.get('desc', ''),
                            'createTime': item.get('createTime', 0),
                        }
                        
                        # Lấy thông tin video
                        if 'video' in item:
                            video_data['video'] = {
                                'height': item['video'].get('height', 0),
                                'width': item['video'].get('width', 0),
                                'duration': item['video'].get('duration', 0),
                                'ratio': item['video'].get('ratio', ''),
                            }
                            
                            # Lấy URL video
                            if 'playAddr' in item['video']:
                                video_data['download_url'] = item['video']['playAddr']
                                
                            # Lấy URL video HD nếu có
                            if 'downloadAddr' in item['video']:
                                video_data['hd_download_url'] = item['video']['downloadAddr']
                                
                        return video_data
            except json.JSONDecodeError:
                print("Không thể parse SIGI_STATE JSON")
        
        # Phương pháp 2: Tìm thông qua __UNIVERSAL_DATA_FOR_REHYDRATION__
        universal_match = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(\{.*?\})</script>', content, re.DOTALL)
        if universal_match:
            try:
                data = json.loads(universal_match.group(1))
                if 'default' in data and '__DEFAULT_SCOPE__' in data['default']:
                    item_info = data['default']['__DEFAULT_SCOPE__'].get('webapp.video-detail', {}).get('itemInfo', {}).get('itemStruct')
                    if item_info:
                        video_data = {
                            'author_name': item_info.get('author', {}).get('nickname', 'unknown'),
                            'video_id': item_info.get('id', ''),
                            'desc': item_info.get('desc', ''),
                            'createTime': item_info.get('createTime', 0),
                        }
                        
                        # Lấy thông tin video
                        if 'video' in item_info:
                            video = item_info['video']
                            video_data['video'] = {
                                'height': video.get('height', 0),
                                'width': video.get('width', 0),
                                'duration': video.get('duration', 0),
                                'ratio': video.get('ratio', ''),
                            }
                            
                            # Lấy URL video
                            video_data['download_url'] = video.get('playAddr', '')
                            video_data['hd_download_url'] = video.get('downloadAddr', video.get('playAddr', ''))
                            
                        return video_data
            except json.JSONDecodeError:
                print("Không thể parse UNIVERSAL_DATA JSON")
                
        # Phương pháp 3: Tìm thẻ meta property 
        soup = BeautifulSoup(content, 'html.parser')
        
        # Lấy thông tin cơ bản từ meta tags
        meta_data = {}
        for meta in soup.find_all('meta', attrs={'property': re.compile('^og:')}):
            prop = meta.get('property', '').replace('og:', '')
            content = meta.get('content', '')
            meta_data[prop] = content
            
        if meta_data:
            # Trích xuất URL video từ meta tags
            video_url = meta_data.get('video:secure_url', meta_data.get('video', ''))
            if video_url:
                # Tìm ID video từ URL hoặc trang
                video_id = extract_video_id(url) or str(int(time.time()))
                
                # Trích xuất tên tác giả từ trang
                author_tag = soup.find('h3', class_=re.compile('author'))
                author_name = 'unknown'
                if author_tag:
                    author_name = author_tag.text.strip()
                
                # Trích xuất mô tả
                desc = meta_data.get('description', '')
                
                return {
                    'author_name': author_name,
                    'video_id': video_id,
                    'desc': desc,
                    'download_url': video_url,
                    'hd_download_url': video_url,
                    'createTime': int(time.time())
                }
                
        # Không tìm thấy thông tin video từ các phương pháp trên
        print("Không thể trích xuất thông tin video từ trang web")
        return None
        
    except Exception as e:
        print(f"Lỗi khi phân tích trang TikTok: {str(e)}")
        # In thông tin chi tiết hơn để debug
        import traceback
        traceback.print_exc()
        return None