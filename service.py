from filename_add import add_suffix_to_filename
from read_md import read_md_file, save_md_file
from segmentation import split_text
from translation import translate_text
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
async def translate_segment(executor, segment):
    """Asynchronous wrapper for translate_text function."""
    return await asyncio.get_event_loop().run_in_executor(executor, translate_text, segment)

async def process_and_translate_md(input_filename, max_workers=5):
    """
    读取Markdown文件,分割文本,并发翻译内容,然后保存结果。

    输入:
    - input_filename (str): 输入的Markdown文件名
    - max_workers (int): 并发翻译的最大工作线程数，默认为5

    输出:
    - 无返回值,但会将翻译后的内容保存到指定的输出文件中
    """
    output_filename = add_suffix_to_filename(input_filename)
    # 步骤1: 读取Markdown文件
    content = read_md_file(input_filename)

    # 步骤2: 分割文本
    segments = split_text(content,num_parts=200)

    # # 步骤3: 并发翻译每个文本片段
    executor = ThreadPoolExecutor(max_workers=max_workers)
    tasks = [translate_segment(executor, segment) for segment in segments]
    translated_segments = await asyncio.gather(*tasks)

    # 步骤4: 将翻译后的片段重新组合成一个字符串
    translated_content = '\n\n'.join(translated_segments)

    # 步骤5: 保存翻译后的内容到新的Markdown文件
    save_md_file(output_filename, translated_content)

    print(f"翻译完成。结果已保存到: {output_filename}")


async def process_and_translate_md_down_part(input_filename, max_workers=5, start_page=1, end_page=None, split_doc=True,
                                             translate=True):
    """
    读取Markdown文件,分割文本,可选择性地翻译内容,然后保存结果。

    输入:
    - input_filename (str): 输入的Markdown文件名
    - max_workers (int): 并发翻译的最大工作线程数，默认为5
    - start_page (int): 开始翻译的页数，默认为1。如果为-1，则不进行翻译
    - end_page (int): 结束翻译的页数，默认为None（翻译到最后）。如果为-1，则不进行翻译
    - split_doc (bool): 是否分割文档，默认为True
    - translate (bool): 是否进行翻译，默认为True

    输出:
    - 无返回值,但会将处理后的内容保存到指定的输出文件中
    """
    output_filename = add_suffix_to_filename(input_filename)
    # 步骤1: 读取Markdown文件
    content = read_md_file(input_filename)

    # 步骤2: 分割文本（如果需要）
    if split_doc:
        segments = split_text(content, num_parts=10)
        download_part(input_filename, segments, "split")
    else:
        segments = [content]

    # 检查是否需要翻译
    should_translate = translate and start_page != -1 and end_page != -1

    if should_translate:
        # 选择要翻译的页面范围
        if end_page is None:
            end_page = len(segments)
        segments_to_translate = segments[start_page - 1:end_page]

        # 步骤3: 并发翻译选定的文本片段
        executor = ThreadPoolExecutor(max_workers=max_workers)
        tasks = [translate_segment(executor, segment) for segment in segments_to_translate]
        translated_segments = await asyncio.gather(*tasks)

        # 步骤4: 将翻译后的片段重新组合成一个字符串
        translated_content = '\n\n'.join(translated_segments)

        # 步骤5: 保存翻译后的内容到新的Markdown文件
        save_md_file(output_filename, translated_content)

        # 步骤6: 保存翻译后的分段内容
        download_part(input_filename, translated_segments, "translated")

        print(f"翻译完成。结果已保存到: {output_filename}")
    else:
        if split_doc:
            print(f"文档已分割。分割后的文件保存在split目录中。")
        else:
            print(f"文档未进行分割或翻译。")


# 使用示例

def download_part(input_filename, segments, key_word):
    """
    保存分割或翻译后的多个文本文件。

    输入:
    - input_filename (str): 输入的Markdown文件名
    - segments (list): 分割或翻译后的文本片段列表
    - key_word (str): 关键字符，用于确定保存路径

    输出:
    - 无返回值,但会将内容保存到指定的输出文件中
    """
    # 构建保存路径
    base_dir = os.path.dirname(input_filename)
    file_name = os.path.splitext(os.path.basename(input_filename))[0]
    save_dir = os.path.join(base_dir, file_name, key_word)

    # 确保保存目录存在
    os.makedirs(save_dir, exist_ok=True)

    # 保存每个片段到单独的文件
    for i, segment in enumerate(segments, 1):
        output_file = os.path.join(save_dir, f"part_{i}.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(segment)

    print(f"{key_word.capitalize()}后的文件已保存到: {save_dir}")

# 使用示例
async def main():
    input_filename = ""
    await process_and_translate_md_down_part(input_filename, max_workers=5)

if __name__ == "__main__":
    asyncio.run(main())

# async def main():
#     input_filename = "data/Toward.md"
#
#     # 示例1：分割文档但不翻译
#     await process_and_translate_md_down_part(input_filename, split_doc=True, translate=False)
#
#     # 示例2：分割文档并翻译第1-10页
#     await process_and_translate_md_down_part(input_filename, start_page=1, end_page=10)
#
#     # 示例3：分割文档但不翻译（使用-1作为start_page）
#     await process_and_translate_md_down_part(input_filename, start_page=-1)

#    # 示例4：翻译全部
#     await process_and_translate_md(input_filename, max_workers=5)

# # 使用示例
# if __name__ == "__main__":
#     input_file = "data/Toward.md"
#     asyncio.get_event_loop().run_until_complete(process_and_translate_md(input_file, max_workers=5))