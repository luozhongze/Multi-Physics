# -*- coding: utf-8 -*-
import json
import re
import time
import codecs
import os
import random 
from api_gemini import GeminiAPI
from tqdm import tqdm


def extract_reasoning_steps(model_output):
    reasoning_content = ""
    start_index = model_output.find("【解析】")
    eoe_index = model_output.find("<eoe>")
    answer_index = model_output.find("【答案】")
    newline_index = model_output.find("\n\n", start_index + len("【解析】") if start_index != -1 else 0)

    end_index = -1

    if answer_index != -1:
        end_index = answer_index
    elif newline_index != -1:
        end_index = newline_index
    elif eoe_index != -1:
        end_index = eoe_index
    elif start_index != -1 and end_index == -1:
        reasoning_content = model_output[start_index + len("【解析】"):].strip()


    if start_index != -1 and end_index != -1 and start_index < end_index:
        reasoning_content = model_output[start_index + len("【解析】"):end_index].strip()
    elif start_index != -1 and end_index == -1:
        reasoning_content = model_output[start_index + len("【解析】"):].strip()


    steps = []
    if reasoning_content:
        step_pattern = re.compile(r'\d+\.\s')
        raw_steps = step_pattern.split(reasoning_content)
        steps = [step.strip() for step in raw_steps if step.strip()]
    return steps

def evaluate_step_correctness(model_api, question, picture, analysis, step_text, standard_answer):

    picture_prompt_part = ""
    if picture:
        picture_prompt_part = f"""题目图片：
{picture}
"""

    step_eval_prompt = f"""请你扮演一位物理学专家，你的任务是判断以下物理题解题步骤是否正确。

题目：
{question}

{picture_prompt_part}

题目标准答案：
{standard_answer}

题目标准解析：
{analysis}

需要判断的解题步骤：
{step_text}

请结合【题目】、【题目标准答案】和【题目标准解析】的逻辑和物理原理。
判断【需要判断的解题步骤】是否完全正确。
你的回答只能是 "正确" 或 "错误" 中的一个，不要输出额外的解释或说明。
如果你无法判断，请注意只要该步骤存在错误的地方就是错误的。
请直接给出判断结果："""

    attempt = 0
    base_delay = 60 

    while True:  
        try:
            response = model_api(step_eval_prompt, "", picture)
            if response:
                judgement = response.strip().lower()
                if "正确" in judgement or "correct" in judgement:
                    return "正确"
                elif "错误" in judgement or "incorrect" in judgement:
                    return "错误"
            return "无法判断"

        except Exception as e:
            if "429" in str(e) and "RESOURCE_EXHAUSTED" in str(e):
                attempt += 1
                delay = (base_delay * (2 ** (attempt - 1))) + random.uniform(0, 15)
                
                tqdm.write(f"\n[API速率限制] 遭遇 429 错误。这是第 {attempt} 次尝试。")
                tqdm.write(f"程序将暂停约 {int(delay / 60)} 分钟后自动重试...")
                
                time.sleep(delay)
                continue
            else:
                tqdm.write(f"\n[API未知错误] 发生了一个非速率限制的API错误: {e}")
                tqdm.write("该步骤将被记为“无法判断”，程序将继续处理下一个步骤。")
                return "无法判断"


def process_single_example(model_api, prompt_prefix, example, original_data_dict):

    index = example['index']
    category = example['category']
    question = example['question']
    standard_answer = example['standard_answer']
    analysis = example['analysis']
    model_output = example['model_output']

    original_example = original_data_dict.get(index)
    picture = original_example['picture'] if original_example and 'picture' in original_example else []

    steps = extract_reasoning_steps(model_output)
    step_judgements = []
    correct_steps_count = 0

    for step_text in steps:
        judgement = evaluate_step_correctness(model_api, prompt_prefix, question, picture, analysis, step_text, standard_answer)
        step_judgements.append({'step': step_text, 'judgement': judgement})
        if judgement == "正确":
            correct_steps_count += 1

    step_accuracy = 0.0
    if steps:
        step_accuracy = correct_steps_count / len(steps)

    evaluated_example = {
        'index': index,
        'category': category,
        'question': question,
        'standard_answer': standard_answer,
        'analysis': analysis,
        'model_output': model_output,
        'reasoning_steps_evaluation': step_judgements,
        'step_accuracy': step_accuracy,
        'step_count': len(steps),
        'picture_used_for_evaluation': picture
    }
    return evaluated_example

