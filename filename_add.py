from pathlib import Path


def add_suffix_to_filename(filepath, suffix="trans", separator="_"):
    # 将输入路径转换为 Path 对象
    path = Path(filepath)

    # 获取目录和文件名
    directory = path.parent
    filename = path.name

    # 分离文件名和扩展名
    name = path.stem
    ext = path.suffix

    # 构造新的文件名
    new_filename = f"{name}{separator}{suffix}{ext}"

    # 组合新的完整路径
    new_filepath = directory / new_filename

    # 返回字符串形式的路径
    return str(new_filepath)