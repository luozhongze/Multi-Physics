import os
import json
import time
import re
import codecs

from tqdm import  tqdm

def extract_choice_answer(model_output, question_type, answer_lenth=None):

    if question_type == 'single_choice':
        model_answer = []
        temp = re.findall(r'[A-D]', model_output[::-1])
        if len(temp) != 0:
            model_answer.append(temp[0])

    elif question_type == 'multi_choice':
        model_answer = []
        answer = ''
        content = re.sub(r'\s+', '', model_output)
        answer_index = content.find('【答案】')
        if answer_index == -1: 
            answer_index = content.find('**答案**') 

        if answer_index != -1:
            temp = content[answer_index:]
            if len(re.findall(r'[A-D]', temp)) > 0:
                answer = "".join(re.findall(r'[A-D]', temp)) 
        else: 
            temp = content[-10:]
            if len(re.findall(r'[A-D]', temp)) > 0:
                answer = "".join(re.findall(r'[A-D]', temp)) 

        if len(answer) != 0:
            model_answer.append(answer)

    return model_answer

def choice_test(**kwargs):

    model_api = kwargs['model_api']
    model_name = kwargs['model_name']
    
    data = kwargs['data']['example']
    keyword = kwargs['keyword']
    prompt = kwargs['prompt']
    question_type = kwargs['question_type']
    
    save_dir = f'../Results/{model_name}'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_file = os.path.join(save_dir, f'{model_name}_{keyword}.json')

    if os.path.exists(save_file):
        with open(save_file, 'r', encoding='utf-8') as f:
            model_answer_dict = json.load(f)['example']
    else:
        model_answer_dict = []


    for i in tqdm(range(len(data))):
        if model_answer_dict != [] and i <= model_answer_dict[-1]['index']:
            continue

        index = data[i]['index']
        question = data[i]['question'].strip() + '\n'
        category = data[i]['category']
        standard_answer = data[i]['answer']
        answer_lenth = len(standard_answer)
        analysis = data[i]['analysis']

        model_output = model_api(prompt, question)
        model_answer = extract_choice_answer(model_output, question_type, answer_lenth)

        dict = {
            'index': index, 
            'category': category,
            'question': question, 
            'standard_answer': standard_answer,
            'analysis': analysis,
            'model_answer': model_answer,
            'model_output': model_output
        }
        model_answer_dict.append(dict)

        time.sleep(1)

        with codecs.open(save_file, 'w+', 'utf-8') as f:
            output = {
                'keyword': keyword, 
                'model_name': model_name,
                'prompt': prompt,
                'example' : model_answer_dict
                }
            json.dump(output, f, ensure_ascii=False, indent=4)
            f.close()


def export_distribute_json(
        model_api,
        model_name: str, 
        directory: str, 
        keyword: str, 
        zero_shot_prompt_text: str, 
        question_type: str
    ) -> None:

    for root, _, files in os.walk(directory):
        for file in files:
            if file == f'{keyword}.json':
                filepath = os.path.join(root, file)
                with codecs.open(filepath, 'r', 'utf-8') as f:
                    data = json.load(f)
        
    
    kwargs = {
        'model_api': model_api,
        'model_name': model_name, 
        'data': data, 
        'keyword': keyword, 
        'prompt': zero_shot_prompt_text, 
        'question_type': question_type
    }
    
    if question_type in ["single_choice", "multi_choice"]:
            choice_test(**kwargs)