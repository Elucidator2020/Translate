def read_md_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"错误: 文件 '{file_path}' 未找到。"
    except IOError:
        return f"错误: 读取文件 '{file_path}' 时发生IO错误。"
    except Exception as e:
        return f"错误: 读取文件 '{file_path}' 时发生未知错误: {str(e)}"

# 保存为新的md
def save_md_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"文件 '{file_path}' 已保存。"
    except IOError:
        return f"错误: 保存文件 '{file_path}' 时发生IO错误。"
    except Exception as e:
        return f"错误: 保存文件 '{file_path}' 时发生未知错误: {str(e)}"