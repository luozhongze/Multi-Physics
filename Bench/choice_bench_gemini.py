import sys
import os
import argparse

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from api_gemini import GeminiAPI
from bench_function import export_distribute_json
from openai import OpenAI
import json


client = OpenAI(
    api_key=" ",
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

if __name__ == "__main__":

    with open("./MCQ_prompt1.json", "r", encoding="utf-8") as f:
        data = json.load(f)['examples']
    f.close()

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    model_name = "gemini-2.5-pro"
    api_key = " "
    model_api = GeminiAPI(api_key, model_name="gemini-2.5-pro", temperature=0.3, max_tokens=65536)

    multi_images = True 

        
    for i in range(len(data)):
        directory = "../Data"
        
        keyword = data[i]['keyword']
        question_type = data[i]['type']
        zero_shot_prompt_text = data[i]['prefix_prompt']
        print(model_name)
        print(keyword)
        print(question_type)

        export_distribute_json(
            model_api, 
            model_name, 
            directory, 
            keyword, 
            zero_shot_prompt_text, 
            question_type, 
            multi_images=multi_images
        )

    
