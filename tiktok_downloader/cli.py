from colorama import init, Fore, Style
import os
import sys
import platform
from datetime import datetime
from .downloader import TikTokDownloader

# Khởi tạo colorama
init(autoreset=True)

class TikTokDownloaderCLI:
    def __init__(self):
        self.downloader = TikTokDownloader()
    
    def clear_screen(self):
        """Xóa màn hình phù hợp với hệ điều hành"""
        os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    def show_header(self):
        """Hiển thị header ứng dụng"""
        self.clear_screen()
        app_info = self.downloader.config.get_app_info()
        
        print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Fore.WHITE}      TIKTOK DOWNLOADER NO LOGO      {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠══════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}Phiên bản:{Fore.WHITE} {app_info['version']:<22} {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}Người dùng:{Fore.WHITE} {app_info['current_user']:<20} {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
        print()
    
    def show_menu(self):
        """Hiển thị menu chính"""
        self.show_header()
        print(f"{Fore.GREEN}1. Tải video TikTok{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. Xem lịch sử tải{Style.RESET_ALL}")
        print(f"{Fore.GREEN}3. Thay đổi thư mục lưu{Style.RESET_ALL}")
        print(f"{Fore.GREEN}4. Cài đặt ứng dụng{Style.RESET_ALL}")
        print(f"{Fore.GREEN}5. Thông tin ứng dụng{Style.RESET_ALL}")
        print(f"{Fore.GREEN}6. Thoát{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════{Style.RESET_ALL}")
        
        while True:
            choice = input(f"{Fore.YELLOW}Chọn chức năng (1-6): {Style.RESET_ALL}")
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            print(f"{Fore.RED}Lựa chọn không hợp lệ. Vui lòng chọn lại.{Style.RESET_ALL}")
    
    def download_video_menu(self):
        """Menu tải video"""
        self.show_header()
        print(f"{Fore.CYAN}═══ TẢI VIDEO TIKTOK ════{Style.RESET_ALL}")
        
        url = input(f"{Fore.YELLOW}Nhập URL video TikTok: {Style.RESET_ALL}")
        if not url.strip():
            print(f"{Fore.RED}URL không được để trống!{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Nhấn Enter để tiếp tục...{Style.RESET_ALL}")
            return
            
        print(f"{Fore.CYAN}Chọn chất lượng video:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Cao (HD){Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. Trung bình{Style.RESET_ALL}")
        
        while True:
            quality_choice = input(f"{Fore.YELLOW}Chọn chất lượng (1-2): {Style.RESET_ALL}")
            if quality_choice in ['1', '2']:
                break
            print(f"{Fore.RED}Lựa chọn không hợp lệ. Vui lòng chọn lại.{Style.RESET_ALL}")
        
        quality = "high" if quality_choice == '1' else "medium"
        
        print(f"{Fore.CYAN}Đang xử lý yêu cầu tải xuống...{Style.RESET_ALL}")
        success = self.downloader.download_video(url, quality)
        
        if success:
            print(f"{Fore.GREEN}Tải xuống hoàn tất!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Tải xuống không thành công. Vui lòng thử lại sau.{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Nhấn Enter để tiếp tục...{Style.RESET_ALL}")
    
    def show_history_menu(self):
        """Menu xem lịch sử tải"""
        self.show_header()
        print(f"{Fore.CYAN}═══ LỊCH SỬ TẢI VIDEO ════{Style.RESET_ALL}")
        
        self.downloader.show_history()
        
        print(f"{Fore.CYAN}═══════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Xóa lịch sử{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. Quay lại menu chính{Style.RESET_ALL}")
        
        while True:
            choice = input(f"{Fore.YELLOW}Chọn chức năng (1-2): {Style.RESET_ALL}")
            if choice == '1':
                confirm = input(f"{Fore.YELLOW}Bạn có chắc muốn xóa toàn bộ lịch sử? (y/n): {Style.RESET_ALL}")
                if confirm.lower() == 'y':
                    self.downloader.download_history = []
                    self.downloader.save_history()
                    print(f"{Fore.GREEN}Đã xóa lịch sử tải.{Style.RESET_ALL}")
                break
            elif choice == '2':
                break
            else:
                print(f"{Fore.RED}Lựa chọn không hợp lệ. Vui lòng chọn lại.{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Nhấn Enter để tiếp tục...{Style.RESET_ALL}")
    
    def change_folder_menu(self):
        """Menu thay đổi thư mục lưu"""
        self.show_header()
        print(f"{Fore.CYAN}═══ THAY ĐỔI THƯ MỤC LƯU ════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Thư mục hiện tại: {self.downloader.download_folder}{Style.RESET_ALL}")
        
        new_folder = input(f"{Fore.YELLOW}Nhập đường dẫn thư mục mới (để trống để hủy): {Style.RESET_ALL}")
        
        if new_folder.strip():
            # Mở rộng đường dẫn ~
            if new_folder.startswith('~'):
                new_folder = os.path.expanduser(new_folder)
                
            # Chuyển đổi dấu gạch chéo phù hợp với hệ điều hành
            new_folder = os.path.normpath(new_folder)
            
            success = self.downloader.change_download_folder(new_folder)
            if success:
                print(f"{Fore.GREEN}Đã thay đổi thư mục lưu thành: {new_folder}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Không thể thay đổi thư mục lưu.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Hủy thay đổi thư mục.{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Nhấn Enter để tiếp tục...{Style.RESET_ALL}")
    
    def settings_menu(self):
        """Menu cài đặt ứng dụng"""
        self.show_header()
        print(f"{Fore.CYAN}═══ CÀI ĐẶT ỨNG DỤNG ════{Style.RESET_ALL}")
        
        config = self.downloader.config
        
        print(f"1. Tự động cập nhật: {Fore.GREEN if config.get_setting('auto_update') else Fore.RED}{config.get_setting('auto_update')}{Style.RESET_ALL}")
        print(f"2. Lưu lịch sử tải: {Fore.GREEN if config.get_setting('save_history') else Fore.RED}{config.get_setting('save_history')}{Style.RESET_ALL}")
        print(f"3. Số lượng lịch sử tối đa: {Fore.CYAN}{config.get_setting('max_history_items')}{Style.RESET_ALL}")
        print(f"4. Giao diện: {Fore.CYAN}{config.get_setting('theme')}{Style.RESET_ALL}")
        print(f"5. Quay lại")
        
        choice = input(f"{Fore.YELLOW}Chọn cài đặt để thay đổi (1-5): {Style.RESET_ALL}")
        
        if choice == '1':
            current = config.get_setting('auto_update')
            new_value = not current
            config.set_setting('auto_update', new_value)
            print(f"{Fore.GREEN}Đã thay đổi 'Tự động cập nhật' thành: {new_value}{Style.RESET_ALL}")
            
        elif choice == '2':
            current = config.get_setting('save_history')
            new_value = not current
            config.set_setting('save_history', new_value)
            print(f"{Fore.GREEN}Đã thay đổi 'Lưu lịch sử tải' thành: {new_value}{Style.RESET_ALL}")
            
        elif choice == '3':
            try:
                current = config.get_setting('max_history_items')
                new_value = int(input(f"{Fore.YELLOW}Nhập số lượng lịch sử tối đa mới: {Style.RESET_ALL}"))
                if new_value < 10:
                    print(f"{Fore.RED}Giá trị tối thiểu là 10.{Style.RESET_ALL}")
                    new_value = 10
                config.set_setting('max_history_items', new_value)
                print(f"{Fore.GREEN}Đã thay đổi 'Số lượng lịch sử tối đa' thành: {new_value}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Giá trị không hợp lệ. Giữ nguyên giá trị cũ.{Style.RESET_ALL}")
                
        elif choice == '4':
            current = config.get_setting('theme')
            new_value = 'light' if current == 'dark' else 'dark'
            config.set_setting('theme', new_value)
            print(f"{Fore.GREEN}Đã thay đổi 'Giao diện' thành: {new_value}{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Nhấn Enter để tiếp tục...{Style.RESET_ALL}")
    
    def about_menu(self):
        """Menu thông tin ứng dụng"""
        self.show_header()
        print(f"{Fore.CYAN}═══ THÔNG TIN ỨNG DỤNG ════{Style.RESET_ALL}")
        
        app_info = self.downloader.config.get_app_info()
        
        print(f"{Fore.YELLOW}Phiên bản:{Style.RESET_ALL} {app_info['version']}")
        print(f"{Fore.YELLOW}Cập nhật:{Style.RESET_ALL} {app_info['last_updated']}")
        print(f"{Fore.YELLOW}Tác giả:{Style.RESET_ALL} {app_info['author']}")
        print(f"{Fore.YELLOW}Người dùng hiện tại:{Style.RESET_ALL} {app_info['current_user']}")
        print(f"{Fore.YELLOW}Hệ điều hành:{Style.RESET_ALL} {platform.system()} {platform.version()}")
        print(f"{Fore.YELLOW}Python:{Style.RESET_ALL} {platform.python_version()}")
        
        print(f"\n{Fore.CYAN}TikTok Downloader là công cụ tải video TikTok không có logo,")
        print(f"giúp người dùng lưu trữ video với chất lượng cao nhất.")
        print(f"Ứng dụng được phát triển chỉ với mục đích học tập.{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Nhấn Enter để tiếp tục...{Style.RESET_ALL}")
    
    def run(self):
        """Chạy giao diện dòng lệnh"""
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.download_video_menu()
            elif choice == '2':
                self.show_history_menu()
            elif choice == '3':
                self.change_folder_menu()
            elif choice == '4':
                self.settings_menu()
            elif choice == '5':
                self.about_menu()
            elif choice == '6':
                self.show_header()
                print(f"{Fore.CYAN}Cảm ơn bạn đã sử dụng ứng dụng!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Thời gian: {datetime.now().strftime('%H:%M:%S %d-%m-%Y')}{Style.RESET_ALL}")
                sys.exit(0)

def run_cli():
    cli = TikTokDownloaderCLI()
    cli.run()

if __name__ == "__main__":
    run_cli()