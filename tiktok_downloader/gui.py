import sys
import os
import threading
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QProgressBar, QComboBox, QTabWidget,
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QFileDialog, QMessageBox, QSystemTrayIcon, 
                             QAction, QMenu, QStatusBar, QToolBar,QDialog,QProgressDialog)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize, QUrl

# Thêm hàm này thay thế cho các phương pháp tìm kiếm hiện tại
# Sửa hàm find_downloaded_file để thêm output debug
def find_downloaded_file(video_id, downloads_dir):
    """Tìm file tải xuống dựa trên video_id"""
    import glob
    import os
    import time
    
    print(f"Tìm kiếm video_id: {video_id} trong: {downloads_dir}")
    
    # Tìm kiếm file chứa video_id
    matching_files = glob.glob(os.path.join(downloads_dir, f"*{video_id}*.mp4"))
    
    if matching_files:
        # Tìm thấy file chứa video_id
        file_path = matching_files[0]
        file_size = os.path.getsize(file_path)
        print(f"Tìm thấy file theo video_id: {file_path}, kích thước: {file_size} bytes")
        return file_path, file_size
    
    # Tìm kiếm thêm trong thư mục TikTok nếu có
    tiktok_dir = os.path.join(downloads_dir, "TikTok")
    if os.path.exists(tiktok_dir):
        matching_files = glob.glob(os.path.join(tiktok_dir, f"*{video_id}*.mp4"))
        if matching_files:
            file_path = matching_files[0]
            file_size = os.path.getsize(file_path)
            print(f"Tìm thấy file trong thư mục TikTok: {file_path}, kích thước: {file_size} bytes")
            return file_path, file_size
    
    # Phương pháp 2: Lấy file mp4 mới nhất trong thư mục
    all_mp4_files = glob.glob(os.path.join(downloads_dir, "*.mp4"))
    all_mp4_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # Liệt kê 3 file mới nhất để debug
    print("3 file mp4 mới nhất:")
    for i, file_path in enumerate(all_mp4_files[:3]):
        if i >= 3:
            break
        print(f"{i+1}. {os.path.basename(file_path)} - {os.path.getsize(file_path)} bytes - {os.path.getmtime(file_path)}")
    
    # Lấy file tạo trong vòng 10 giây qua
    current_time = time.time()
    recent_files = [f for f in all_mp4_files if os.path.getmtime(f) > (current_time - 10)]
    
    if recent_files:
        file_path = recent_files[0]
        file_size = os.path.getsize(file_path)
        print(f"Tìm thấy file mới nhất (trong 10s): {file_path}, kích thước: {file_size} bytes")
        return file_path, file_size
    
    # Nếu không có file nào được tạo trong 10 giây qua nhưng có các file mp4
    if all_mp4_files:
        file_path = all_mp4_files[0]
        file_size = os.path.getsize(file_path)
        print(f"Tìm thấy file mp4 mới nhất: {file_path}, kích thước: {file_size} bytes")
        return file_path, file_size
    
    # Không tìm thấy file
    print("Không tìm thấy file nào!")
    return None, 0

# Đảm bảo có thể import các module cần thiết
try:
    from .downloader import TikTokDownloader
    from .updater import Updater
