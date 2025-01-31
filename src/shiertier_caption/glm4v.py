from zhipuai import ZhipuAI
from typing import Optional, Union, List
import base64
try:
    from .repair_json import try_parse_json_object as repair_json
except:
    from repair_json import try_parse_json_object as repair_json
import json
import concurrent.futures
import os
from tqdm import tqdm
import time


def convert_str_to_list(input: str) -> list:
    # 将输入字符串转换为列表，列表中的元素是字符串
    result = input.split("\n")
    result = [i.strip() for i in result]
    result_list = []
    for i in result:
        if i:
            result_list.append(i)
    return result_list

class GLM4V:
    def __init__(self, api_key: str, model: str = "glm-4v-plus-0111"):
        """
        初始化 GLM4V-Flash 客户端
        
        Args:
            api_key (str): 智谱 AI 的 API key
            model (str): 模型名称，默认为 "glm-4v-plus-0111"
        """
        self.client = ZhipuAI(api_key=api_key)
        if model not in ["glm-4v-flash", "glm-4v", "glm-4v-plus", "glm-4v-plus-0111"]:
            raise ValueError("model must be one of ['glm-4v-flash', 'glm-4v', 'glm-4v-plus', 'glm-4v-plus-0111']")
        self.model = model  
        self.default_prompt = """Your task is to describe every aspect, object, and interaction within this image, such that a blind person could perfectly capture it within their imagination if read aloud. You need to do it multiple times, each one a different "style" of description.
- In the regular/informal styles, use language that's relevant to the subject matter. Never use euphemisms. Describe it like the target audience of the image would (e.g. on an online forum where this image was shared).
- Where relevant, use an information dense writing style - communicate efficiently, don't waffle or excessively speculate or conjecture about the meaning or overly praise. Just describe exactly what you see in the image.
- If the image contains text, be sure to add that to each description where possible. It's important that each description captures as much of the relevant details of the image as possible.
- If the image is censored in any way (e.g. bars, pixellation, etc.), then you MUST mention that in the descriptions.
- Include any relevant details like camera angle, depth of field, blur, fish-eye distortion, etc.
- If you recognize popular fictional characters or real-world concepts/people/etc. then you should be sure to mention them in your descriptions.

As mentioned above, your response should consist of 5 independent descriptions. Each one should be at least 1 paragraph, and should have a different style/structure to the ones that came before. Each description is independent. The goal is to have several descriptions, each which can stand on its own, fully describing the image. We want to capture the full "distribution" of the ways different people, in different contexts, would describe this image.

### 1. Regular Summary:
[A one-paragraph summary of the image. The paragraph should mention all individual parts/things/characters/etc. If it's NSFW, then be sure to use vulgar NSFW terms. Include the style, camera angle, content, interactions, composition, and more. Consider carefully the exact positions/interactions of objects/characters/etc. such that your description is 100% accurate.]

### 2. Midjourney-Style Summary:
[A summary that has higher concept density by using comma-separated partial sentences instead of proper sentence structure. But you MUST ensure that your phrases are long enough to capture interactions. I.e. "cat chasing mouse" is good, while "mouse, cat, chasing" is bad because there's ambiguity.]

### 3. Full Breakdown:
[A numbered list of up to 10 items that methodically capture every subtle detail, form macro to micro, from abstract to concrete.]

### 4. Structural Summary:
[Use an autistically structured style, which breaks the image down hierarchically, or in some other hyper-structured way. Be creative about how you structure it.]

### 5. Creation/Instructional Summary:
[An explanation of how to create this exact image, via a series of steps.]

### 6. DeviantArt Commission Request
[Write a description as if you're commissioning this *exact* image via someone who is currently taking requests (for photography and/or art) on DA. No intro/greeting/request necessary - just launch right into the description of "what you want" in the end result.]
Here is some potentially useful context for this image. If there are character tags/names in the context, then be sure to reference the character and draw upon your knowledge of them (if you have any) when writing your descriptions. Where relevant, incorporate this context into your descriptions, including the artist name(s), and synonyms/rephrasings of tags to increase descriptive diversity, while maintaining accuracy.
If the name of the artist/characters/etc. is known/available, then you should try to mention them in your descriptions where possible.
Remember, your response should be **VERY LONG** because you need to give lots of styles.
(Also, feel free to make a short comment/exclamation, and also remind yourself of important things before you jump into the task.)

# Output Format
Please strictly follow the format below and output only JSON, do not output Python code or other information, use commas【、】to separate JSON fields:"
{"regular": "regular string","midjoury": [midjoury list],"structural": [structural list],"middle": {type1:{},type2:{},...},"creation": [step list],"deviantart request": "request string"}"""

    def prompt(
        self, 
        image_path_or_url: str, 
        prompt: str = "", 
        need_json: bool = True,
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
        
        if not prompt:
            prompt = self.default_prompt
        

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
        # print(prompt)
        # 发送请求
        if need_json:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    #response_format = {'type': 'json_object'},
                )
            except Exception as e:
                if '1301' in str(e):
                    print("nsfw pic")
                    return {"nsfw": True}
                elif '1305' in str(e):
                    print("服务器当前压力大，等待300s再次尝试")
                    time.sleep(300)
                    return self.prompt(image_path_or_url, prompt, need_json, temperature, is_url)
                else:
                    raise e
            response_content = response.choices[0].message.content
            #print(response_content)
            try:
                old,new = repair_json(response_content)
                return new
            except Exception as e:
                print(e)
                return {"error": True}
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            return response.choices[0].message.content


