from setuptools import setup, find_packages

setup(
    name="tiktok-downloader",
    version="1.2.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "tqdm>=4.50.0",
        "colorama>=0.4.4",
        "beautifulsoup4>=4.9.3",
    ],
    entry_points={
        'console_scripts': [
            'tiktok-downloader=tiktok_downloader.cli:run_cli',
        ],
    },
    author="Toihoccode1405code",
    author_email="toihoccode1405@gmail.com",
    description="TikTok video downloader without watermark",
    long_description=open("README.md").read() if hasattr(open, "__call__") and open("README.md", encoding="utf-8") else "",
    long_description_content_type="text/markdown",
    keywords="tiktok, downloader, video, no watermark",
    url="https://github.com/toihoccode1405/tiktok-downloader",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.7",
)