# LAB:Auto Update
# TEST Site:http://codezpc.github.io/CodeAPI/LB/test.exe

import os
import urllib.request

def download_file():
    # 创建download目录
    download_dir = os.path.join(os.path.dirname(__file__), 'download')
    os.makedirs(download_dir, exist_ok=True)
    
    # 下载URL和目标文件路径
    url = 'http://codezpc.github.io/CodeAPI/LB/test.exe'
    file_path = os.path.join(download_dir, 'test.exe')
    
    try:
        # 下载文件
        print(f"正在从 {url} 下载文件...")
        urllib.request.urlretrieve(url, file_path)
        print(f"文件已成功下载到：{file_path}")
        return True
    except Exception as e:
        print(f"下载失败: {str(e)}")
        return False

if __name__ == "__main__":
    download_file()