except ImportError:
    # Fallback nếu không import được từ package
    try:
        from downloader import TikTokDownloader
        from updater import Updater
    except ImportError:
        # Tạo class giả cho việc kiểm thử
        class TikTokDownloader:
            def __init__(self):
                self.download_history = [
            {
                "video_id": "7123456789012345678",
                "timestamp": "2025-04-13 15:42:30",
                "status": "success",
                "quality": "high", 
                "size": 15728640,
                "file_path": "/downloads/TikTok_7123456789012345678.mp4",
                "url": "https://www.tiktok.com/@username/video/7123456789012345678"
            },
            {
                "video_id": "7098765432109876543",
                "timestamp": "2025-04-13 14:30:15",
                "status": "success",
                "quality": "medium",
                "size": 7340032,
                "file_path": "/downloads/TikTok_7098765432109876543.mp4",
                "url": "https://www.tiktok.com/@other_user/video/7098765432109876543"
            },
            {
                "video_id": "7112233445566778899",
                "timestamp": "2025-04-12 22:15:10",
                "status": "fail",
                "quality": "high",
                "size": 0,
                "file_path": "",
                "url": "https://www.tiktok.com/@invalid_user/video/7112233445566778899"
            }
        ]
            
            def download_video(self, url, quality):
                return True
                
            def show_history(self):
                pass
                
            def save_history(self):
                """Giả lập lưu lịch sử, trong thực tế sẽ lưu vào file"""
                # Không cần làm gì vì chúng ta đang sử dụng lịch sử trong bộ nhớ
                pass
                
            def export_history(self, format_type, file_path=None):
                return True
                
        class Updater:
            def __init__(self):
                self.current_version = "1.2.2"
                
            def check_for_updates(self):
                """Kiểm tra cập nhật"""
                # Hiển thị thông báo đang kiểm tra
                self.version_label.setText(f"Phiên bản: {self.updater.current_version} (Đang kiểm tra...)")
                
                # Thực hiện kiểm tra
                has_update, latest_version = self.updater.check_for_updates()
                
                if has_update:
                    self.version_label.setText(f"Phiên bản: {self.updater.current_version} (Có bản mới: {latest_version})")
                    reply = QMessageBox.question(self, "Có phiên bản mới", 
                                                f"Phiên bản mới {latest_version} đã sẵn sàng!\nBạn có muốn cập nhật ngay không?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        # Hiển thị dialog tiến trình cập nhật
                        progress_dialog = QProgressDialog("Đang cập nhật...", "Hủy", 0, 100, self)
                        progress_dialog.setWindowTitle("Cập nhật")
                        progress_dialog.setWindowModality(Qt.WindowModal)
                        progress_dialog.setAutoClose(True)
                        progress_dialog.setValue(0)
                        
                        # Giả lập tiến trình cập nhật
                        for i in range(101):
                            progress_dialog.setValue(i)
                            QApplication.processEvents()
                            time.sleep(0.05)
                            if progress_dialog.wasCanceled():
                                break
                        
                        success = self.updater.perform_update()
                        if success:
                            QMessageBox.information(self, "Cập nhật thành công", 
                                                "Đã cập nhật lên phiên bản mới. Vui lòng khởi động lại ứng dụng!")
                        else:
                            QMessageBox.critical(self, "Lỗi cập nhật", 
                                                "Không thể cập nhật. Vui lòng thử lại sau!")
                else:
                    self.version_label.setText(f"Phiên bản: {self.updater.current_version} (Mới nhất)")
                    QMessageBox.information(self, "Không có cập nhật", 
                                        "Bạn đang sử dụng phiên bản mới nhất!")
                            
            def perform_update(self):
                return True

# Hàm trợ giúp để lấy đường dẫn đến tài nguyên
def get_resource_path(relative_path):
    """Lấy đường dẫn đến file tài nguyên, hỗ trợ cả khi chạy từ bundle"""
    try:
        # PyInstaller tạo thư mục tạm cho resources
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class DownloadThread(QThread):
    """Thread riêng để tải video tránh treo giao diện"""
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str) # success, file_path
    
    def __init__(self, downloader, url, quality):
        super().__init__()
        self.downloader = downloader
        self.url = url
        self.quality = quality
    
    # Sửa trong class DownloadThread - phương thức run()
    def run(self):
        self.status_signal.emit("Đang xử lý URL...")
        self.progress_signal.emit(10)
        
        self.progress_signal.emit(30)
        self.status_signal.emit("Đang tải video...")
        
        try:
            success = self.downloader.download_video(self.url, self.quality)
            self.progress_signal.emit(100)
            
            if success:
                import datetime
                import re
                import time
                
                # Extract video_id từ URL
                video_id = re.search(r'video/(\d+)', self.url)
                video_id = video_id.group(1) if video_id else str(int(datetime.datetime.now().timestamp()))
                
                # Đợi một chút để đảm bảo file được lưu hoàn tất
                time.sleep(1)
                
                # Tìm file đã tải xuống
                downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                file_path, file_size = find_downloaded_file(video_id, downloads_dir)
                
                # Nếu không tìm thấy, sử dụng giá trị mặc định
                # Trong hàm run() của lớp DownloadThread
                if not file_path:
                    # Không tìm thấy file, lấy đường dẫn mặc định (không dùng wildcard)
                    file_path = os.path.join(downloads_dir, f"{video_id}.mp4")
                    file_size = 0  # Đặt kích thước là 0 nếu không tìm thấy file
                    
                    # Thử lại sau 1 giây nữa
                    time.sleep(1)
                    second_try_path, second_try_size = find_downloaded_file(video_id, downloads_dir)
                    if second_try_path:
                        file_path = second_try_path
                        file_size = second_try_size
                
                # Thêm vào lịch sử
                self.downloader.download_history.insert(0, {
                    "video_id": video_id,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "success",
                    "quality": self.quality,
                    "size": file_size,
                    "file_path": file_path,
                    "url": self.url
                })
                
                self.status_signal.emit("Tải xuống thành công!")
                self.finished_signal.emit(True, file_path)
            else:
                self.status_signal.emit("Tải xuống thất bại!")
                self.finished_signal.emit(False, "")
        except Exception as e:
            self.status_signal.emit(f"Lỗi: {str(e)}")
            self.finished_signal.emit(False, "")

