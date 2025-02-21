# -*- coding: utf-8 -*-
import json
import re
import time
import codecs  # Import the codecs module
import os
from api_gemini import GeminiAPI
from tqdm import tqdm  # Import tqdm for progress bar

def extract_reasoning_steps(model_output):
    """Extract reasoning steps from the model output, between 【解析】 and 【答案】 or \\n\\n or <eoe>"""
    reasoning_content = ""
    start_index = model_output.find("【解析】")
    eoe_index = model_output.find("<eoe>")
    answer_index = model_output.find("【答案】")
    newline_index = model_output.find("\n\n", start_index + len("【解析】") if start_index != -1 else 0) # Start searching from after 【解析】

    end_index = -1 # Initialize end_index to -1, indicating not found

    # Prioritize 【答案】, then \n\n, and finally <eoe>
    if answer_index != -1:
        end_index = answer_index
    elif newline_index != -1:
        end_index = newline_index
    elif eoe_index != -1:
        end_index = eoe_index
    elif start_index != -1 and end_index == -1: # If only 【解析】 is present without an ending marker, extract to the end
        reasoning_content = model_output[start_index + len("【解析】"):].strip()


    if start_index != -1 and end_index != -1 and start_index < end_index:
        reasoning_content = model_output[start_index + len("【解析】"):end_index].strip()
    elif start_index != -1 and end_index == -1: # If only 【解析】 is present without an ending marker, extract to the end
        reasoning_content = model_output[start_index + len("【解析】"):].strip()


    steps = []
    if reasoning_content:
        # Use regular expression to split steps, matching numerical序号 and dot
        step_pattern = re.compile(r'\d+\.\s')
        raw_steps = step_pattern.split(reasoning_content)
        # Remove the empty string produced by the first split and remove leading/trailing whitespace from each step
        steps = [step.strip() for step in raw_steps if step.strip()]
    return steps

def evaluate_step_correctness(model_api, prompt, question, picture, analysis, step_text):
    """Call Gemini API to judge the correctness of a single step"""
    picture_prompt_part = ""
    if picture: # Always add the picture prompt part, assuming picture always exists and is not empty
        picture_prompt_part = f"""题目图片：
{picture}
"""

    step_eval_prompt = f"""请你扮演一位物理学专家，你的任务是判断以下物理题解题步骤是否正确。

题目：
{question}

{picture_prompt_part}

题目标准解析：
{analysis}

需要判断的解题步骤：
{step_text}

请判断【需要判断的解题步骤】是否符合【题目标准解析】的逻辑和物理原理。
你的回答只需要是 "正确" 或 "错误" 中的一个，不要输出额外的解释或说明。
请直接给出判断结果："""

    response = model_api(step_eval_prompt, "", picture) # question is in prompt, pass empty string for question parameter here
    if response:
        judgement = response.strip().lower()
        if "正确" in judgement or "correct" in judgement: # Compatible with Chinese and English answers
            return "正确"
        elif "错误" in judgement or "incorrect" in judgement:
            return "错误"
    return "无法判断" # API call failed or other situations

