import subprocess
import sys
import os

def install_dependencies():
    """安装项目所需的依赖包"""
    
    print("开始安装音乐提示词偏好分析系统所需的依赖...")
    
    # 要安装的依赖包列表
    dependencies = [
        'pandas',
        'matplotlib',
        'numpy',
        'nltk',
        'xlsxwriter',
        'openpyxl'  # 用于读写Excel文件
    ]
    
    # 检查pip是否可用
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
    except subprocess.CalledProcessError:
        print("错误: 无法找到pip。请确保pip已正确安装。")
        return False
    
    # 安装依赖
    for package in dependencies:
        print(f"\n正在安装 {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"{package} 安装成功!")
        except subprocess.CalledProcessError:
            print(f"错误: 安装 {package} 失败")
            return False
    
    # 下载NLTK资源
    print("\n正在下载NLTK资源...")
    try:
        import nltk
        nltk.download('words')
        nltk.download('stopwords')
        print("NLTK资源下载成功!")
    except Exception as e:
        print(f"警告: NLTK资源下载失败: {e}")
        print("您可以稍后再次尝试，或者在运行主程序时系统会自动下载。")
    
    print("\n所有依赖安装完成!")
    return True

if __name__ == "__main__":
    install_dependencies() 