### This file is used to generate the json file for the benchmarking of the model
import sys
import os
import argparse

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from api_grok import GrokAPI
from bench_function import export_distribute_json
from openai import OpenAI
import json


client = OpenAI(
    api_key=" ",
    base_url="https://api.x.ai/v1",
)

if __name__ == "__main__":

    # Load the MCQ_prompt.json file
    with open("./MCQ_prompt1.json", "r", encoding="utf-8") as f:
        data = json.load(f)['examples']
    f.close()

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    model_name = "grok-2-vision-1212"
    api_key = " "
    model_api = GrokAPI(api_key, model_name="grok-2-vision-1212", temperature=0, max_tokens=8192)

    multi_images = True # whether to support multi images input, True means support, False means not support

        
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