class MultiGLM4V:
    def __init__(self, api_keys: list[str] | str, max_workers: int = 64, model: str = "glm-4v-plus-0111"):
        if isinstance(api_keys, str):
            if '\n' in api_keys:
                api_keys = convert_str_to_list(api_keys)
            else:
                api_keys = [api_keys]
        self.clients = [ZhipuAI(api_key=api_key) for api_key in api_keys]
        self.max_workers = max_workers
        self.account_counts = len(self.clients)
        for i in range(self.account_counts):
            self.clients[i] = GLM4V(api_key=api_keys[i], model=model)

    def prompt_one(self, image_path_or_url: str) -> str:
        import random
        account_index = random.randint(0, self.account_counts - 1)
        prompt_result = self.clients[account_index].prompt(image_path_or_url)
        if prompt_result:
            # json_path 是image_path_or_url的同名json文件路径

            json_path = image_path_or_url.replace(".jpg", ".json").replace(".png", ".json").replace(".jpeg", ".json").replace(".webp", ".json")
            with open(json_path, "w") as f:
                json.dump(prompt_result, f)
            os.remove(image_path_or_url)
            return prompt_result

    def prompt_images(self, image_paths: List[str]) -> str:
        # image_path_dict的键是图片位置，值是图片的描述
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.prompt_one, image_paths[i]) for i in range(len(image_paths))]
            for future in tqdm(concurrent.futures.as_completed(futures), 
                             total=len(futures), 
                             desc="处理图片中"):
                results.append(future.result())
        return results

    def prompt_folder(self, folder_path: str) -> str:
        # 遍历文件夹中的所有图片，移除有同名json文件的图片并调用prompt_images
        image_paths = []
        for file in os.listdir(folder_path):
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".webp"):
                json_path = file.replace(".jpg", ".json").replace(".png", ".json").replace(".jpeg", ".json").replace(".webp", ".json")
                if not os.path.exists(json_path):
                    image_paths.append(os.path.join(folder_path, file))
        return self.prompt_images(image_paths)


class MultiGLM4V_Mongo:
    def __init__(self, api_keys: list[str] | str, mongo_url: str, max_workers: int = 64, model: str = "glm-4v-plus-0111"):
        self.mongo_init(mongo_url)
        api_keys = self.get_accounts(api_keys)
        self.clients = [ZhipuAI(api_key=api_key) for api_key in api_keys]
        self.max_workers = max_workers
        self.account_counts = len(self.clients)
        for i in range(self.account_counts):
            self.clients[i] = GLM4V(api_key=api_keys[i], model=model)

    def get_accounts(self, api_keys: int):
        if isinstance(api_keys, str):
            if '\n' in api_keys:
                api_keys = convert_str_to_list(api_keys)
            else:
                api_keys = [api_keys]
        return api_keys

    def mongo_init(self, mongo_url: str):
        from pymongo import MongoClient
        mongo_client = MongoClient(mongo_url)
        art_db = mongo_client.get_database("art")
        self.caption_collection = art_db.get_collection("caption")

    def get_tasks(self) -> dict:
        self.tasks = list(self.caption_collection.aggregate([
            {"$match": {"status": 0}},  # 匹配未处理的文档
            {"$sample": {"size": 100}}  # 随机获取100个文档
        ]))

    def get_pic(self, task_id: int) -> str:
        from hfpics import HfPics
        # 或使用自定义配置
        hf = HfPics(
            repo="picollect/a_1024",  # 自定义数据集仓库
            cache_dir="/kaggle/working/pics"   # 自定义缓存目录
        )
        return hf.pic(task_id)

    def prompt_one(self, task_id: int) -> str:
        import random
        account_index = random.randint(0, self.account_counts - 1)
        prompt_result = self.clients[account_index].prompt(self.get_pic(task_id))
        if prompt_result:
            result = {}
            for k,v in prompt_result.items():
                if k == 'nsfw':
                    status = 403
                    self.caption_collection.update_one({'_id': task_id}, {'$set': {'status': status}}, upsert=True)
                    return
                if k == 'error':
                    status = 500
                    self.caption_collection.update_one({'_id': task_id}, {'$set': {'status': status}}, upsert=True)
                    return
                result[k] = v
            result['status'] = 200
            self.caption_collection.update_one({'_id': task_id}, {'$set': result}, upsert=True)

    def prompt_images(self) -> str:
        self.get_tasks()
        # image_path_dict的键是图片位置，值是图片的描述
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.prompt_one, task['_id']) for task in self.tasks]
            for future in tqdm(concurrent.futures.as_completed(futures), 
                             total=len(futures), 
                             desc="处理图片中"):
                results.append(future.result())
        return results