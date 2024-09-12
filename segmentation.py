import re
import os

def split_text(long_text, num_parts=10):
    # 使用原始字符串来避免 Unicode 转义问题
    long_text = r"{}".format(long_text)

    # 按段落分割文本，同时保留公式
    paragraphs = re.split(r'\n\s*\n', long_text.strip())

    # 计算每部分的目标长度
    total_length = sum(len(p) for p in paragraphs)
    target_length = total_length // num_parts

    result = []
    current_part = ""
    current_length = 0

    for paragraph in paragraphs:
        if current_length + len(paragraph) > target_length and len(result) < num_parts - 1:
            result.append(current_part.strip())
            current_part = ""
            current_length = 0

        current_part += paragraph + "\n\n"
        current_length += len(paragraph)

    # 添加最后一部分
    if current_part:
        result.append(current_part.strip())

    # 如果分割的部分少于要求的数量，将最后一部分继续分割
    while len(result) < num_parts:
        longest_part = max(result, key=len)
        index = result.index(longest_part)

        # 尝试在句子边界分割，同时保护公式
        sentences = re.split(r'(?<=[.!?])\s+(?![^$]*\$)', longest_part)
        mid = len(sentences) // 2

        result[index] = ' '.join(sentences[:mid])
        result.insert(index + 1, ' '.join(sentences[mid:]))
    return result

def split_text_download(long_text, path, num_parts=10):
    # 使用原始字符串来避免 Unicode 转义问题
    long_text = r"{}".format(long_text)

    # 按段落分割文本，同时保留公式
    paragraphs = re.split(r'\n\s*\n', long_text.strip())

    # 计算每部分的目标长度
    total_length = sum(len(p) for p in paragraphs)
    target_length = total_length // num_parts

    result = []
    current_part = ""
    current_length = 0

    for paragraph in paragraphs:
        if current_length + len(paragraph) > target_length and len(result) < num_parts - 1:
            result.append(current_part.strip())
            current_part = ""
            current_length = 0

        current_part += paragraph + "\n\n"
        current_length += len(paragraph)

    # 添加最后一部分
    if current_part:
        result.append(current_part.strip())

    # 如果分割的部分少于要求的数量，将最后一部分继续分割
    while len(result) < num_parts:
        longest_part = max(result, key=len)
        index = result.index(longest_part)

        # 尝试在句子边界分割，同时保护公式
        sentences = re.split(r'(?<=[.!?])\s+(?![^$]*\$)', longest_part)
        mid = len(sentences) // 2

        result[index] = ' '.join(sentences[:mid])
        result.insert(index + 1, ' '.join(sentences[mid:]))
    file_path = path.split('.md')[0]
    # 新建文件夹

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for i, part in enumerate(result, 1):
        with open(f"{file_path}/part_{i}.md", "w", encoding='utf-8') as f:
            f.write(part)
    return result
# split_parts = split_text(test_text, 3) #
# for i, part in enumerate(split_parts, 1):
#     print(f"Part {i}:")
#     print(part)
#     print("-" * 40)