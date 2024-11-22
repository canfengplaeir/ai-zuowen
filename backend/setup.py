import os

def setup_project():
    # 获取项目根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建必要的目录
    directories = [
        os.path.join(base_dir, 'database'),
        os.path.join(base_dir, 'uploads'),
        os.path.join(base_dir, 'logs')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

if __name__ == '__main__':
    setup_project() 