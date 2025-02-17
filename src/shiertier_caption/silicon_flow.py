from typing import Optional, Union, List
import base64
try:
    from .repair_json import try_parse_json_object as repair_json
except:
    from repair_json import try_parse_json_object as repair_json
import json
import time
from openai import OpenAI

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def _image_content(image_path):
    # 如果是jpg
    if image_path.endswith(".jpg") or image_path.endswith(".jpeg"):
        return f"data:image/jpeg;base64,{encode_image(image_path)}"
    # 如果是png
    elif image_path.endswith(".png"):
        return f"data:image/png;base64,{encode_image(image_path)}"
    elif image_path.endswith(".webp"):
        return f"data:image/webp;base64,{encode_image(image_path)}"
    else:
        type = image_path.split(".")[-1]
        return f"data:image/{type};base64,{encode_image(image_path)}"

def image_content(image_path):
    return {
        "type": "image_url",
        "image_url": {
            "url": _image_content(image_path),
            "detail":"high"
        }
    }

class SiliconFlow:
    def __init__(self, api_key: str, model: str = "Qwen/Qwen2-VL-72B-Instruct"):
        """
        初始化 SiliconFlow 客户端

        Args:
            api_key (str): 硅基流动的 API key
            model (str): 模型名称，默认为 "Qwen/QVQ-72B-Preview"
        """
        self.client = OpenAI(
            api_key=api_key, # 从https://cloud.siliconflow.cn/account/ak获取
            base_url="https://api.siliconflow.cn/v1"
        )
        self.api_key = api_key
        self.base_url = "https://api.siliconflow.cn/v1"
        self.model = model

        self.default_prompt = """Your task is to describe every aspect, object, and interaction within this image, such that a blind person could perfectly capture it within their imagination if read aloud. You need to do it multiple times, each one a different "style" of description.
- In the regular/informal styles, use language that's relevant to the subject matter. Never use euphemisms. Describe it like the target audience of the image would (e.g. on an online forum where this image was shared).
- Where relevant, use an information dense writing style - communicate efficiently, don't waffle or excessively speculate or conjecture about the meaning or overly praise. Just describe exactly what you see in the image.
- If the image contains text, be sure to add that to each description where possible. It's important that each description captures as much of the relevant details of the image as possible.
- If the image is censored in any way (e.g. bars, pixellation, etc.), then you MUST mention that in the descriptions.
- Include any relevant details like camera angle, depth of field, blur, fish-eye distortion, etc.
- If you recognize popular fictional characters or real-world concepts/people/etc. then you should be sure to mention them in your descriptions.

Please output in JSON format with the following fields:
{"regular": "regular string","midjoury": [midjoury list],"structural": [structural list],"middle": {type1:{},type2:{},...},"creation": [step list],"deviantart request": "request string"}"""

    def prompt(
        self,
        image_path_or_url: str,
        prompt: str = "",
        is_url: bool = False
    ) -> str:
        """
        对图片进行提问并获取回答

        Args:
            image_path_or_url (str): 图片的本地路径或URL
            prompt (str): 关于图片的提问
            is_url (bool): 是否为URL链接，默认为False（即本地文件）

        Returns:
            dict: 模型的回答
        """
        if not prompt:
            prompt = self.default_prompt

        # 准备图片数据
        if is_url:
            image_data = {"url": image_path_or_url}
        else:
            image_data = image_content(image_path_or_url)
        # 构建请求消息
        messages = [{
            "role": "user",
            "content": [
                image_data,
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }]
        response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=False
            )
        return response.choices[0].message.content

if __name__ == "__main__":
    silicon_flow = SiliconFlow("")
    result = silicon_flow.prompt(
        r"C:\Users\jie\Pictures\patreon.png",
        "用英文给这张图片生成用于训练的caption"
    )
    print(result)
