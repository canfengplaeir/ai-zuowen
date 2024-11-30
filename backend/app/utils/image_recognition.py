import base64
from typing import Optional, Tuple
from openai import OpenAI
from .env_manager import env_manager


class ImageRecognitionService:
    def __init__(self):
        api_key = env_manager.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.client = OpenAI(
            api_key=api_key, base_url=env_manager.get("OPENAI_BASE_URL")
        )

    def recognize_text(self, image_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        识别图片中的文字
        返回: (content, error_message)
        """
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")

            completion = self.client.chat.completions.create(
                model="qwen-vl-max",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                            {"type": "text", "text": "请识别并提取图片中的作文内容"},
                        ],
                    }
                ],
            )

            return completion.choices[0].message.content, None

        except Exception as e:
            error_msg = str(e)
            if "Arrearage" in error_msg:
                return None, "API 账户余额不足，请联系管理员充值"
            elif "invalid_api_key" in error_msg:
                return None, "API 密钥无效，请检查配置"
            else:
                print(f"图像识别失败: {error_msg}")  # 记录详细错误信息
                return None, "图像识别服务暂时不可用，请稍后重试"
