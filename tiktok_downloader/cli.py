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

def print_banner():
    """Hiển thị banner đẹp mắt khi khởi động ứng dụng"""
    terminal_width = shutil.get_terminal_size().columns
    banner_width = 60
    padding = max(0, (terminal_width - banner_width) // 2)
    
    clear_screen()
    print("\n" + " " * padding + f"{Fore.CYAN}╔{'═' * 58}╗{Style.RESET_ALL}")
    print(" " * padding + f"{Fore.CYAN}║{Style.RESET_ALL}{Back.CYAN}{Fore.BLACK}                  TIKTOK VIDEO DOWNLOADER                  {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
    print(" " * padding + f"{Fore.CYAN}║{Style.RESET_ALL}{' ' * 58}{Fore.CYAN}║{Style.RESET_ALL}")
    print(" " * padding + f"{Fore.CYAN}║{Style.RESET_ALL}{Fore.GREEN}  ▶ Tải video TikTok không có watermark{' ' * 23}{Fore.CYAN}║{Style.RESET_ALL}")
    print(" " * padding + f"{Fore.CYAN}║{Style.RESET_ALL}{Fore.YELLOW}  ▶ Nhiều nguồn API để đảm bảo độ tin cậy{' ' * 19}{Fore.CYAN}║{Style.RESET_ALL}")
    print(" " * padding + f"{Fore.CYAN}║{Style.RESET_ALL}{Fore.MAGENTA}  ▶ Hỗ trợ tất cả các loại URL TikTok{' ' * 24}{Fore.CYAN}║{Style.RESET_ALL}")
    print(" " * padding + f"{Fore.CYAN}║{Style.RESET_ALL}{' ' * 58}{Fore.CYAN}║{Style.RESET_ALL}")
    
    # Hiển thị phiên bản
    try:
        from .. import __version__
    except:
        try:
            from tiktok_downloader import __version__
        except:
            __version__ = "1.2.2"
            
    version_str = f"v{__version__}"
    print(" " * padding + f"{Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}  Phiên bản: {Fore.GREEN}{version_str}{' ' * (45 - len(version_str))}{Fore.CYAN}║{Style.RESET_ALL}")
    print(" " * padding + f"{Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}  Tác giả: {Fore.GREEN}toihoccode1405{' ' * 32}{Fore.CYAN}║{Style.RESET_ALL}")
    print(" " * padding + f"{Fore.CYAN}╚{'═' * 58}╝{Style.RESET_ALL}\n")

def show_interactive_menu():
    """Hiển thị menu tương tác trực quan"""
    downloader = TikTokDownloader()
    
    while True:
        clear_screen()
        print_banner()
        
        print(f"{Fore.CYAN}╔{'═' * 58}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}{Back.CYAN}{Fore.BLACK}                       MENU CHÍNH                       {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * 58}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}1.{Style.RESET_ALL} Tải video TikTok{' ' * 38}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}2.{Style.RESET_ALL} Xem lịch sử tải xuống{' ' * 34}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}3.{Style.RESET_ALL} Xuất lịch sử ra file{' ' * 35}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}4.{Style.RESET_ALL} Xóa lịch sử tải xuống{' ' * 34}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}5.{Style.RESET_ALL} Kiểm tra cập nhật{' ' * 37}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}0.{Style.RESET_ALL} Thoát{' ' * 51}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * 58}╝{Style.RESET_ALL}\n")
        
        try:
            choice = input(f"{Fore.GREEN}Chọn chức năng (0-5): {Style.RESET_ALL}")
            
            if choice == '0':
                clear_screen()
                print(f"\n{Fore.CYAN}Cảm ơn bạn đã sử dụng TikTok Downloader!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Tạm biệt và hẹn gặp lại!{Style.RESET_ALL}\n")
                break
                
            elif choice == '1':
                download_video_interactive(downloader)
                
            elif choice == '2':
                clear_screen()
                print(f"\n{Fore.CYAN}╔{'═' * 58}╗{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}{Back.CYAN}{Fore.BLACK}                   LỊCH SỬ TẢI XUỐNG                   {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
                print(f"{Fore.CYAN}╚{'═' * 58}╝{Style.RESET_ALL}\n")
                downloader.show_history()
                input(f"\n{Fore.YELLOW}Nhấn Enter để quay lại menu chính...{Style.RESET_ALL}")
                
            elif choice == '3':
                export_history_interactive(downloader)
                
            elif choice == '4':
                clear_screen()
                print(f"\n{Fore.CYAN}╔{'═' * 58}╗{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL}{Back.CYAN}{Fore.BLACK}                    XÓA LỊCH SỬ                        {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
                print(f"{Fore.CYAN}╚{'═' * 58}╝{Style.RESET_ALL}\n")
                confirm = input(f"{Fore.RED}Bạn có chắc chắn muốn xóa tất cả lịch sử? (y/n): {Style.RESET_ALL}")
                if confirm.lower() == 'y':
                    downloader.download_history = []
                    downloader.save_history()
                    print(f"\n{Fore.GREEN}Đã xóa lịch sử tải xuống thành công!{Style.RESET_ALL}")
                    time.sleep(2)
                
            elif choice == '5':
                check_updates_interactive()
                
            else:
                print(f"{Fore.RED}Lỗi: Tùy chọn không hợp lệ!{Style.RESET_ALL}")
                time.sleep(1)
                
        except Exception as e:
            print(f"{Fore.RED}Lỗi: {e}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Nhấn Enter để tiếp tục...{Style.RESET_ALL}")

def download_video_interactive(downloader):
    """Giao diện tương tác để tải video"""
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}╔{'═' * 58}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}{Back.CYAN}{Fore.BLACK}                   TẢI VIDEO TIKTOK                    {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * 58}╝{Style.RESET_ALL}\n")
        
        url = input(f"{Fore.YELLOW}Nhập URL video TikTok {Fore.CYAN}(nhập 'q' để quay lại menu){Fore.YELLOW}: {Style.RESET_ALL}")
        
        if url.lower() == 'q':
            break
            
        if not url:
            print(f"{Fore.RED}Lỗi: URL không được để trống!{Style.RESET_ALL}")
            time.sleep(1.5)
            continue
            
        print(f"\n{Fore.CYAN}Chọn chất lượng video:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}1.{Style.RESET_ALL} Cao (HD)")
        print(f"  {Fore.GREEN}2.{Style.RESET_ALL} Trung bình")
        quality_choice = input(f"\n{Fore.YELLOW}Chọn chất lượng (1-2): {Style.RESET_ALL}")
        
        quality = "high" if quality_choice != "2" else "medium"
        
        # Hiển thị animation hoặc thanh tiến trình
        print(f"\n{Fore.CYAN}Đang xử lý yêu cầu tải xuống...{Style.RESET_ALL}")
        
        # Tải video
        success = downloader.download_video(url, quality)
        
        if success:
            print(f"\n{Fore.GREEN}┌{'─' * 58}┐{Style.RESET_ALL}")
            print(f"{Fore.GREEN}│{Back.GREEN}{Fore.BLACK}              TẢI XUỐNG THÀNH CÔNG!                   {Style.RESET_ALL}{Fore.GREEN}│{Style.RESET_ALL}")
            print(f"{Fore.GREEN}└{'─' * 58}┘{Style.RESET_ALL}")

            print(f"\n{Fore.YELLOW}Lưu ý: Nếu video vẫn có watermark, có thể nó đã được nhúng{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}trực tiếp trong nội dung bởi người tạo, không phải lỗi của phần mềm.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}┌{'─' * 58}┐{Style.RESET_ALL}")
            print(f"{Fore.RED}│{Back.RED}{Fore.WHITE}              TẢI XUỐNG THẤT BẠI!                     {Style.RESET_ALL}{Fore.RED}│{Style.RESET_ALL}")
            print(f"{Fore.RED}│{' ' * 58}│{Style.RESET_ALL}")
            print(f"{Fore.RED}│  {Fore.YELLOW}Vui lòng kiểm tra lại URL hoặc thử lại sau.{' ' * 16}{Fore.RED}│{Style.RESET_ALL}")
            print(f"{Fore.RED}└{'─' * 58}┘{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Nhấn Enter để tiếp tục...{Style.RESET_ALL}")

def export_history_interactive(downloader):
    """Giao diện tương tác để xuất lịch sử"""
    clear_screen()
    print(f"\n{Fore.CYAN}╔{'═' * 58}╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}{Back.CYAN}{Fore.BLACK}                XUẤT LỊCH SỬ TẢI XUỐNG                {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚{'═' * 58}╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Chọn định dạng xuất:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}1.{Style.RESET_ALL} Văn bản (TXT)")
    print(f"  {Fore.GREEN}2.{Style.RESET_ALL} Bảng tính (CSV)")
    choice = input(f"\n{Fore.YELLOW}Chọn định dạng (1-2): {Style.RESET_ALL}")
    
    format_type = "txt" if choice != "2" else "csv"
    
    success = downloader.export_history(format_type)
    
    if success:
        print(f"\n{Fore.GREEN}Xuất lịch sử thành công!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Không thể xuất lịch sử. Vui lòng thử lại sau.{Style.RESET_ALL}")
        
    input(f"\n{Fore.YELLOW}Nhấn Enter để quay lại menu chính...{Style.RESET_ALL}")

def check_updates_interactive():
    """Giao diện tương tác để kiểm tra cập nhật"""
    clear_screen()
    print(f"\n{Fore.CYAN}╔{'═' * 58}╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}{Back.CYAN}{Fore.BLACK}                   KIỂM TRA CẬP NHẬT                  {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚{'═' * 58}╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}Đang kiểm tra cập nhật từ máy chủ...{Style.RESET_ALL}")
    
    # Tạo hiệu ứng đang tải
    for _ in range(3):
        sys.stdout.write(f"{Fore.CYAN}.{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.5)
    print("\n")
    
    updater = Updater()
    has_update, latest_version = updater.check_for_updates()
    
    if has_update:
        print(f"{Fore.GREEN}┌{'─' * 58}┐{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│{Back.GREEN}{Fore.BLACK}            CÓ PHIÊN BẢN MỚI KHẢ DỤNG!                {Style.RESET_ALL}{Fore.GREEN}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│{' ' * 58}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│  {Fore.WHITE}Phiên bản hiện tại: {Fore.YELLOW}{updater.current_version}{' ' * 30}{Fore.GREEN}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│  {Fore.WHITE}Phiên bản mới: {Fore.YELLOW}{latest_version}{' ' * 35}{Fore.GREEN}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}└{'─' * 58}┘{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Bạn có muốn cập nhật ngay bây giờ không?{Style.RESET_ALL}")
        update_choice = input(f"{Fore.YELLOW}Cập nhật ngay (y/n): {Style.RESET_ALL}")
        
        if update_choice.lower() == 'y':
            print(f"\n{Fore.CYAN}Đang cập nhật...{Style.RESET_ALL}")
            success = updater.perform_update()
            
            if success:
                print(f"\n{Fore.GREEN}Cập nhật thành công! Vui lòng khởi động lại ứng dụng.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Cập nhật thất bại. Vui lòng thử lại sau.{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}┌{'─' * 58}┐{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│{Back.GREEN}{Fore.BLACK}          BẠN ĐANG SỬ DỤNG PHIÊN BẢN MỚI NHẤT!        {Style.RESET_ALL}{Fore.GREEN}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│{' ' * 58}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│  {Fore.WHITE}Phiên bản hiện tại: {Fore.YELLOW}{updater.current_version}{' ' * 30}{Fore.GREEN}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}└{'─' * 58}┘{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Nhấn Enter để quay lại menu chính...{Style.RESET_ALL}")

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
    parser.add_argument('--menu', action='store_true', help='Hiển thị menu tương tác')
    
    args = parser.parse_args()
    
    # Kiểm tra cập nhật tự động theo định kỳ
    updater = Updater()
    updater.check_for_updates(auto_update=False)
    
    # Xử lý các tùy chọn dòng lệnh
    if args.check_update or args.update:
        if args.update:
            updater.perform_update()
            return
        else:
            has_update, latest_version = updater.check_for_updates()
            if not has_update:
                print(f"{Fore.GREEN}Bạn đang sử dụng phiên bản mới nhất ({updater.current_version}).{Style.RESET_ALL}")
            return
    
    # Khởi tạo downloader
    downloader = TikTokDownloader()
    
    if args.history:
        print(f"\n{Fore.CYAN}╔{'═' * 58}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}{Back.CYAN}{Fore.BLACK}                   LỊCH SỬ TẢI XUỐNG                   {Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * 58}╝{Style.RESET_ALL}\n")
        downloader.show_history()
        return
        
    if args.clear_history:
        if input(f"{Fore.RED}Bạn có chắc chắn muốn xóa tất cả lịch sử? (y/n): {Style.RESET_ALL}").lower() == 'y':
            downloader.download_history = []
            downloader.save_history()
            print(f"{Fore.GREEN}Đã xóa lịch sử tải xuống.{Style.RESET_ALL}")
        return
    
    if args.export:
        print(f"\n{Fore.CYAN}Đang xuất lịch sử ra file {args.export.upper()}...{Style.RESET_ALL}")
        downloader.export_history(args.export)
        return
    
    # Hiển thị menu tương tác nếu được yêu cầu hoặc không có URL
    if args.menu or not args.url:
        show_interactive_menu()
        return
        
    # Nếu URL được cung cấp, tiến hành tải video
    success = downloader.download_video(args.url, args.quality)
    if success:
        print(f"{Fore.GREEN}Tải xuống thành công!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Tải xuống không thành công. Vui lòng thử lại sau.{Style.RESET_ALL}")

if __name__ == "__main__":
    run_cli()