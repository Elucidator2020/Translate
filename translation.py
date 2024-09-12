import openai
from config import API_KEY, PROXY_HTTP, PROXY_HTTPS
import os

# 初始化 OpenAI API
openai.api_key = API_KEY

# 翻译文本

def translate_text(text):
    return translate_text_openai(text)

def initialize_config():
    os.environ['http_proxy'] = PROXY_HTTP
    os.environ['https_proxy'] = PROXY_HTTPS

def translate_text_openai(text):
    initialize_config()
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"翻译文本为中文，保持markdown格式：\n{text}"
            }
        ],
        max_tokens=14000,
    )
    print("------------翻译-------------")
    return response.choices[0].message.content


# 测试翻译功能
if __name__ == "__main__":
    text = r"hello! I am a student.This is $a+b = b+a$"
    print(translate_text(text))