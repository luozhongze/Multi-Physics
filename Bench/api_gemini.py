# -*- coding: utf-8 -*-
import base64
import time
import random
from openai import OpenAI
import google.api_core.exceptions

client = OpenAI(
    api_key=" ",  
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

class GeminiAPI:
    def __init__(self, api_key, model_name, temperature, max_tokens, rate_limit_rpm=2000):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key
        self.rate_limit_rpm = rate_limit_rpm
        self.last_call_time = 0  

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def forward(self, prompt, question, picture):
        usr_content = [{"type": "text", "text": question}]
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

            for attempt in range(max_retries):
                try:
                    return func()  
                except google.api_core.exceptions.ResourceExhausted as e:
                   print(f"Error occurred (ResourceExhausted): {e}")
                   if attempt == max_retries - 1:
                      raise e  
                   sleep_duration = base_delay * (2 ** attempt) + random.uniform(0, 1) 
                   print(f"Retrying after {sleep_duration:.2f} seconds")
                   time.sleep(sleep_duration)
                except Exception as e: 
                    if "500" in str(e): 
                        print(f"Error 500: {e}")
                        return None 
                    else:
                        raise e 

        try: 
            response = retry_with_exponential_backoff(_api_call)
            return response
        except Exception as e: 
            print(f"Exception occurred in forward after retry: {e}")
            return None


    def postprocess(self, response):
         if response and response.choices and response.choices[0].message:
              return response.choices[0].message.content
         return ""


    def __call__(self, prompt: str, question: str, picture: list):

        min_delay = 60 / self.rate_limit_rpm

        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time

        if time_since_last_call < min_delay:
            time.sleep(min_delay - time_since_last_call)

        self.last_call_time = time.time()

        response = self.forward(prompt, question, picture)

        if response is None:
            return " "  

        if response and response.choices and response.choices[0].finish_reason == 'content_filter':
            return " "  

        model_output = self.postprocess(response)
        if model_output:
            return model_output
        else:
            print("Model output is empty, retrying...")
            return " "  


def test(model, prompt: str, question: str, picture: list):
    response = model(prompt, question, picture)
    return response

if __name__ == "__main__":
    api_key = " ",
    model_api = GeminiAPI(api_key, model_name="gemini-2.5-pro", temperature=0.3, max_tokens=65536)

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