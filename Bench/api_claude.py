# -*- coding: utf-8 -*-
import base64
import time
import random
import anthropic

class ClaudeAPI:
    def __init__(self, api_key, model_name, temperature, max_tokens):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = anthropic.Anthropic(api_key=api_key)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode('utf-8')

    def forward(self, prompt, question, picture):
        # Get image base64 encoding
        usr_content = [{"type": "text", "text": question}]
        
        for pic in picture:
            image_data = self.encode_image(pic)
            image_media_type = "image/png"  # Adjust media type based on your image format

            usr_content.append({
                'type': "image",
                'source': {
                    'type': 'base64',
                    'media_type': image_media_type,
                    'data': image_data,
                }
            })

        def _api_call():
            response = self.client.messages.create(
                model=self.model_name,
                system=prompt,  # Pass system prompt as a top-level key
                messages=[
                    {
                        "role": "user",
                        "content": usr_content
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response

        def retry_with_exponential_backoff(func, max_retries=5, base_delay=5):
            """ Retry function with exponential backoff strategy """
            for attempt in range(max_retries):
                try:
                    return func()  # Try calling the function
                except Exception as e:
                    print(f"Error occurred: {e}")
                    if attempt == max_retries - 1:
                        raise e  # If max retries exceeded, raise exception
                    sleep_duration = base_delay * (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff
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
        if response and hasattr(response, 'content') and response.content:
            # 提取 content 中的文本
            return response.content[0].text
        return ""
    
    def __call__(self, prompt: str, question: str, picture: list):
        while True:
            response = self.forward(prompt, question, picture)

            # 如果返回的数据中包含 'content'，则提取文本
            if response and hasattr(response, 'content') and response.content:
                model_output = self.postprocess(response)
                if model_output:  # 如果模型输出不为空
                    return model_output
                else:
                    print("Model output is empty, retrying...")  # 如果模型输出为空，则重试
            else:
                print("没有 'content' 字段，正在查看原始响应。")
                # 如果没有 'content' 字段，返回原始响应
                return str(response)


def test(model, prompt: str, question: str, picture: list):
    response = model(prompt, question, picture)
    
    return response


if __name__ == "__main__":
    api_key = " "
    model_api = ClaudeAPI(api_key, model_name="claude-3-5-sonnet-20241022", temperature=0, max_tokens=8192)

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
