## This script is used to evaluate the accuracy of the model output in the form of json file.
import json
import os
from statistics import mean
import codecs
import argparse


score_dict = {
        "model_name": None,
        "correct_question_num": 0.0,
        "question_num": 1412,
        "accuracy": 0.0,
        'subject':{
            '1': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 82,
                'type': 
                {
                    '1': {'correct_question_num': 0.0, 'question_num': 82, 'accuracy': 0.0},
                }
            },
            '2': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 155,
                'type': 
                {
                    '2': {'correct_question_num': 0.0, 'question_num': 155, 'accuracy': 0.0},
                }
            },
            '3': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 110,
                'type': 
                {
                    '3': {'correct_question_num': 0.0, 'question_num': 110, 'accuracy': 0.0},
                }
            },
            '4': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 164,
                'type': 
                {
                    '4': {'correct_question_num': 0.0, 'question_num': 164, 'accuracy': 0.0},
                }
            },
            '5': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 79,
                'type': 
                {
                    '5': {'correct_question_num': 0.0, 'question_num': 79, 'accuracy': 0.0},
                }
            },
            '6': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 108,
                'type': 
                {
                    '6': {'correct_question_num': 0.0, 'question_num': 108, 'accuracy': 0.0},
                }
            },
            '7': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 173,
                'type': 
                {
                    '7': {'correct_question_num': 0.0, 'question_num': 173, 'accuracy': 0.0},
                }
            },
            '8': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 122,
                'type': 
                {
                    '8': {'correct_question_num': 0.0, 'question_num': 122, 'accuracy': 0.0},
                }
            },
            '9': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 136,
                'type':
                {
                    '9': {'correct_question_num': 0.0, 'question_num': 136, 'accuracy': 0.0},
                }
            },
            '10': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 127,
                'type':
                {
                    '10': {'correct_question_num': 0.0, 'question_num': 127, 'accuracy': 0.0},
                }
            },
            '11': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 156,
                'type': 
                {
                    '11': {'correct_question_num': 0.0, 'question_num': 156, 'accuracy': 0.0},
                }
            }
        }
    }



def check_length_equal(item, filename):
    if len(item["model_answer"]) != len(item["standard_answer"]):
        print("model_answer and standard_answer length is not equal, filename:"+filename+"\tindex:"+str(item["index"]))
        item["model_answer"]=["Z"]*len(item["standard_answer"])


def obj_score_eval(obj_output_dir: str) -> None:

    obj_files = [os.path.join(obj_output_dir, file) for file in os.listdir(obj_output_dir) if file.endswith(".json") and file != 'correction_score.json']

    for file in obj_files:
        if "correction_score" in file:
            continue

        with codecs.open(file, "r", 'utf-8') as f:
            data = json.load(f)
            f.close()
        
        if 'keyword' in data.keys():
            keyword = data['keyword']
        else:
            keyword = data['keywords']
            
        model_name = data['model_name']

        score_dict['model_name'] = model_name


        c_q_num = 0.0
        ac = 0.0

        print(f"Calculating {keyword} {model_name} score")

        for key, value in score_dict['subject'].items():
            if keyword in value['type'].keys():
                break
        
        for item in data['example']:
            assert len(item['standard_answer']) == 1, "standard_answer length is not 1"
            check_length_equal(item, file)

            if keyword in ['1','2','3','4','5','6','7','8','9','10','11']:
                if item['model_answer'][0].lower() == item['standard_answer'][0].lower():
                    c_q_num += 1
                elif item['model_answer'][0].lower() in item['standard_answer'][0].lower():
                    c_q_num += 0.5

            else:
                if item['model_answer'][0].lower() == item['standard_answer'][0].lower():
                    c_q_num += 1


        score_dict['subject'][key]['type'][keyword]['correct_question_num'] = c_q_num
        ac = round(c_q_num / score_dict['subject'][key]['type'][keyword]['question_num'], 3)
        score_dict['subject'][key]['type'][keyword]['accuracy'] = ac

        score_dict['subject'][key]['correct_question_num'] += c_q_num
            

    c_q_num = 0.0

    for value in score_dict['subject'].values():
        value['accuracy'] = round(value['correct_question_num'] / value['question_num'], 3)
        c_q_num += value['correct_question_num']
    
    score_dict['correct_question_num'] = c_q_num
    score_dict['accuracy'] = round(c_q_num / score_dict['question_num'], 3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--obj_output_dir', type=str, default='../Results/gemini-2.0-flash')

    args = parser.parse_args()

    obj_output_dir = args.obj_output_dir

    obj_score_eval(obj_output_dir)
    with open(os.path.join(obj_output_dir, 'correction_score.json'), 'w+') as f:
        json.dump(score_dict, f, ensure_ascii=False, indent=4)