def evaluate_reasoning_accuracy(model_api, data_file_path, result_json_path, original_data_dict):

    with open(data_file_path, 'r', encoding='utf-8') as f_result:
        result_data = json.load(f_result)

    output_dir = os.path.join(os.path.dirname(result_json_path), "evaluated_results")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file_path = os.path.join(output_dir, os.path.basename(result_json_path).replace(".json", "_evaluated.json"))

    output_data = {}
    evaluated_indices = set()
    
    if os.path.exists(output_file_path):
        tqdm.write(f"检测到已存在的评估文件，将从 {output_file_path} 继续。")
        try:
            with codecs.open(output_file_path, 'r', 'utf-8') as f_existing:
                output_data = json.load(f_existing)
                evaluated_indices = {ex['index'] for ex in output_data.get('evaluated_example', [])}
                tqdm.write(f"已找到 {len(evaluated_indices)} 个已评估的题目。")
        except (json.JSONDecodeError, IOError) as e:
            tqdm.write(f"警告：无法读取或解析旧的评估文件 '{output_file_path}' (错误: {e})。将重新开始评估该文件。")
            output_data = {}
            evaluated_indices = set()

    if not output_data:
        output_data = {
            'keyword': result_data['keyword'],
            'model_name': result_data['model_name'],
            'prompt': result_data['prompt'],
            'evaluated_example': [],
            'average_step_accuracy': 0.0,
            'average_step_count': 0.0
        }

    evaluated_list = output_data.get('evaluated_example', [])
    step_accuracy_sum = sum(ex.get('step_accuracy', 0.0) for ex in evaluated_list)
    step_count_sum = sum(ex.get('step_count', 0) for ex in evaluated_list)
    example_count = len(evaluated_list)
    
    model_name = result_data['model_name']
    prompt_prefix = result_data['prompt']
    
    examples_to_process = [ex for ex in result_data['example'] if ex['index'] not in evaluated_indices]

    if not examples_to_process:
        tqdm.write(f"文件 {os.path.basename(data_file_path)} 中的所有题目均已评估完毕。")
    else:
        with codecs.open(output_file_path, 'w', 'utf-8') as outfile:
            for example in tqdm(examples_to_process, desc=f"评估剩余题目于 {os.path.basename(data_file_path)}", dynamic_ncols=True):
                evaluated_example = process_single_example(model_api, prompt_prefix, example, original_data_dict)
                output_data['evaluated_example'].append(evaluated_example)
                
                step_accuracy_sum += evaluated_example['step_accuracy']
                step_count_sum += evaluated_example['step_count']
                example_count += 1
                
                output_data['average_step_accuracy'] = step_accuracy_sum / example_count if example_count > 0 else 0.0
                output_data['average_step_count'] = step_count_sum / example_count if example_count > 0 else 0.0
                
                outfile.seek(0)
                outfile.truncate()
                json.dump(output_data, outfile, ensure_ascii=False, indent=4)
                outfile.flush()
                time.sleep(1)

    final_avg_accuracy = output_data.get('average_step_accuracy', 0.0)
    final_avg_count = output_data.get('average_step_count', 0.0)
    print(f"文件 {os.path.basename(data_file_path)} 的平均步骤正确率: {final_avg_accuracy:.4f}")
    print(f"文件 {os.path.basename(data_file_path)} 的平均步骤数: {final_avg_count:.2f}")
    print(f"评估结果已保存至: {output_file_path}")

    return step_accuracy_sum, step_count_sum, example_count



if __name__ == "__main__":

    api_key = " "  
    model_api = GeminiAPI(api_key, model_name="gemini-2.5-flash", temperature=0, max_tokens=8192)

    results_dir = "../Results/gemma-3-27b-it" 
    data_dir = "../Data" 

    model_name_prefix = os.path.basename(results_dir) 

    global_step_accuracy_sum = 0.0
    global_step_count_sum = 0.0
    global_example_count = 0

    for i in range(1, 12):
        result_json_file = f"{model_name_prefix}_{i}.json"
        data_json_file = f"{i}.json"

        result_json_file_path = os.path.join(results_dir, result_json_file)
        data_json_file_path = os.path.join(data_dir, data_json_file)

        original_data_file_path = data_json_file_path 

        print(f"\n开始处理文件: {result_json_file_path}")

        if not os.path.exists(result_json_file_path):
            print(f"错误：找不到结果文件 {result_json_file_path}，跳过。")
            continue
        if not os.path.exists(original_data_file_path):
            print(f"错误：找不到原始数据文件 {original_data_file_path}，跳过。")
            continue

        with open(original_data_file_path, 'r', encoding='utf-8') as f_original:
            original_data = json.load(f_original)
        original_data_dict = {item['index']: item for item in original_data['example']}

        step_accuracy_file_sum, step_count_file_sum, example_file_count = evaluate_reasoning_accuracy(model_api, result_json_file_path, result_json_file_path, original_data_dict) 
        
        global_step_accuracy_sum += step_accuracy_file_sum
        global_step_count_sum += step_count_file_sum
        global_example_count += example_file_count

    if global_example_count > 0:
        global_average_step_accuracy = global_step_accuracy_sum / global_example_count 
        global_average_step_count = global_step_count_sum / global_example_count
    else:
        global_average_step_accuracy = 0.0
        global_average_step_count = 0.0

    print("\n-----------------------------------")
    print("所有主题的全局评估结果:")
    print(f"全局平均步骤正确率: {global_average_step_accuracy:.4f}")
    print(f"全局平均步骤数: {global_average_step_count:.2f}")
    print("所有文件的评估已完成!")