def evaluate_reasoning_accuracy(model_api, data_file_path, result_json_path, original_data_dict): # Add original_data_dict parameter
    """Evaluate the correctness rate of model reasoning steps and output JSON results **while calling API**"""
    with open(data_file_path, 'r', encoding='utf-8') as f_result:
        result_data = json.load(f_result)

    output_dir = os.path.join(os.path.dirname(result_json_path), "evaluated_results") # Create subdirectory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file_path = os.path.join(output_dir, os.path.basename(result_json_path).replace(".json", "_evaluated.json")) # Generate new filename

    output_data = { # Initialize output_data, including basic information and empty evaluated_example list
        'keyword': result_data['keyword'],
        'model_name': result_data['model_name'],
        'prompt': result_data['prompt'],
        'evaluated_example': [],
        'average_step_accuracy': 0.0 # Initialize average_step_accuracy in output_data
    }

    # Use codecs.open to support UTF-8 encoding, and use 'w+' mode
    with codecs.open(output_file_path, 'w+', 'utf-8') as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=4) # Write initial output_data structure first
        outfile.flush() # Immediately write buffer content to file

        model_name = result_data['model_name']
        prompt_prefix = result_data['prompt']
        examples = result_data['example']

        step_accuracy_sum = 0.0 # Initialize sum of step accuracies
        example_count = 0 # Initialize count of examples

        # Wrap examples with tqdm for progress bar
        for example in tqdm(examples, desc=f"Evaluating questions in {os.path.basename(data_file_path)}", dynamic_ncols=True):
            evaluated_example = process_single_example(model_api, prompt_prefix, example, original_data_dict) # Call function to process single example
            output_data['evaluated_example'].append(evaluated_example) # Add evaluation result to output_data
            step_accuracy_sum += evaluated_example['step_accuracy'] # Accumulate step accuracy
            example_count += 1 # Increment example count

            # Overwrite the entire output_data, but because of append mode, the previous basic structure is preserved, only evaluated_example list grows
            outfile.seek(0) # Move file pointer to the beginning of the file
            outfile.truncate() # Clear file content
            output_data['average_step_accuracy'] = step_accuracy_sum / example_count if example_count > 0 else 0.0 # Calculate and update average_step_accuracy
            json.dump(output_data, outfile, ensure_ascii=False, indent=4) # Write updated output_data
            outfile.flush() # Immediately write buffer content to file
            time.sleep(1) # Avoid too fast requests

        average_step_accuracy = output_data['average_step_accuracy'] # Retrieve calculated average from output_data
        print(f"Average Step Accuracy for {os.path.basename(data_file_path)}: {average_step_accuracy:.4f}") # Print average step accuracy for the file
        print(f"The evaluation results have been saved to: {output_file_path}")


def process_single_example(model_api, prompt_prefix, example, original_data_dict): # Function definition also needs to update original_data_dict parameter
    """Process evaluation logic for a single question and return evaluated_example dictionary"""
    index = example['index']
    category = example['category']
    question = example['question']
    standard_answer = example['standard_answer']
    analysis = example['analysis']
    model_output = example['model_output']

    # Get picture information from original data
    original_example = original_data_dict.get(index)
    picture = original_example['picture'] if original_example and 'picture' in original_example else []

    steps = extract_reasoning_steps(model_output)
    step_judgements = []
    correct_steps_count = 0

    for step_text in steps:
        judgement = evaluate_step_correctness(model_api, prompt_prefix, question, picture, analysis, step_text)
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
        'picture_used_for_evaluation': picture
    }
    return evaluated_example


if __name__ == "__main__":
    api_key = " " # Replace with your API key or use environment variables
    model_api = GeminiAPI(api_key, model_name="gemini-2.0-flash-thinking-exp-01-21", temperature=0, max_tokens=65536)

    results_dir = "../Results/gemini-2.0-flash" # Directory where result json files are located
    data_dir = "../Data" # Directory where original data json files are located

    model_name_prefix = os.path.basename(results_dir) # Dynamically get model name prefix

    for i in range(1, 12): # Loop through gemini-2.0-flash_1.json to gemini-2.0-flash_11.json
        result_json_file = f"{model_name_prefix}_{i}.json" # Use dynamically obtained prefix
        data_json_file = f"{i}.json" # Corresponding original data filename

        result_json_file_path = os.path.join(results_dir, result_json_file)
        data_json_file_path = os.path.join(data_dir, data_json_file)

        original_data_file_path = data_json_file_path # Dynamically set original_data_file_path

        print(f"Being evaluated: {result_json_file_path}") # Output current file being processed

        # Load corresponding original data file
        with open(original_data_file_path, 'r', encoding='utf-8') as f_original:
            original_data = json.load(f_original)
        original_data_dict = {item['index']: item for item in original_data['example']} # Create index to example mapping

        evaluate_reasoning_accuracy(model_api, result_json_file_path, result_json_file_path, original_data_dict) # Pass original_data_dict


    print("Evaluation of all documents complete!") # All files evaluated!
