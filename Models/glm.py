import torch
from PIL import Image
from vllm import LLM, SamplingParams

class GLM4V_API_vllm: # Class name modified to distinguish from the original version
    def __init__(self, model_path, device='cuda'): # device parameter is kept for interface consistency
        self.device = device # device parameter kept, vllm might handle it differently
        self.model_path = model_path

        # Load vllm LLM
        print(f"Loading vllm model, model path: {model_path}") # Log: vllm model loading start
        self.llm = LLM(model=model_path,
                       tensor_parallel_size=1, # Adjust according to actual situation
                       max_model_len=8192, # Adjust according to model and needs
                       trust_remote_code=True,
                       enforce_eager=True)

        print(f"vllm model loaded.") # Log: vllm model loading finish
        self.stop_token_ids = [151329, 151336, 151338] # GLM common stop tokens, adjust as needed
        self.sampling_params = SamplingParams(temperature=0.5, # Sampling parameters, can be adjusted
                                                max_tokens=8192,
                                                stop_token_ids=self.stop_token_ids,
                                                top_k=5,
                                                )


    def encode_image(self, image_path):
        try:
            image = Image.open(image_path).convert('RGB')
            return image
        except Exception as e:
            return None # Handle image open failure

    def forward(self, prompt, question, picture):
        # Prepare query, including prompt and question
        query = f"{prompt}\n{question}"

        # Get image path and load image
        image_path = picture[0] # Explicitly name image path variable
        image = self.encode_image(image_path)

        if image is None: # Important: Handle image loading failure
            return "**Image loading failed, please check the path**" # Return error message for image loading failure

        # Prepare vllm inputs format
        inputs = {
            "prompt": query,
            "multi_modal_data": {
                "image": image
            },
        }
        # print(inputs) # Print inputs for debugging - you can remove this after input check is done
        # Generate model response using vllm
        outputs = self.llm.generate(inputs, sampling_params=self.sampling_params) # prompt parameter accepts inputs dictionary directly
        for o in outputs: # vllm output format needs iteration
            response = o.outputs[0].text # Get generated text
            return response # Return the text of the first output

    def __call__(self, prompt: str, question: str, picture: list):
        # Call forward method to get result
        response = self.forward(prompt, question, picture)
        return response

def test_vllm(model, prompt: str, question: str, picture: list): # Function name modified to distinguish from original version
    response = model(prompt, question, picture)
    return response

if __name__ == "__main__":
    # Important: Please modify model_path to your actual model path
    model_path = "./glm-4v" # Replace with your GLM-4V model local path

    # Initialize GLM-4V model API (vllm version)
    model_api_vllm = GLM4V_API_vllm(model_path=model_path) # Use vllm version of API

    # Example data (keep unchanged)
    data_example = {
        "category": "exclusive",
        "question": "中国宋代科学家沈括在公元1086年写的《梦溪笔谈》中最早记载了“方家(术士)以磁石磨针锋，则能指南，然常微偏东，不全南也”。进一步研究表明，地球周围地磁场的磁感线分布如图所示，结合上述材料，下列说法正确的是\nA.在地磁场的作用下小磁针静止时指南的磁极叫北极，指北的磁极叫南极\nB. 对垂直射问地球表面宇宙射线中的高能带电粒子，在南、北极所受阻挡作用最弱，赤道附近最强\nC. 形成地磁场的原因可能是带正电的地球自转引起的\nD. 由于地磁场的影响，在奥斯特发现电流磁效应的实验中，通电导线应相对水平地面竖直放置",
        "picture": ["../Data/9/1_0.png"],
        "answer": ["B"],
        "analysis": "地球内部存在磁场，地磁南极在地理北极附近；所以在地磁场的作用下小磁针静止时指南的磁极叫南极，指北的磁极叫北极，选项错误；在地球的南北极地磁的方向与几乎地面垂直，对垂直射向地球表面宇宙射线中的高能带电粒子，在南、北极所受阻挡作用最弱，赤道附近的磁场方向与地面平行则高能粒子所受的磁场力最大，选项B正确；地球自转方向自西向东，地球的南极是地磁场的北极，由安培定则判断可能地球是带负电的，故C错误；在奥斯特发现电流磁效应的实验中，若通电导线相对水平地面竖直放置，地磁场方向与导线电流的方向垂直，则根据安培定则可知，地磁场对实验的影响较大，故在进行奥斯特实验时，通电导线南北放置时实验现象最明显，故D错误；故选B",
        "index": 1
    }

    choice_question = data_example['question']
    choice_picture = data_example['picture']
    choice_prompt = "请你做一道物理选择题。\n请你结合文字和图片一步一步思考。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下："

    result_vllm = test_vllm(model_api_vllm, choice_prompt, choice_question, choice_picture) # Use vllm version of test function and model api
    print("Model output (vllm):\n" + result_vllm) # Output result marked as vllm
