# -*- coding: utf-8 -*-
import json
import os
import codecs
import argparse
from collections import defaultdict

DATA_NEW_PATH = "../Data" 

def load_difficulty_data(data_path: str) -> dict:
    difficulty_lookup = {}
    print(f"Loading difficulty data from: {data_path}")
    if not os.path.exists(data_path):
        print(f"Error: Directory with difficulty data not found at '{data_path}'")
        return None

    rated_files = [f for f in os.listdir(data_path) if f.endswith(".json")]
    for filename in rated_files:
        filepath = os.path.join(data_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            difficulty_lookup[filename] = {
                item['index']: item.get('level', -1) 
                for item in data.get('example', [])
            }
    print("Difficulty data loaded successfully.")
    return difficulty_lookup

def check_length_equal(item, filename):
    if len(item["model_answer"]) != len(item["standard_answer"]):
        print(f"Warning: model_answer and standard_answer length is not equal. Filename: {filename}, Index: {item['index']}")
        item["model_answer"] = ["Z"] * len(item["standard_answer"])

def calculate_score_by_difficulty(obj_output_dir: str, difficulty_lookup: dict) -> dict:
    level_stats = defaultdict(lambda: {'total_score': 0.0, 'question_count': 0})
    model_name = "Unknown"

    result_files = [f for f in os.listdir(obj_output_dir) if f.endswith(".json") and 'score' not in f]

    for filename in result_files:
        filepath = os.path.join(obj_output_dir, filename)

        with codecs.open(filepath, "r", 'utf-8') as f:
            data = json.load(f)

        keyword = data.get('keyword') or data.get('keywords')
        data_filename = f"{keyword}.json"
        
        if data.get('model_name'):
            model_name = data['model_name']

        print(f"Processing results from: {filename}")

        if data_filename not in difficulty_lookup:
            print(f"Warning: No difficulty data found for '{data_filename}'. Skipping this file.")
            continue

        for item in data['example']:
            score = 0.0
            assert len(item['standard_answer']) == 1, "standard_answer length is not 1"
            check_length_equal(item, filename)

            model_ans = item['model_answer'][0].lower()
            std_ans = item['standard_answer'][0].lower()

            if model_ans == std_ans:
                score = 1.0
            elif keyword in ['1','2','3','4','5','6','7','8','9','10','11'] and model_ans in std_ans:
                 score = 0.5

            question_index = item['index']
            level = difficulty_lookup[data_filename].get(question_index, -1) 

            level_stats[level]['total_score'] += score
            level_stats[level]['question_count'] += 1

    final_report = {
        "model_name": model_name,
        "performance_by_difficulty": {}
    }

    print("\n--- Calculating Final Averages ---")
    for level, stats in sorted(level_stats.items()):
        count = stats['question_count']
        total_score = stats['total_score']
        
        if count > 0:
            average_score = round(total_score / count, 4)
        else:
            average_score = 0.0
        
        level_key = f"Level_{level}" if level != -1 else "Level_RatingFailed"
        
        final_report["performance_by_difficulty"][level_key] = {
            "total_questions": count,
            "total_score": total_score,
            "average_score": average_score
        }

    return final_report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluate model accuracy based on question difficulty.")
    parser.add_argument('--obj_output_dir', type=str, default='../Results/llama-4-maverick',
                        help="Directory containing the model's output JSON files.")
    
    args = parser.parse_args()
    obj_output_dir = args.obj_output_dir

    difficulty_lookup_data = load_difficulty_data(DATA_NEW_PATH)

    if difficulty_lookup_data:
        final_difficulty_report = calculate_score_by_difficulty(obj_output_dir, difficulty_lookup_data)

        print("\n" + "="*60)
        print(f"Difficulty-Based Performance Report for: {final_difficulty_report['model_name']}")
        print("="*60)
        for level, data in final_difficulty_report["performance_by_difficulty"].items():
            print(f"\n{level}:")
            print(f"  - Total Questions: {data['total_questions']}")
            print(f"  - Total Score:     {data['total_score']}")
            print(f"  - Average Score:   {data['average_score']:.2%}") 
        print("="*60)

        output_filename = os.path.join(obj_output_dir, 'difficulty_score.json')
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(final_difficulty_report, f, ensure_ascii=False, indent=4)
        print(f"\nDetailed report saved to: {output_filename}")