class BatchDownloadThread(QThread):
    """Thread riêng để tải nhiều video cùng lúc"""
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)
    video_progress_signal = pyqtSignal(int, int, bool)  # index, progress, success
    finished_signal = pyqtSignal(int, int)  # success_count, fail_count
    
    def __init__(self, downloader, urls, quality):
        super().__init__()
        self.downloader = downloader
        self.urls = urls
        self.quality = quality
        self.is_running = True
    
    # Trong class BatchDownloadThread - phương thức run():
    def run(self):
        success_count = 0
        fail_count = 0
        
        total_urls = len(self.urls)
        
        for i, url in enumerate(self.urls):
            if not self.is_running:
                break
                
            self.status_signal.emit(f"Đang tải video {i+1}/{total_urls}")
            self.progress_signal.emit(int((i / total_urls) * 100))
            
            # Báo hiệu đang bắt đầu xử lý video
            self.video_progress_signal.emit(i, 10, False)
            
            # Tải video
            try:
                # Cập nhật tiến trình để cải thiện trải nghiệm
                self.video_progress_signal.emit(i, 30, False)
                
                success = self.downloader.download_video(url, self.quality)
                
                # Cập nhật tiến trình khi tải xong
                self.video_progress_signal.emit(i, 90, False)
                
                if success:
                    import datetime
                    import re
                    import time
                    
                    # Extract video_id từ URL
                    video_id = re.search(r'video/(\d+)', url)
                    video_id = video_id.group(1) if video_id else str(int(datetime.datetime.now().timestamp()))
                    
                    # Đợi một chút để đảm bảo file được lưu hoàn tất
                    time.sleep(1)
                    
                    # Tìm file đã tải xuống
                    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                    file_path, file_size = find_downloaded_file(video_id, downloads_dir)
                    
                    # Nếu không tìm thấy, sử dụng giá trị mặc định
                    # Trong hàm run() của lớp BatchDownloadThread
                    if not file_path:
                        # Không tìm thấy file, lấy đường dẫn mặc định (không dùng wildcard)
                        file_path = os.path.join(downloads_dir, f"{video_id}.mp4")
                        file_size = 0  # Đặt kích thước là 0 nếu không tìm thấy file
                        
                        # Thử lại sau 1 giây nữa
                        time.sleep(1)
                        second_try_path, second_try_size = find_downloaded_file(video_id, downloads_dir)
                        if second_try_path:
                            file_path = second_try_path
                            file_size = second_try_size
                    
                    # Thêm vào lịch sử
                    self.downloader.download_history.insert(0, {
                        "video_id": video_id,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "success",
                        "quality": self.quality,
                        "size": file_size,
                        "file_path": file_path,
                        "url": url
                    })
                    
                    success_count += 1
                    self.video_progress_signal.emit(i, 100, True)
                else:
                    fail_count += 1
                    self.video_progress_signal.emit(i, 100, False)
            except Exception as e:
                fail_count += 1
                self.status_signal.emit(f"Lỗi: {str(e)}")
                self.video_progress_signal.emit(i, 100, False)
            
            # Delay để cập nhật giao diện - giảm xuống để tránh đợi quá lâu
            self.msleep(200)
            
            # Đảm bảo ứng dụng có thời gian xử lý các sự kiện UI
            QApplication.processEvents()

        self.progress_signal.emit(100)
        self.status_signal.emit(f"Hoàn tất: {success_count} thành công, {fail_count} thất bại")
        self.finished_signal.emit(success_count, fail_count)
    
    def stop(self):
        """Dừng quá trình tải xuống"""
        self.is_running = False

    

