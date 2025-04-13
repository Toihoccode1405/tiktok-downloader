import sys
from .cli import run_cli

if __name__ == "__main__":
    if "--gui" in sys.argv:
        try:
            from .gui import main
            main()
        except ImportError:
            print("Không thể tải giao diện đồ họa. Vui lòng cài đặt PyQt5 bằng lệnh: pip install PyQt5")
            sys.exit(1)
    else:
        run_cli()