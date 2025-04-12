# TikTok Downloader

Một công cụ mạnh mẽ để tải video TikTok không có watermark.

## Tính năng

- Tải video TikTok không có watermark
- Hỗ trợ nhiều nguồn API cho độ tin cậy cao
- Xử lý URL TikTok đầy đủ và rút gọn
- Lưu lịch sử tải xuống
- Kiểm tra tính toàn vẹn của video tải xuống
- Hiển thị tiến trình tải xuống với thanh tiến độ
- Tự động xử lý các lỗi và thử lại

## Cài đặt

```bash
pip install tiktok-downloader
```

## Sử dụng

### Dòng lệnh

```bash
# Tải một video
tiktok-downloader https://www.tiktok.com/@username/video/1234567890

# Tải video với chất lượng cao
tiktok-downloader --quality high https://www.tiktok.com/@username/video/1234567890

# Xem lịch sử tải xuống
tiktok-downloader --history
```

### Trong Python

```python
from tiktok_downloader import TikTokDownloader

downloader = TikTokDownloader()
downloader.download_video("https://www.tiktok.com/@username/video/1234567890")

# Xem lịch sử
downloader.show_history()
```

## Yêu cầu

- Python 3.7+
- Kết nối Internet

## Cập nhật

Công cụ sẽ tự động kiểm tra và thông báo khi có phiên bản mới.

## Giấy phép

MIT License