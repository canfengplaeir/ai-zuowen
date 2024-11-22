使用python,sqlite,vue,daisyui写一个AI批改作文
1. 登录和注册系统
2. 上传作文
3. 批改作文
4. 查看批改结果
5. 查看历史批改记录
6. 修改个人信息
7. 修改密码
8. 退出登录
9. 管理员功能
10.批改完成的作文进行保存

#工作流
图像识别AI识别作文,获取内容 > 语言模型AI批改作文 > 返回批改结果(包含分数,批改意见)


#以下是参考文档

我的API_key:sk-e9e56ee4ab4d42c6b2d87058de20c84d

##千问语言turbo大模型(后续如果该模型效果不好,可以更换其他模型)
model_id: qwen-turbo
文本输出:
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-turbo", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': '你是一个高中英语老师,你的任务是批改作文'},
        {'role': 'user', 'content': '你的作文内容'}],
    )
    
print(completion.model_dump_json())
```


##千问图像理解模型
model_id: qwen-vl-max
```python
from openai import OpenAI
import os
import base64
#  base 64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image("test.png")
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-vl-max-latest",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}, # 传入base64_image字符串 
                },
                {"type": "text", "text": "这是什么"},
            ],
        }
    ],
)
print(completion.choices[0].message.content)
```

