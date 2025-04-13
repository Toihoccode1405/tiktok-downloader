import argparse
import sys
import os
import time
import shutil
from colorama import init, Fore, Style, Back
from .downloader import TikTokDownloader
from .updater import Updater

def clear_screen():
    """Xóa màn hình terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    """Lấy chiều rộng của terminal và đảm bảo giá trị hợp lý"""
    try:
        width = shutil.get_terminal_size().columns
        return max(80, min(width, 120))  # Giới hạn trong khoảng 80-120
    except:
        return 80  # Mặc định nếu không lấy được kích thước

def center_text(text, width=None, fill_char=' '):
    """Căn giữa văn bản trong terminal"""
    if width is None:
        width = get_terminal_width()
    padding = max(0, (width - len(text)) // 2)
    return fill_char * padding + text + fill_char * padding

def print_modern_logo():
    """Hiển thị logo TikTok với phong cách hiện đại"""
    terminal_width = get_terminal_width()
    
    logo = [
        f"{Fore.CYAN}  ████████╗{Fore.MAGENTA}██╗{Fore.WHITE}██╗  ██╗{Fore.CYAN}████████╗{Fore.MAGENTA}██████╗ {Fore.WHITE}██╗  ██╗{Style.RESET_ALL}",
        f"{Fore.CYAN}  ╚══██╔══╝{Fore.MAGENTA}██║{Fore.WHITE}██║ ██╔╝{Fore.CYAN}╚══██╔══╝{Fore.MAGENTA}██╔══██╗{Fore.WHITE}██║ ██╔╝{Style.RESET_ALL}",
        f"{Fore.CYAN}     ██║   {Fore.MAGENTA}██║{Fore.WHITE}█████╔╝ {Fore.CYAN}   ██║   {Fore.MAGENTA}██║  ██║{Fore.WHITE}█████╔╝ {Style.RESET_ALL}",
        f"{Fore.CYAN}     ██║   {Fore.MAGENTA}██║{Fore.WHITE}██╔═██╗ {Fore.CYAN}   ██║   {Fore.MAGENTA}██║  ██║{Fore.WHITE}██╔═██╗ {Style.RESET_ALL}",
        f"{Fore.CYAN}     ██║   {Fore.MAGENTA}██║{Fore.WHITE}██║  ██╗{Fore.CYAN}   ██║   {Fore.MAGENTA}██████╔╝{Fore.WHITE}██║  ██╗{Style.RESET_ALL}",
        f"{Fore.CYAN}     ╚═╝   {Fore.MAGENTA}╚═╝{Fore.WHITE}╚═╝  ╚═╝{Fore.CYAN}   ╚═╝   {Fore.MAGENTA}╚═════╝ {Fore.WHITE}╚═╝  ╚═╝{Style.RESET_ALL}"
    ]
    
    print("\n")
    for line in logo:
        print(center_text(line, terminal_width))
            
    print("\n")
    print(center_text(f"{Fore.GREEN}▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅{Style.RESET_ALL}", terminal_width))
    print(center_text(f"{Fore.YELLOW}⚡ VIDEO DOWNLOADER ⚡{Style.RESET_ALL}", terminal_width))
    print(center_text(f"{Fore.GREEN}▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅{Style.RESET_ALL}", terminal_width))
    print("\n")

def print_banner():
    """Hiển thị banner hiện đại khi khởi động ứng dụng"""
    terminal_width = get_terminal_width()
    clear_screen()
    print_modern_logo()
    
    # Hiển thị phiên bản
    try:
        from .. import __version__
    except:
        try:
            from tiktok_downloader import __version__
        except:
            __version__ = "1.2.2"
    
    # Thông tin phần mềm
    print(center_text(f"{Fore.CYAN}● Tải video TikTok không có watermark{Style.RESET_ALL}", terminal_width))
    print(center_text(f"{Fore.YELLOW}● Nhiều nguồn API để đảm bảo độ tin cậy{Style.RESET_ALL}", terminal_width))
    print(center_text(f"{Fore.MAGENTA}● Hỗ trợ tất cả các loại URL TikTok{Style.RESET_ALL}", terminal_width))
    print("\n")
    
    version_str = f"{__version__}"
    author_str = "toihoccode1405"
    info_text = f"{Fore.WHITE}Phiên bản: {Fore.GREEN}v{version_str}{Fore.WHITE} | Tác giả: {Fore.GREEN}{author_str}{Style.RESET_ALL}"
    print(center_text(info_text, terminal_width))
    print("\n")

def show_interactive_menu():
    """Hiển thị menu tương tác với thiết kế hiện đại"""
    downloader = TikTokDownloader()
    terminal_width = get_terminal_width()
    
    while True:
        clear_screen()
        print_banner()
        
        # Menu chính với thiết kế hiện đại
        menu_title = f"{Fore.WHITE}━━━━━━━━━━━━━━━━ {Fore.CYAN}MENU CHÍNH{Fore.WHITE} ━━━━━━━━━━━━━━━━{Style.RESET_ALL}"
        print(center_text(menu_title, terminal_width))
        print("\n")
        
        menu_items = [
            f"{Fore.GREEN}1. {Fore.WHITE}Tải video TikTok{Style.RESET_ALL}",
            f"{Fore.GREEN}1.1 {Fore.WHITE}Tải nhiều video cùng lúc{Style.RESET_ALL}",
            f"{Fore.GREEN}2. {Fore.WHITE}Xem lịch sử tải xuống{Style.RESET_ALL}",
            f"{Fore.GREEN}3. {Fore.WHITE}Xuất lịch sử ra file{Style.RESET_ALL}",
            f"{Fore.GREEN}4. {Fore.WHITE}Xóa lịch sử tải xuống{Style.RESET_ALL}",
            f"{Fore.GREEN}5. {Fore.WHITE}Kiểm tra cập nhật{Style.RESET_ALL}",
            f"{Fore.RED}0. {Fore.WHITE}Thoát{Style.RESET_ALL}"
        ]
        
        for item in menu_items:
            print(center_text(item, terminal_width))
        
        print("\n")
        print(center_text(f"{Fore.YELLOW}❯❯❯{Style.RESET_ALL}", terminal_width))
        
        try:
            choice = input(center_text(f"{Fore.GREEN}Chọn chức năng (0-5): {Style.RESET_ALL}", terminal_width, fill_char=''))
            
            if choice == '0':
                clear_screen()
                print("\n\n")
                print(center_text(f"{Fore.CYAN}Cảm ơn bạn đã sử dụng TikTok Downloader!{Style.RESET_ALL}", terminal_width))
                print(center_text(f"{Fore.YELLOW}Tạm biệt và hẹn gặp lại!{Style.RESET_ALL}", terminal_width))
                print("\n\n")
                break
                
            elif choice == '1':
                download_video_interactive(downloader)
                
            elif choice == '1.1':
                batch_download_interactive(downloader)

            elif choice == '2':
                show_history_interactive(downloader)
                
            elif choice == '3':
                export_history_interactive(downloader)
                
            elif choice == '4':
                clear_history_interactive(downloader)
                
            elif choice == '5':
                check_updates_interactive()
                
            else:
                print(center_text(f"{Fore.RED}Lỗi: Tùy chọn không hợp lệ!{Style.RESET_ALL}", terminal_width))
                time.sleep(1)
                
        except Exception as e:
            print(center_text(f"{Fore.RED}Lỗi: {e}{Style.RESET_ALL}", terminal_width))
            input(center_text(f"{Fore.YELLOW}Nhấn Enter để tiếp tục...{Style.RESET_ALL}", terminal_width, fill_char=''))

def show_history_interactive(downloader):
    """Hiển thị lịch sử tải xuống với UI hiện đại"""
    terminal_width = get_terminal_width()
    
    clear_screen()
    print("\n")
    title = f"{Fore.WHITE}━━━━━━━━━━━━━━━━ {Fore.CYAN}LỊCH SỬ TẢI XUỐNG{Fore.WHITE} ━━━━━━━━━━━━━━━━{Style.RESET_ALL}"
    print(center_text(title, terminal_width))
    print("\n")
    
    downloader.show_history()
    print("\n")
    input(center_text(f"{Fore.YELLOW}[Nhấn Enter để quay lại menu chính]{Style.RESET_ALL}", terminal_width, fill_char=''))

def clear_history_interactive(downloader):
    """Xóa lịch sử tải xuống với UI hiện đại"""
    terminal_width = get_terminal_width()
    
    clear_screen()
    print("\n")
    title = f"{Fore.WHITE}━━━━━━━━━━━━━━━━ {Fore.CYAN}XÓA LỊCH SỬ{Fore.WHITE} ━━━━━━━━━━━━━━━━{Style.RESET_ALL}"
    print(center_text(title, terminal_width))
    print("\n")
    
    warning = f"{Fore.RED}⚠ CẢNH BÁO: Hành động này không thể hoàn tác!{Style.RESET_ALL}"
    print(center_text(warning, terminal_width))
    print("\n")
    
    confirm = input(center_text(f"{Fore.YELLOW}Bạn có chắc chắn muốn xóa tất cả lịch sử? (y/n): {Style.RESET_ALL}", terminal_width, fill_char=''))
    if confirm.lower() == 'y':
        downloader.download_history = []
        downloader.save_history()
        print("\n")
        success = f"{Fore.GREEN}✅ Đã xóa lịch sử tải xuống thành công!{Style.RESET_ALL}"
        print(center_text(success, terminal_width))
        time.sleep(2)
    else:
        print("\n")
        cancel = f"{Fore.YELLOW}⚪ Đã hủy thao tác xóa lịch sử.{Style.RESET_ALL}"
        print(center_text(cancel, terminal_width))
        time.sleep(2)

def download_video_interactive(downloader):
    """Giao diện tương tác để tải video với UI hiện đại"""
    terminal_width = get_terminal_width()
    
    while True:
        clear_screen()
        print("\n")
        title = f"{Fore.WHITE}━━━━━━━━━━━━━━━━ {Fore.CYAN}TẢI VIDEO TIKTOK{Fore.WHITE} ━━━━━━━━━━━━━━━━{Style.RESET_ALL}"
        print(center_text(title, terminal_width))
        print("\n")
        
        url_prompt = f"{Fore.YELLOW}Nhập URL video TikTok {Fore.CYAN}(nhập 'q' để quay lại menu){Fore.YELLOW}: {Style.RESET_ALL}"
        url = input(center_text(url_prompt, terminal_width, fill_char=''))
        
        if url.lower() == 'q':
            break
            
        if not url:
            print("\n")
            error = f"{Fore.RED}⛔ Lỗi: URL không được để trống!{Style.RESET_ALL}"
            print(center_text(error, terminal_width))
            time.sleep(1.5)
            continue
        
        print("\n")    
        quality_title = f"{Fore.CYAN}Chọn chất lượng video:{Style.RESET_ALL}"
        print(center_text(quality_title, terminal_width))
        print(center_text(f"{Fore.GREEN}1. {Fore.WHITE}Cao (HD){Style.RESET_ALL}", terminal_width))
        print(center_text(f"{Fore.GREEN}2. {Fore.WHITE}Trung bình{Style.RESET_ALL}", terminal_width))
        print("\n")
        
        quality_choice = input(center_text(f"{Fore.YELLOW}Chọn chất lượng (1-2): {Style.RESET_ALL}", terminal_width, fill_char=''))
        
        quality = "high" if quality_choice != "2" else "medium"
        
        # Hiển thị animation tải xuống
        print("\n")
        loading_text = f"{Fore.CYAN}Đang xử lý yêu cầu tải xuống...{Style.RESET_ALL}"
        print(center_text(loading_text, terminal_width))
        
        for _ in range(3):
            sys.stdout.write(center_text(f"{Fore.CYAN}. {Style.RESET_ALL}", terminal_width, fill_char=''))
            sys.stdout.flush()
            time.sleep(0.5)
        print("\n")
        
        # Tải video
        success = downloader.download_video(url, quality)
        
        if success:
            print("\n")
            success_icon = f"{Fore.GREEN}✅ TẢI XUỐNG THÀNH CÔNG!{Style.RESET_ALL}"
            print(center_text(success_icon, terminal_width))
            print("\n")
            note_line1 = f"{Fore.YELLOW}Lưu ý: Nếu video vẫn có watermark, có thể nó đã được nhúng{Style.RESET_ALL}"
            note_line2 = f"{Fore.YELLOW}trực tiếp trong nội dung bởi người tạo, không phải lỗi của phần mềm.{Style.RESET_ALL}"
            print(center_text(note_line1, terminal_width))
            print(center_text(note_line2, terminal_width))
        else:
            print("\n")
            error_icon = f"{Fore.RED}❌ TẢI XUỐNG THẤT BẠI!{Style.RESET_ALL}"
            print(center_text(error_icon, terminal_width))
            print("\n")
            error_note = f"{Fore.YELLOW}Vui lòng kiểm tra lại URL hoặc thử lại sau.{Style.RESET_ALL}"
            print(center_text(error_note, terminal_width))
        
        print("\n")
        input(center_text(f"{Fore.YELLOW}[Nhấn Enter để tiếp tục...]{Style.RESET_ALL}", terminal_width, fill_char=''))

def export_history_interactive(downloader):
    """Giao diện tương tác để xuất lịch sử với UI hiện đại"""
    terminal_width = get_terminal_width()
    
    clear_screen()
    print("\n")
    title = f"{Fore.WHITE}━━━━━━━━━━━━━━━━ {Fore.CYAN}XUẤT LỊCH SỬ TẢI XUỐNG{Fore.WHITE} ━━━━━━━━━━━━━━━━{Style.RESET_ALL}"
    print(center_text(title, terminal_width))
    print("\n")
    
    format_title = f"{Fore.CYAN}Chọn định dạng xuất:{Style.RESET_ALL}"
    print(center_text(format_title, terminal_width))
    print(center_text(f"{Fore.GREEN}1. {Fore.WHITE}Văn bản (TXT){Style.RESET_ALL}", terminal_width))
    print(center_text(f"{Fore.GREEN}2. {Fore.WHITE}Bảng tính (CSV){Style.RESET_ALL}", terminal_width))
    print("\n")
    
    choice = input(center_text(f"{Fore.YELLOW}Chọn định dạng (1-2): {Style.RESET_ALL}", terminal_width, fill_char=''))
    
    format_type = "txt" if choice != "2" else "csv"
    
    # Hiển thị animation xử lý
    print("\n")
    processing = f"{Fore.CYAN}Đang xử lý...{Style.RESET_ALL}"
    print(center_text(processing, terminal_width))
    time.sleep(1)
    
    success = downloader.export_history(format_type)
    
    if success:
        print("\n")
        success_msg = f"{Fore.GREEN}✅ Xuất lịch sử thành công!{Style.RESET_ALL}"
        print(center_text(success_msg, terminal_width))
    else:
        print("\n")
        error_msg = f"{Fore.RED}❌ Không thể xuất lịch sử. Vui lòng thử lại sau.{Style.RESET_ALL}"
        print(center_text(error_msg, terminal_width))
    
    print("\n")    
    input(center_text(f"{Fore.YELLOW}[Nhấn Enter để quay lại menu chính...]{Style.RESET_ALL}", terminal_width, fill_char=''))

def check_updates_interactive():
    """Giao diện tương tác để kiểm tra cập nhật với UI hiện đại"""
    terminal_width = get_terminal_width()
    
    clear_screen()
    print("\n")
    title = f"{Fore.WHITE}━━━━━━━━━━━━━━━━ {Fore.CYAN}KIỂM TRA CẬP NHẬT{Fore.WHITE} ━━━━━━━━━━━━━━━━{Style.RESET_ALL}"
    print(center_text(title, terminal_width))
    print("\n")
    
    checking = f"{Fore.YELLOW}Đang kiểm tra cập nhật từ máy chủ...{Style.RESET_ALL}"
    print(center_text(checking, terminal_width))
    
    # Tạo hiệu ứng đang tải đẹp hơn
    loader = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    for i in range(8):
        sys.stdout.write(center_text(f"\r{Fore.CYAN}{loader[i]}{Style.RESET_ALL}", terminal_width, fill_char=''))
        sys.stdout.flush()
        time.sleep(0.2)
    print("\n")
    
    updater = Updater()
    has_update, latest_version = updater.check_for_updates()
    
    if has_update:
        print("\n")
        update_available = f"{Fore.GREEN}🔔 CÓ PHIÊN BẢN MỚI KHẢ DỤNG!{Style.RESET_ALL}"
        print(center_text(update_available, terminal_width))
        print("\n")
        
        current_ver = f"{Fore.WHITE}Phiên bản hiện tại: {Fore.YELLOW}{updater.current_version}{Style.RESET_ALL}"
        new_ver = f"{Fore.WHITE}Phiên bản mới: {Fore.YELLOW}{latest_version}{Style.RESET_ALL}"
        print(center_text(current_ver, terminal_width))
        print(center_text(new_ver, terminal_width))
        
        print("\n")
        update_prompt = f"{Fore.CYAN}Bạn có muốn cập nhật ngay bây giờ không?{Style.RESET_ALL}"
        print(center_text(update_prompt, terminal_width))
        print("\n")
        
        update_choice = input(center_text(f"{Fore.YELLOW}Cập nhật ngay (y/n): {Style.RESET_ALL}", terminal_width, fill_char=''))
        
        if update_choice.lower() == 'y':
            print("\n")
            updating = f"{Fore.CYAN}Đang cập nhật...{Style.RESET_ALL}"
            print(center_text(updating, terminal_width))
            
            # Animation cập nhật
            for i in range(10):
                bar = "█" * i + "░" * (10 - i)
                percent = i * 10
                sys.stdout.write(center_text(f"\r{Fore.CYAN}[{bar}] {percent}%{Style.RESET_ALL}", terminal_width, fill_char=''))
                sys.stdout.flush()
                time.sleep(0.3)
            print("\n")
            
            success = updater.perform_update()
            
            if success:
                print("\n")
                update_success = f"{Fore.GREEN}✅ Cập nhật thành công! Vui lòng khởi động lại ứng dụng.{Style.RESET_ALL}"
                print(center_text(update_success, terminal_width))
            else:
                print("\n")
                update_failed = f"{Fore.RED}❌ Cập nhật thất bại. Vui lòng thử lại sau.{Style.RESET_ALL}"
                print(center_text(update_failed, terminal_width))
    else:
        print("\n")
        latest_ver = f"{Fore.GREEN}✓ BẠN ĐANG SỬ DỤNG PHIÊN BẢN MỚI NHẤT!{Style.RESET_ALL}"
        print(center_text(latest_ver, terminal_width))
        print("\n")
        
        current_ver = f"{Fore.WHITE}Phiên bản hiện tại: {Fore.YELLOW}{updater.current_version}{Style.RESET_ALL}"
        print(center_text(current_ver, terminal_width))
    
    print("\n")
    input(center_text(f"{Fore.YELLOW}[Nhấn Enter để quay lại menu chính...]{Style.RESET_ALL}", terminal_width, fill_char=''))

def batch_download_interactive(downloader):
    """Giao diện tương tác tải nhiều video cùng lúc"""
    terminal_width = get_terminal_width()
    clear_screen()
    print("\n")
    title = f"{Fore.WHITE}━━━━━━━━━━━━━━━━ {Fore.CYAN}TẢI NHIỀU VIDEO{Fore.WHITE} ━━━━━━━━━━━━━━━━{Style.RESET_ALL}"
    print(center_text(title, terminal_width))
    print("\n")
    
    info = f"{Fore.YELLOW}Nhập các URL TikTok mỗi URL trên một dòng.{Style.RESET_ALL}"
    print(center_text(info, terminal_width))
    print(center_text(f"{Fore.YELLOW}Nhập dòng trống để hoàn tất.{Style.RESET_ALL}", terminal_width))
    print("\n")
    
    urls = []
    count = 1
    while True:
        url = input(center_text(f"{Fore.GREEN}Video {count}: {Style.RESET_ALL}", terminal_width, fill_char=''))
        if not url:
            break
        urls.append(url)
        count += 1
    
    if not urls:
        print("\n")
        print(center_text(f"{Fore.RED}Không có URL nào được nhập.{Style.RESET_ALL}", terminal_width))
        time.sleep(1.5)
        return
        
    print("\n")    
    quality_title = f"{Fore.CYAN}Chọn chất lượng video:{Style.RESET_ALL}"
    print(center_text(quality_title, terminal_width))
    print(center_text(f"{Fore.GREEN}1. {Fore.WHITE}Cao (HD){Style.RESET_ALL}", terminal_width))
    print(center_text(f"{Fore.GREEN}2. {Fore.WHITE}Trung bình{Style.RESET_ALL}", terminal_width))
    print("\n")
    
    quality_choice = input(center_text(f"{Fore.YELLOW}Chọn chất lượng (1-2): {Style.RESET_ALL}", terminal_width, fill_char=''))
    quality = "high" if quality_choice != "2" else "medium"
    
    # Hiển thị animation tải xuống
    print("\n")
    batch_progress = f"{Fore.CYAN}Đang tải {len(urls)} video...{Style.RESET_ALL}"
    print(center_text(batch_progress, terminal_width))
    print("\n")
    
    success_count = 0
    fail_count = 0
    
    for i, url in enumerate(urls):
        progress_text = f"{Fore.YELLOW}Đang xử lý video {i+1}/{len(urls)}{Style.RESET_ALL}"
        print(center_text(progress_text, terminal_width))
        
        # Hiển thị URL đang tải
        short_url = url[:50] + "..." if len(url) > 50 else url
        url_text = f"{Fore.CYAN}{short_url}{Style.RESET_ALL}"
        print(center_text(url_text, terminal_width))
        
        # Hiển thị animation tiến trình
        for j in range(5):
            bar = "█" * j + "░" * (5 - j)
            sys.stdout.write(center_text(f"\r{Fore.CYAN}[{bar}]{Style.RESET_ALL}", terminal_width, fill_char=''))
            sys.stdout.flush()
            time.sleep(0.1)
        
        # Tải video
        success = downloader.download_video(url, quality)
        
        if success:
            success_text = f"{Fore.GREEN}✓ Thành công{Style.RESET_ALL}"
            print(center_text(success_text, terminal_width))
            success_count += 1
        else:
            fail_text = f"{Fore.RED}✗ Thất bại{Style.RESET_ALL}"
            print(center_text(fail_text, terminal_width))
            fail_count += 1
            
        print()
    
    # Hiển thị kết quả tổng quan
    print("\n")
    summary_title = f"{Fore.WHITE}━━━━━━━━━━━━━━━━ {Fore.CYAN}KẾT QUẢ{Fore.WHITE} ━━━━━━━━━━━━━━━━{Style.RESET_ALL}"
    print(center_text(summary_title, terminal_width))
    print("\n")
    
    total_text = f"{Fore.WHITE}Tổng số video: {Fore.YELLOW}{len(urls)}{Style.RESET_ALL}"
    success_text = f"{Fore.GREEN}Tải thành công: {success_count}{Style.RESET_ALL}"
    fail_text = f"{Fore.RED}Tải thất bại: {fail_count}{Style.RESET_ALL}"
    
    print(center_text(total_text, terminal_width))
    print(center_text(success_text, terminal_width))
    print(center_text(fail_text, terminal_width))
    
    print("\n")
    input(center_text(f"{Fore.YELLOW}[Nhấn Enter để tiếp tục...]{Style.RESET_ALL}", terminal_width, fill_char=''))

# Các hàm run_cli() và main() giữ nguyên như trước
def run_cli():
    """Chạy ứng dụng dòng lệnh"""
    parser = argparse.ArgumentParser(description='TikTok Video Downloader')
    parser.add_argument('--url', help='URL của video TikTok cần tải')
    parser.add_argument('--quality', choices=['high', 'medium'], default='high', 
                      help='Chất lượng video (mặc định: high)')
    parser.add_argument('--menu', action='store_true', help='Hiển thị menu tương tác')
    parser.add_argument('--version', action='store_true', help='Hiển thị phiên bản')
    parser.add_argument('--export', choices=['txt', 'csv'], help='Xuất lịch sử tải xuống')
    
    args = parser.parse_args()
    
    # Khởi tạo colorama
    init()
    
    if args.version:
        try:
            from .. import __version__
        except:
            try:
                from tiktok_downloader import __version__
            except:
                __version__ = "1.2.2"
                
        print(f"TikTok Downloader v{__version__}")
        return
        
    elif args.menu or len(sys.argv) == 1:
        # Chế độ menu tương tác
        show_interactive_menu()
        return
        
    # Xử lý các tham số command line khác
    downloader = TikTokDownloader()
    
    if args.export:
        success = downloader.export_history(args.export)
        if success:
            print(f"Đã xuất lịch sử ra file .{args.export}")
        else:
            print("Không thể xuất lịch sử.")
        return
        
    if args.url:
        print(f"Đang tải video từ: {args.url}")
        print(f"Chất lượng: {args.quality}")
        success = downloader.download_video(args.url, args.quality)
        
        if success:
            print("Tải xuống thành công!")
        else:
            print("Tải xuống thất bại. Vui lòng kiểm tra lại URL hoặc thử lại sau.")
        return
    
    # Nếu không có tham số nào, hiển thị menu
    show_interactive_menu()

def main():
    """Hàm main để chạy từ command line"""
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nĐã hủy bởi người dùng.")
    except Exception as e:
        print(f"Lỗi không mong muốn: {str(e)}")
        
if __name__ == "__main__":
    main()