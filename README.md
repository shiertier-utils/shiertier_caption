# shiertier_caption

一个使用智谱AI GLM4V-Flash模型进行图片描述的Python包。

## 安装

```bash
pip install shiertier_caption
```

## 使用方法

```python
from shiertier_caption import GLM4VFlash

# 初始化客户端
client = GLM4VFlash(api_key="your_api_key")

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

## 功能特点

- 支持本地图片和URL图片
- 简单易用的API接口
- 自动处理base64编码
- 完整的错误处理

## API文档

### GLM4VFlash类

```python
GLM4VFlash(api_key: str)
```

参数:
- `api_key`: 智谱AI的API密钥

### prompt方法

```python
prompt(image_path_or_url: str, prompt: str, is_url: bool = False) -> str
```

参数:
- `image_path_or_url`: 图片的本地路径或URL
- `prompt`: 关于图片的提问
- `is_url`: 是否为URL链接，默认为False（即本地文件）

返回值:
- 返回模型的文本回答
- 如果发生错误，返回错误信息字符串

## 许可证

MIT License 