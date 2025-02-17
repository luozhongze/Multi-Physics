# -*- coding: utf-8 -*-
import base64
import time
import random
from openai import OpenAI


client = OpenAI(
    api_key="sk-4edd528b52524765893eec7f96b39b12",  # 如果使用环境变量，请设置环境变量"YOUR_API_KEY"
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


class QwenAPI:
    def __init__(self, api_key, model_name, temperature, max_tokens):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def forward(self, prompt, question, picture):
        # 构建 content 列表，先添加文本部分
        usr_content = [{"type": "text", "text": question}]
        # 再添加图片部分
        for pic in picture:
            usr_content.append({
                'type': "image_url",
                'image_url': {"url": f"data:image/png;base64,{self.encode_image(pic)}"}
            })

        def _api_call():
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "system",
                    "content": prompt
                },
                    {
                        "role": "user",
                        "content": usr_content
                    }],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response

        def retry_with_exponential_backoff(func, max_retries=5, base_delay=5):
            """ 使用指数退避策略重试一个函数调用
            func: 要调用的函数
            max_retries: 最大重试次数
            base_delay: 基础延迟时间（秒）
            """
            for attempt in range(max_retries):
                try:
                    return func()  # 尝试调用函数
                except Exception as e:
                    print(f"Error occurred: {e}")
                    if attempt == max_retries - 1:
                        raise e  # 超过最大次数，抛出异常
                    sleep_duration = base_delay * (2 ** attempt) + random.uniform(0, 1)  # 计算退避延迟
                    print(f"Retrying after {sleep_duration:.2f} seconds")
                    time.sleep(sleep_duration)
            
        while True:
            try:
                response = retry_with_exponential_backoff(_api_call)
                return response
            except Exception as e:
                print(f"Exception occurred: {e}")
                time.sleep(1)


    def postprocess(self, response):
         if response and response.choices and response.choices[0].message:
              return response.choices[0].message.content
         return ""


    def __call__(self, prompt: str, question: str, picture: list):
       while True:
           response = self.forward(prompt, question, picture)
           
           if response and response.choices and response.choices[0].finish_reason == 'content_filter':
               print("模型输出被内容过滤器拦截，跳过当前题目。")
               return " "  # 返回 None，表示被过滤器拦截
           model_output = self.postprocess(response)
           if model_output: # 如果model_output不为空
               return model_output
           else:
               print("Model output is empty, retrying...") # 输出model为空的信息，并重新进行调用

def test(model, prompt: str, question: str, picture: list):
    response = model(prompt, question, picture)
    return response

if __name__ == "__main__":
    api_key = "sk-4edd528b52524765893eec7f96b39b12",
    model_api = QwenAPI(api_key, model_name="qwen-vl-plus-latest", temperature=0, max_tokens=8192)

    data_example = {
        "category": "exclusive",
        "question": "中国宋代科学家沈括在公元1086年写的《梦溪笔谈》中最早记载了“方家(术士)以磁石磨针锋，则能指南，然常微偏东，不全南也”。进一步研究表明，地球周围地磁场的磁感线分布如图所示，结合上述材料，下列说法正确的是\nA.在地磁场的作用下小磁针静止时指南的磁极叫北极，指北的磁极叫南极\nB. 对垂直射问地球表面宇宙射线中的高能带电粒子，在南、北极所受阻挡作用最弱，赤道附近最强\nC. 形成地磁场的原因可能是带正电的地球自转引起的\nD. 由于地磁场的影响，在奥斯特发现电流磁效应的实验中，通电导线应相对水平地面竖直放置",
        "picture": [
            "../Data/9/1_0.png"
        ],
        "answer": [
            "B"
        ],
        "analysis": "地球内部存在磁场，地磁南极在地理北极附近；所以在地磁场的作用下小磁针静止时指南的磁极叫南极，指北的磁极叫北极，选项错误；在地球的南北极地磁的方向与几乎地面垂直，对垂直射向地球表面宇宙射线中的高能带电粒子，在南、北极所受阻挡作用最弱，赤道附近的磁场方向与地面平行则高能粒子所受的磁场力最大，选项B正确；地球自转方向自西向东，地球的南极是地磁场的北极，由安培定则判断可能地球是带负电的，故C错误；在奥斯特发现电流磁效应的实验中，若通电导线相对水平地面竖直放置，地磁场方向与导线电流的方向垂直，则根据安培定则可知，地磁场对实验的影响较大，故在进行奥斯特实验时，通电导线南北放置时实验现象最明显，故D错误；故选B",
        "index": 1
    }

    choice_question = data_example['question']
    choice_picture = data_example['picture']
    choice_prompt = "请你做一道物理选择题。\n请你结合文字和图片一步一步思考。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下："

    result = test(model_api, choice_prompt, choice_question, choice_picture)

    print("Model output:\n" + result)