from zhipuai import ZhipuAI
from typing import Optional, Union
import base64

class GLM4VFlash:
    def __init__(self, api_key: str):
        """
        初始化 GLM4V-Flash 客户端
        
        Args:
            api_key (str): 智谱 AI 的 API key
        """
        self.client = ZhipuAI(api_key=api_key)
        self.model = "glm-4v-flash"

    def prompt(
        self, 
        image_path_or_url: str, 
        prompt: str, 
        temperature: float = 0.8, 
        is_url: bool = False
    ) -> str:
        """
        对图片进行提问并获取回答
        
        Args:
            image_path_or_url (str): 图片的本地路径或URL
            prompt (str): 关于图片的提问
            is_url (bool): 是否为URL链接，默认为False（即本地文件）
        
        Returns:
            str: 模型的回答
        """
        try:
            # 准备图片数据
            if is_url:
                image_data = {"url": image_path_or_url}
            else:
                # 读取本地图片并转换为base64
                with open(image_path_or_url, 'rb') as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                image_data = {"url": img_base64}

            # 构建请求消息
            messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": image_data
                    },
                    {
                        "type": "text",
                        "text": prompt
                    },
                ],
                "temperature": temperature
            }]

            # 发送请求
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            # 返回结果
            return response.choices[0].message.content

        except Exception as e:
            return f"错误：{str(e)}" 

class GLM4VPlus:
    def __init__(self, api_key: str):
        """
        初始化 GLM4V-Plus 客户端
        
        Args:
            api_key (str): 智谱 AI 的 API key
        """
        self.client = ZhipuAI(api_key=api_key)
        self.model = "glm-4v-plus"

    def prompt(
        self, 
        image_path_or_url: str, 
        prompt: str, 
        temperature: float = 0.8, 
        is_url: bool = False
    ) -> str:
        """
        对图片进行提问并获取回答
        
        Args:
            image_path_or_url (str): 图片的本地路径或URL
            prompt (str): 关于图片的提问
            is_url (bool): 是否为URL链接，默认为False（即本地文件）
        
        Returns:
            str: 模型的回答
        """
        try:
            # 准备图片数据
            if is_url:
                image_data = {"url": image_path_or_url}
            else:
                # 读取本地图片并转换为base64
                with open(image_path_or_url, 'rb') as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                image_data = {"url": img_base64}

            # 构建请求消息
            messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": image_data
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
                'temperature': temperature
            }]

            # 发送请求
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            # 返回结果
            return response.choices[0].message.content

        except Exception as e:
            return f"错误：{str(e)}" 

class GLM4VPlus0111:
    def __init__(self, api_key: str):
        """
        初始化 GLM4V-Plus 客户端
        
        Args:
            api_key (str): 智谱 AI 的 API key
        """
        self.client = ZhipuAI(api_key=api_key)
        self.model = "glm-4v-plus-0111"

    def prompt(
        self, 
        image_path_or_url: str, 
        prompt: str, 
        temperature: float = 0.8, 
        is_url: bool = False
    ) -> str:
        """
        对图片进行提问并获取回答
        
        Args:
            image_path_or_url (str): 图片的本地路径或URL
            prompt (str): 关于图片的提问
            is_url (bool): 是否为URL链接，默认为False（即本地文件）
        
        Returns:
            str: 模型的回答
        """
        try:
            # 准备图片数据
            if is_url:
                image_data = {"url": image_path_or_url}
            else:
                # 读取本地图片并转换为base64
                with open(image_path_or_url, 'rb') as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                image_data = {"url": img_base64}

            # 构建请求消息
            messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": image_data
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
                'temperature': temperature
            }]

            # 发送请求
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            # 返回结果
            return response.choices[0].message.content

        except Exception as e:
            return f"错误：{str(e)}" 
