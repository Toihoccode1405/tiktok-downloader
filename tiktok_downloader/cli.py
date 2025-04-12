import argparse
import sys
import os
from colorama import init, Fore, Style
from .downloader import TikTokDownloader
from .updater import Updater

def run_cli():
    """Điểm vào chính của ứng dụng command-line"""
    # Khởi tạo colorama
    init(autoreset=True)
    
    # Khởi tạo parser
    parser = argparse.ArgumentParser(description="Tải video TikTok không có watermark")
    parser.add_argument('url', nargs='?', help='URL video TikTok cần tải xuống')
    parser.add_argument('-q', '--quality', choices=['high', 'medium'], default='high',
                       help='Chất lượng video (high hoặc medium)')
    parser.add_argument('--history', action='store_true', help='Hiển thị lịch sử tải xuống')
    parser.add_argument('--clear-history', action='store_true', help='Xóa lịch sử tải xuống')
    parser.add_argument('--export', choices=['txt', 'csv'], help='Xuất lịch sử ra file (txt hoặc csv)')
    parser.add_argument('--check-update', action='store_true', help='Kiểm tra bản cập nhật mới')
    parser.add_argument('--update', action='store_true', help='Cập nhật lên phiên bản mới nhất')
    
    args = parser.parse_args()
    
    # Kiểm tra cập nhật nếu cần
    if args.check_update or args.update:
        updater = Updater()
        if args.update:
            updater.perform_update()
            return
        else:
            has_update, latest_version = updater.check_for_updates()
            if not has_update:
                print(f"{Fore.GREEN}Bạn đang sử dụng phiên bản mới nhất ({updater.current_version}).{Style.RESET_ALL}")
            return
    
    # Kiểm tra cập nhật tự động theo định kỳ
    updater = Updater()
    updater.check_for_updates(auto_update=False)
    
    # Khởi tạo downloader
    downloader = TikTokDownloader()
    
    # Xử lý các lệnh
    if args.history:
        downloader.show_history()
        return
        
    if args.clear_history:
        if input(f"{Fore.YELLOW}Bạn có chắc chắn muốn xóa tất cả lịch sử? (y/n): {Style.RESET_ALL}").lower() == 'y':
            downloader.download_history = []
            downloader.save_history()
            print(f"{Fore.GREEN}Đã xóa lịch sử tải xuống.{Style.RESET_ALL}")
        return
    
    if args.export:
        downloader.export_history(args.export)
        return
    
    # Xử lý việc tải video
    if args.url:
        # Nếu URL được cung cấp, tiến hành tải video
        success = downloader.download_video(args.url, args.quality)
        if success:
            print(f"{Fore.GREEN}Tải xuống thành công!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Tải xuống không thành công. Vui lòng thử lại sau.{Style.RESET_ALL}")
    else:
        # Nếu không có URL, hiển thị giao diện tương tác
        print(f"{Fore.CYAN}═══ TẢI VIDEO TIKTOK ════{Style.RESET_ALL}")
        while True:
            url = input("Nhập URL video TikTok (nhập 'q' để thoát): ")
            if url.lower() == 'q':
                break
                
            if url:
                quality = 'high'
                print("Chọn chất lượng video:")
                print("1. Cao (HD)")
                print("2. Trung bình")
                choice = input("Chọn chất lượng (1-2): ")
                if choice == '2':
                    quality = 'medium'
                    
                print(f"{Fore.CYAN}Đang xử lý yêu cầu tải xuống...{Style.RESET_ALL}")
                success = downloader.download_video(url, quality)
                
                if success:
                    print(f"{Fore.GREEN}Tải xuống thành công!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Tải xuống không thành công. Vui lòng thử lại sau.{Style.RESET_ALL}")
                
                input("Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    run_cli()