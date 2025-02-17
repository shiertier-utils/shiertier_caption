# shiertier_caption

一个使用智谱AI GLM4V系列模型进行图片描述的Python包。支持GLM4V-Flash、GLM4V、GLM4V-Plus等多个模型。

## 特点

- 支持多种GLM4V模型
- 支持本地图片和URL图片输入
- 支持多API密钥并行处理
- 支持MongoDB存储和批量处理
- 自动处理JSON响应格式
- 完整的错误处理机制

## 安装

```bash
pip install shiertier_caption
```

## 基础使用

### 单图片处理

```python
from shiertier_caption import GLM4V

# 初始化客户端
client = GLM4V(api_key="your_api_key", model="glm-4v-plus-0111")

# 使用本地图片
response = client.prompt(
    image_path_or_url="path/to/your/image.jpg",
    prompt="描述这张图片"
)
print(response)

# 使用URL图片
response = client.prompt(
    image_path_or_url="https://example.com/image.jpg",
    prompt="描述这张图片",
    is_url=True
)
print(response)
```

### 批量处理

```python
from shiertier_caption import MultiGLM4V

# 使用多个API密钥初始化
api_keys = ["key1", "key2", "key3"]
client = MultiGLM4V(api_keys=api_keys, max_workers=64)

# 处理文件夹中的所有图片
results = client.prompt_folder("path/to/image/folder")

# 处理指定的图片列表
image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
results = client.prompt_images(image_paths)
```

### MongoDB支持

```python
from shiertier_caption import MultiGLM4V_Mongo

# 初始化MongoDB支持的客户端
client = MultiGLM4V_Mongo(
    api_keys=api_keys,
    mongo_url="mongodb://localhost:27017",
    max_workers=64
)

# 处理任务
results = client.prompt_images()
```

## API文档

### GLM4V类

```python
GLM4V(api_key: str, model: str = "glm-4v-plus-0111")
```

参数:
- `api_key`: 智谱AI的API密钥
- `model`: 模型名称，可选值：
  - glm-4v-flash
  - glm-4v
  - glm-4v-plus
  - glm-4v-plus-0111

### prompt方法

```python
prompt(
    image_path_or_url: str,
    prompt: str = "",
    need_json: bool = True,
    temperature: float = 0.8,
    is_url: bool = False
) -> str
```

参数:
- `image_path_or_url`: 图片的本地路径或URL
- `prompt`: 关于图片的提问，默认使用预设的描述提示词
- `need_json`: 是否需要JSON格式的响应
- `temperature`: 采样温度，控制输出的随机性
- `is_url`: 是否为URL链接

返回值:
- 如果need_json为True，返回JSON格式的描述
- 如果need_json为False，返回文本格式的描述

### MultiGLM4V类

```python
MultiGLM4V(api_keys: Union[List[str], str], max_workers: int = 64, model: str = "glm-4v-plus-0111")
```

参数:
- `api_keys`: API密钥列表或包含多个密钥的字符串
- `max_workers`: 最大并行工作线程数
- `model`: 使用的模型名称

### MultiGLM4V_Mongo类

```python
MultiGLM4V_Mongo(api_keys: Union[List[str], str], mongo_url: str, max_workers: int = 64, model: str = "glm-4v-plus-0111")
```

### SiliconFlow类

```python
from shiertier_caption import SiliconFlow
s = SiliconFlow(api_key: str, model: str = "Qwen/Qwen2-VL-72B-Instruct")

s.prompt(
    image_path_or_url: str,
    prompt: str = "",
    is_url: bool = False
) -> str

```

参数:
- `api_key`: 硅基流动的API密钥
- `model`: 使用的模型名称





## 许可证

MIT License