class TikTokDownloaderApp(QMainWindow):
    """Ứng dụng TikTok Downloader với giao diện PyQt5"""
    
    def __init__(self):
        super().__init__()
        self.downloader = TikTokDownloader()
        self.updater = Updater()
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo giao diện người dùng"""
        self.setWindowTitle("TikTok Video Downloader")
        self.setGeometry(100, 100, 900, 600)
        
        # Tìm icon hoặc dùng icon mặc định
        try:
            icon_path = get_resource_path("resources/icons/app_icon.png")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except:
            # Bỏ qua nếu không có icon
            pass
        
        # Thiết lập palette màu chủ đạo
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)
        
        # Tạo tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #353535;
                color: white;
                padding: 10px 15px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: #2196F3;
                color: white;
            }
        """)
        
        # Tạo các tab chính
        self.tab_download = QWidget()
        self.tab_batch = QWidget()
        self.tab_history = QWidget()
        self.tab_settings = QWidget()
        
        # Thêm các tab vào tab widget
        self.tabs.addTab(self.tab_download, "Tải Video")
        self.tabs.addTab(self.tab_batch, "Tải Nhiều Video")
        self.tabs.addTab(self.tab_history, "Lịch Sử")
        self.tabs.addTab(self.tab_settings, "Cài Đặt")
        
        # Setup các tab
        self.setup_download_tab()
        self.setup_batch_tab()
        self.setup_history_tab()
        self.setup_settings_tab()
        
        # Thanh trạng thái
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(f"Sẵn sàng tải video | Phiên bản: {self.updater.current_version}")
        
        # Widget chính
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)
        
        self.setCentralWidget(central_widget)
        
    def setup_download_tab(self):
        """Thiết lập tab tải video đơn lẻ"""
        layout = QVBoxLayout()
        
        # Logo TikTok (nếu không có file thì hiển thị text)
        logo_label = QLabel("TikTok Downloader")
        logo_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        logo_label.setFont(font)
        layout.addWidget(logo_label)
        
        # URL input
        url_layout = QHBoxLayout()
        url_label = QLabel("URL Video:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Nhập URL video TikTok...")
        self.paste_btn = QPushButton("Dán")
        self.paste_btn.clicked.connect(self.paste_url)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.paste_btn)
        layout.addLayout(url_layout)
        
        # Chất lượng video
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Chất lượng:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItem("Cao (HD)", "high")
        self.quality_combo.addItem("Trung bình", "medium")
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        layout.addLayout(quality_layout)
        
        # Thư mục lưu
        save_layout = QHBoxLayout()
        save_label = QLabel("Lưu tại:")
        self.save_path = QLineEdit()
        self.save_path.setReadOnly(True)
        self.save_path.setText(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.browse_btn = QPushButton("Duyệt...")
        self.browse_btn.clicked.connect(self.browse_folder)
        save_layout.addWidget(save_label)
        save_layout.addWidget(self.save_path)
        save_layout.addWidget(self.browse_btn)
        layout.addLayout(save_layout)
        
        # Thanh tiến trình
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Trạng thái tải xuống
        self.status_label = QLabel("Sẵn sàng tải xuống")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Nút tải xuống
        self.download_btn = QPushButton("Tải Video")
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #0b7dda;
            }
            
            QPushButton:pressed {
                background-color: #0a6fc2;
            }
        """)
        self.download_btn.clicked.connect(self.download_video)
        layout.addWidget(self.download_btn)
        
        # Thêm spacing
        layout.addStretch()
        
        self.tab_download.setLayout(layout)
    
    def setup_batch_tab(self):
        """Thiết lập tab tải nhiều video"""
        layout = QVBoxLayout()
        
        # Tiêu đề
        title = QLabel("Tải Nhiều Video Cùng Lúc")
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        title.setFont(font)
        layout.addWidget(title)
        
        # Hướng dẫn
        instruction = QLabel("Nhập mỗi URL trên một dòng:")
        layout.addWidget(instruction)
        
        # Ô nhập nhiều URL
        self.batch_urls = QTextEdit()
        self.batch_urls.setPlaceholderText("https://www.tiktok.com/@username/video/1234567890\nhttps://www.tiktok.com/@username/video/9876543210\n...")
        layout.addWidget(self.batch_urls)
        
        # Chất lượng video
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Chất lượng:")
        self.batch_quality_combo = QComboBox()
        self.batch_quality_combo.addItem("Cao (HD)", "high")
        self.batch_quality_combo.addItem("Trung bình", "medium")
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.batch_quality_combo)
        quality_layout.addStretch()
        layout.addLayout(quality_layout)
        
        # Thanh tiến trình
        self.batch_progress = QProgressBar()
        self.batch_progress.setRange(0, 100)
        self.batch_progress.setValue(0)
        layout.addWidget(self.batch_progress)
        
        # Trạng thái
        self.batch_status = QLabel("Sẵn sàng")
        self.batch_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.batch_status)
        
        # Nút tải xuống hàng loạt
        self.batch_download_btn = QPushButton("Bắt Đầu Tải")
        self.batch_download_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.batch_download_btn.clicked.connect(self.batch_download)
        layout.addWidget(self.batch_download_btn)
        
        layout.addStretch()
        
        self.tab_batch.setLayout(layout)
    
    def setup_history_tab(self):
        """Thiết lập tab lịch sử tải xuống"""
        layout = QVBoxLayout()
        
        # Bảng lịch sử
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Video ID", "Thời gian", "Trạng thái", "Chất lượng", "Kích thước"])
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.history_table)
        
        # Các nút chức năng
        buttons_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Làm mới")
        self.refresh_btn.clicked.connect(self.refresh_history)
        self.clear_history_btn = QPushButton("Xóa lịch sử")
        self.clear_history_btn.clicked.connect(self.clear_history)
        self.export_btn = QPushButton("Xuất lịch sử")
        self.export_btn.clicked.connect(self.export_history)
        
        buttons_layout.addWidget(self.refresh_btn)
        buttons_layout.addWidget(self.clear_history_btn)
        buttons_layout.addWidget(self.export_btn)
        
        layout.addLayout(buttons_layout)
        
        self.tab_history.setLayout(layout)
        
        # Load lịch sử
        self.refresh_history()
    
    def setup_settings_tab(self):
        """Thiết lập tab cài đặt"""
        layout = QVBoxLayout()
        
        # Cài đặt thư mục lưu mặc định
        default_dir_layout = QHBoxLayout()
        default_dir_label = QLabel("Thư mục lưu mặc định:")
        self.default_dir_input = QLineEdit()
        self.default_dir_input.setText(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.default_dir_browse = QPushButton("Duyệt...")
        self.default_dir_browse.clicked.connect(self.browse_default_dir)
        
        default_dir_layout.addWidget(default_dir_label)
        default_dir_layout.addWidget(self.default_dir_input)
        default_dir_layout.addWidget(self.default_dir_browse)
        layout.addLayout(default_dir_layout)
        
        # Tên file mặc định
        filename_layout = QHBoxLayout()
        filename_label = QLabel("Định dạng tên file:")
        self.filename_input = QLineEdit()
        self.filename_input.setText("TikTok_%videoId%")
        filename_hint = QLabel("(%videoId%, %author%, %date%)")
        
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.filename_input)
        filename_layout.addWidget(filename_hint)
        layout.addLayout(filename_layout)
        
        # Bật/tắt thông báo
        notification_layout = QHBoxLayout()
        notification_label = QLabel("Thông báo khi tải xong:")
        self.notification_toggle = QComboBox()
        self.notification_toggle.addItem("Bật")
        self.notification_toggle.addItem("Tắt")
        
        notification_layout.addWidget(notification_label)
        notification_layout.addWidget(self.notification_toggle)
        notification_layout.addStretch()
        layout.addLayout(notification_layout)
        
        # Proxy settings
        proxy_layout = QHBoxLayout()
        proxy_label = QLabel("Proxy (tùy chọn):")
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("http://user:pass@host:port")
        
        proxy_layout.addWidget(proxy_label)
        proxy_layout.addWidget(self.proxy_input)
        layout.addLayout(proxy_layout)
        
        # Kiểm tra cập nhật
        update_layout = QHBoxLayout()
        update_label = QLabel("Kiểm tra cập nhật:")
        self.check_update_btn = QPushButton("Kiểm tra ngay")
        self.check_update_btn.clicked.connect(self.check_for_updates)
        self.version_label = QLabel("Phiên bản: 1.2.2")
        
        update_layout.addWidget(update_label)
        update_layout.addWidget(self.check_update_btn)
        update_layout.addWidget(self.version_label)
        layout.addLayout(update_layout)
        
        # Nút lưu cài đặt
        self.save_settings_btn = QPushButton("Lưu Cài Đặt")
        self.save_settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        self.save_settings_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_settings_btn)
        
        layout.addStretch()
        
        self.tab_settings.setLayout(layout)
    
    def paste_url(self):
        """Dán URL từ clipboard"""
        clipboard = QApplication.clipboard()
        self.url_input.setText(clipboard.text())
    
    def browse_folder(self):
        """Chọn thư mục lưu video"""
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu video")
        if folder:
            self.save_path.setText(folder)
    
    def browse_default_dir(self):
        """Chọn thư mục lưu mặc định"""
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu mặc định")
        if folder:
            self.default_dir_input.setText(folder)
    
    def download_video(self):
        """Tải video từ URL"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập URL video TikTok!")
            return
        
        quality = self.quality_combo.currentData()
        
        self.progress_bar.setValue(0)
        self.status_label.setText("Đang chuẩn bị tải xuống...")
        self.download_btn.setEnabled(False)
        
        # Tạo thread tải xuống
        self.download_thread = DownloadThread(self.downloader, url, quality)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.status_signal.connect(self.update_status)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()
    
    def update_progress(self, value):
        """Cập nhật thanh tiến trình"""
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        """Cập nhật trạng thái"""
        self.status_label.setText(status)
        self.statusBar.showMessage(status)
    
    def download_finished(self, success, file_path):
        """Xử lý khi tải xuống hoàn tất"""
        self.download_btn.setEnabled(True)
        
        if success:
            # Hiển thị thông báo
            QMessageBox.information(self, "Hoàn tất", "Video đã được tải xuống thành công!")
            
            # Lưu lịch sử vào file
            self.downloader.save_history()

            # Làm mới lịch sử
            self.refresh_history()
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể tải xuống video. Vui lòng kiểm tra URL và thử lại!")

    def batch_download(self):
        """Tải nhiều video cùng lúc"""
        urls_text = self.batch_urls.toPlainText().strip()
        if not urls_text:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ít nhất một URL!")
            return
        
        # Tách các URL thành danh sách
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        quality = self.batch_quality_combo.currentData()
        
        # Tạo bảng để hiển thị tiến trình tải xuống
        self.batch_table = QTableWidget()
        self.batch_table.setColumnCount(3)
        self.batch_table.setHorizontalHeaderLabels(["URL", "Tiến trình", "Trạng thái"])
        self.batch_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.batch_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.batch_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # Thêm các URL vào bảng
        for i, url in enumerate(urls):
            self.batch_table.insertRow(i)
            
            # URL (hiển thị ngắn gọn)
            short_url = url if len(url) < 50 else url[:47] + "..."
            self.batch_table.setItem(i, 0, QTableWidgetItem(short_url))
            
            # Thanh tiến trình
            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(0)
            self.batch_table.setCellWidget(i, 1, progress)
            
            # Trạng thái
            self.batch_table.setItem(i, 2, QTableWidgetItem("Đang chờ"))
        
        # Dialog hiển thị tiến trình
        self.batch_dialog = QDialog(self)
        self.batch_dialog.setWindowTitle("Đang tải video")
        self.batch_dialog.resize(600, 400)
        
        dialog_layout = QVBoxLayout()
        
        # Thêm bảng vào dialog
        dialog_layout.addWidget(self.batch_table)
        
        # Thêm thanh tiến trình tổng thể
        self.batch_progress.setValue(0)
        dialog_layout.addWidget(self.batch_progress)
        
        # Thêm trạng thái
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Trạng thái:"))
        status_layout.addWidget(self.batch_status)
        dialog_layout.addLayout(status_layout)
        
        # Thêm nút hủy
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.cancel_batch_download)
        dialog_layout.addWidget(cancel_btn)
        
        self.batch_dialog.setLayout(dialog_layout)
        
        # Tạo thread tải xuống
        self.batch_thread = BatchDownloadThread(self.downloader, urls, quality)
        self.batch_thread.progress_signal.connect(self.batch_progress.setValue)
        self.batch_thread.status_signal.connect(self.batch_status.setText)
        self.batch_thread.video_progress_signal.connect(self.update_video_progress)
        self.batch_thread.finished_signal.connect(self.batch_download_finished)
        
        # Kết nối tín hiệu kết thúc để đóng dialog
        self.batch_thread.finished.connect(self.batch_dialog.accept)
        
        # Bắt đầu tải
        self.batch_thread.start()
        
        # Hiển thị dialog
        self.batch_dialog.exec_()

    def cancel_batch_download(self):
        """Hủy quá trình tải nhiều video"""
        if hasattr(self, 'batch_thread') and self.batch_thread.isRunning():
            reply = QMessageBox.question(self, "Xác nhận hủy", 
                                        "Bạn có chắc chắn muốn hủy quá trình tải xuống?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.batch_thread.stop()
                self.batch_status.setText("Đã hủy quá trình tải xuống")

    def update_video_progress(self, index, progress, success):
        """Cập nhật tiến trình và trạng thái của video trong bảng"""
        # Cập nhật thanh tiến trình
        progress_bar = self.batch_table.cellWidget(index, 1)
        if progress_bar:
            progress_bar.setValue(progress)
        
        # Cập nhật trạng thái
        if progress == 100:
            status = "Thành công" if success else "Thất bại"
            status_color = QColor(0, 170, 0) if success else QColor(200, 0, 0)
            
            status_item = QTableWidgetItem(status)
            status_item.setForeground(status_color)
            self.batch_table.setItem(index, 2, status_item)

    def batch_download_finished(self, success_count, fail_count):
        """Xử lý khi tải xuống hàng loạt hoàn tất"""
        # Đảm bảo thread dừng hoàn toàn
        if hasattr(self, 'batch_thread'):
            if self.batch_thread.isRunning():
                self.batch_thread.quit()
                self.batch_thread.wait()
        
        # Hiển thị thông báo kết quả
        QMessageBox.information(self, "Hoàn tất", 
                            f"Đã tải xuống {success_count + fail_count} video.\n"
                            f"Thành công: {success_count}\n"
                            f"Thất bại: {fail_count}")
        
        # Lưu lịch sử vào file
        self.downloader.save_history()

        # Làm mới lịch sử
        self.refresh_history()
        
    def refresh_history(self):
        """Làm mới danh sách lịch sử"""
        # Xóa danh sách cũ
        self.history_table.setRowCount(0)
        
        # Lấy lịch sử từ downloader
        history = self.downloader.download_history
        
        # Nếu lịch sử trống, hiển thị thông báo
        if not history:
            self.history_table.setRowCount(1)
            empty_msg = QTableWidgetItem("Chưa có video nào được tải xuống")
            # Đặt item ở cột đầu tiên
            self.history_table.setItem(0, 0, empty_msg)
            
            # Span item qua tất cả các cột để hiển thị ở giữa
            self.history_table.setSpan(0, 0, 1, 5)
            return
        
        # Hiển thị dữ liệu thực từ lịch sử
        for i, item in enumerate(history):
            self.history_table.insertRow(i)
            
            video_id = item.get('video_id', 'Unknown')
            time_str = item.get('timestamp', 'Unknown')
            status = 'Thành công' if item.get('status') == 'success' else 'Thất bại'
            quality = item.get('quality', 'Unknown')
            size_bytes = item.get('size', 0)
            
            # Tính kích thước theo GB, MB hoặc KB tùy thuộc vào độ lớn
            if size_bytes > 1024 * 1024 * 1024:
                size = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
            elif size_bytes > 1024 * 1024:
                size = f"{size_bytes / (1024 * 1024):.2f} MB"
            elif size_bytes > 1024:
                size = f"{size_bytes / 1024:.2f} KB"
            else:
                size = f"{size_bytes} Bytes"
            
            self.history_table.setItem(i, 0, QTableWidgetItem(video_id))
            self.history_table.setItem(i, 1, QTableWidgetItem(time_str))
            
            # Đặt màu sắc cho trạng thái
            status_item = QTableWidgetItem(status)
            if item.get('status') == 'success':
                status_item.setForeground(QColor(0, 170, 0))  # Xanh lá
            else:
                status_item.setForeground(QColor(200, 0, 0))  # Đỏ
                
            self.history_table.setItem(i, 2, status_item)
            self.history_table.setItem(i, 3, QTableWidgetItem(quality))
            self.history_table.setItem(i, 4, QTableWidgetItem(size))
            
    def clear_history(self):
        """Xóa lịch sử tải xuống"""
        reply = QMessageBox.question(self, "Xác nhận", 
                                     "Bạn có chắc chắn muốn xóa tất cả lịch sử tải xuống?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Xóa lịch sử
            self.downloader.download_history = []
            self.downloader.save_history()
            self.refresh_history()
            QMessageBox.information(self, "Đã xóa", "Lịch sử tải xuống đã được xóa!")
    
    def export_history(self):
        """Xuất lịch sử ra file"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Xuất lịch sử", "", 
                                                "CSV Files (*.csv);;Text Files (*.txt)", 
                                                options=options)
        if file_name:
            format_type = 'csv' if file_name.endswith('.csv') else 'txt'
            success = self.downloader.export_history(format_type, file_name)
            
            if success:
                QMessageBox.information(self, "Xuất lịch sử", f"Lịch sử đã được xuất ra file {file_name}!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xuất lịch sử!")
    
    def save_settings(self):
        """Lưu các cài đặt"""
        # Đây là nơi bạn sẽ lưu các cài đặt vào file cấu hình
        QMessageBox.information(self, "Cài đặt", "Đã lưu cài đặt thành công!")
    
    def check_for_updates(self):
        """Kiểm tra cập nhật"""
        has_update, latest_version = self.updater.check_for_updates()
        
        if has_update:
            reply = QMessageBox.question(self, "Có phiên bản mới", 
                                        f"Phiên bản mới {latest_version} đã sẵn sàng!\nBạn có muốn cập nhật ngay không?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                success = self.updater.perform_update()
                if success:
                    QMessageBox.information(self, "Cập nhật thành công", 
                                           "Đã cập nhật lên phiên bản mới. Vui lòng khởi động lại ứng dụng!")
                else:
                    QMessageBox.critical(self, "Lỗi cập nhật", 
                                        "Không thể cập nhật. Vui lòng thử lại sau!")
        else:
            self.version_label.setText(f"Phiên bản: {self.updater.current_version} (Mới nhất)")
            QMessageBox.information(self, "Không có cập nhật", 
                                   "Bạn đang sử dụng phiên bản mới nhất!")
    
    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng"""
        # Dừng tất cả các thread đang chạy
        if hasattr(self, 'download_thread') and self.download_thread.isRunning():
            self.download_thread.quit()
            self.download_thread.wait(1000)  # Đợi tối đa 1 giây
        
        if hasattr(self, 'batch_thread') and self.batch_thread.isRunning():
            self.batch_thread.stop()
            self.batch_thread.quit()
            self.batch_thread.wait(1000)
        
        # Chấp nhận đóng cửa sổ
        event.accept()

def main():
    """Hàm chạy chính cho ứng dụng PyQt5"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Phong cách giao diện thống nhất
    
    # Thiết lập stylesheet cho toàn bộ ứng dụng
    app.setStyleSheet("""
        QWidget {
            font-size: 10pt;
        }
        
        QPushButton {
            padding: 5px 10px;
            border-radius: 3px;
        }
        
        QLineEdit, QTextEdit, QComboBox {
            padding: 5px;
            border: 1px solid #555;
            border-radius: 3px;
            background-color: #444;
        }
        
        QProgressBar {
            border: 1px solid #555;
            border-radius: 3px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #2196F3;
        }
        
        QTableWidget {
            gridline-color: #555;
            background-color: #444;
            border: 1px solid #555;
        }
        
        QTableWidget::item {
            padding: 5px;
        }
    """)
    
    window = TikTokDownloaderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()