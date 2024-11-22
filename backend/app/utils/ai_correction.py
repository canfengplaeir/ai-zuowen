import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# 确保在最开始就加载环境变量
load_dotenv()

class AICorrectionService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("OPENAI_BASE_URL")
        )

    def correct_essay(self, content: str) -> str:
        """批改作文"""
        try:
            system_prompt = """
你是经验丰富的高中英语教师，具有多年的教学经验和深入的语言知识。你的目标是帮助学生提高英语写作能力，特别是应用文和读后续写的技能。请保持积极鼓励的态度，同时提供具体且建设性的反馈。

评分标准：
- 应用文（15分）：内容完整性（5分）、语言准确性（5分）和格式正确性（5分）
- 读后续写（25分）：创意与连贯性（10分）、语言运用（10分）和逻辑结构（5分）

请按以下流程批改：
1. 阅读理解：仔细阅读作文，理解意图和内容
2. 错误标注：标记语法、拼写、标点符号等错误
3. 内容评估：评估内容是否符合要求
4. 语言使用：评价词汇选择和句子结构
5. 格式检查：检查格式或故事连贯性
6. 打分：给出详细的分项评分
7. 建议与鼓励：指出优点和改进建议
8. 学习指导：推荐学习资源和练习方法

请用中文回复，并按以下格式输出：

【总体评价】
(整体表现的评价)

【错误分析】
(具体的错误标注和解释)

【分项评分】
- 内容/创意：X分
- 语言：X分
- 格式/结构：X分
- 总分：X分

【改进建议】
(具体的改进方向和建议)

【学习指导】
(推荐的学习资源和方法)
"""
            completion = self.client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {
                        'role': 'system', 
                        'content': system_prompt
                    },
                    {
                        'role': 'user', 
                        'content': content
                    }
                ]
            )
            
            if completion.choices and completion.choices[0].message:
                result = completion.choices[0].message.content
                if result is not None:
                    return result
            return "批改失败：无法获取AI响应"
            
        except Exception as e:
            print(f"批改出错: {str(e)}")  # 添加日志
            return f"批改出错: {str(e)}" 