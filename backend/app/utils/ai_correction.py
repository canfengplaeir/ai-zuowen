from typing import Optional, Tuple
from openai import OpenAI
import base64
import json


def encode_image(image_path: str) -> str:
    """将图片转换为base64编码"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class AIService:
    def __init__(self, api_key: str, base_url: str):
        """初始化 AI 服务"""
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def process_essay(
        self, image_path: str
    ) -> Tuple[Optional[str], Optional[dict], Optional[int]]:
        """处理作文图片：识别文本并批改"""
        try:
            base64_image = encode_image(image_path)

            system_prompt = """你是一个专业的英语教师。请识别图片中的英语作文内容，并按照以下JSON格式返回批改结果：
{
    "content": "识别出的作文原文",
    "score": 分数(0-100的整数),
    "overall_feedback": "总体评价",
    "grammar_issues": [
        {
            "error": "错误内容",
            "correction": "修改建议",
            "explanation": "解释说明"
        }
    ],
    "vocabulary_feedback": {
        "highlights": ["好的用词1", "好的用词2"],
        "suggestions": ["改进建议1", "改进建议2"]
    },
    "structure_analysis": {
        "strengths": ["优点1", "优点2"],
        "weaknesses": ["不足1", "不足2"]
    },
    "improvement_suggestions": ["建议1", "建议2"]
}

请注意：
0.使用中文输出
1. 必须返回合法的JSON格式
2. content字段必须包含完整的作文原文
3. 评分标准：90-100优秀，80-89良好，70-79中等，60-69及格，60以下不及格
4. 所有字段都必须存在且格式正确"""

            completion = self.client.chat.completions.create(
                model="qwen-vl-max",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            }
                        ],
                    },
                ],
            )

            if completion.choices and completion.choices[0].message:
                result = completion.choices[0].message.content
                print("AI返回结果:", result)  # 添加调试日志

                try:
                    # 尝试清理和格式化 JSON 字符串
                    result = result.strip()
                    if result.startswith("```json"):
                        result = result[7:]
                    if result.endswith("```"):
                        result = result[:-3]
                    result = result.strip()

                    feedback_json = json.loads(result)

                    # 验证必要字段
                    if not all(
                        key in feedback_json
                        for key in ["content", "score", "overall_feedback"]
                    ):
                        raise ValueError("返回结果缺少必要字段")

                    # 提取内容和分数
                    content = feedback_json.pop("content", "")
                    score = int(feedback_json.get("score", 0))

                    return content, feedback_json, score

                except json.JSONDecodeError as e:
                    print(f"JSON解析错误: {str(e)}, 原始内容: {result}")
                    return None, "AI返回的结果格式不正确", None
                except ValueError as e:
                    print(f"数据验证错误: {str(e)}")
                    return None, str(e), None

            return None, "AI未返回有效结果", None

        except Exception as e:
            print(f"AI处理错误: {str(e)}")  # 添加日志
            return None, f"处理出错: {str(e)}", None
