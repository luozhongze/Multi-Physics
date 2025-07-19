# Physics-Bench

Physics-Bench: Towards Comprehensive Physical Reasoning Evaluation of Multimodal LLMs in Chinese Physics Problems
https://github.com/luozhongze/Physics-Bench/

## Statistics of Question Types

| Letters     | Question Types              | Number     | Average Question Length     | Average Analysis Length     |
| :-----: | :----------------: | :-----: | :-----: | :-----: |
| A       | Linear Motion      | 82       | 168.99       | 238.15       |
| B       | Interactions in Mechanics   | 155       | 201.05       | 218.69       |
| C       | Newton's Laws of Motion   | 110       | 201.33       | 234.85       |
| D       | Curvilinear Motion   | 164       | 203.45       | 237.64       |
| E       | Law of Universal Gravitation and Space Exploration   | 79       | 250.52       | 316.43       |
| F       | Mechanical Energy   | 108       | 218.66       | 274.52       |
| G       | Electrostatic Field   | 173       | 207.30       | 212.38       |
| H       | Constant Electric Current   | 122       | 183.20       | 215.63       |
| I       | Magnetic field   | 136       | 245.34       | 262.21       |
| J       | Electromagnetic induction   | 127       | 197.37       | 195.15       |
| K       | Alternating current   | 156       | 200.90       | 270.12       |
| **All**       | **Physics-Bench**   | **1412**       | **206.75**       | **239.74**       |

## The comparison with other existing benchmarks

| Benchmark       | Size   | Avg. Q. Leng. | Average Analysis Length     | Expl. | Question     | Lang.  |
| --------------- | ------ | ------------- | ------------- | ----- | ------------ | ------ |
| Ai2D            | 5K     | 9.78          | None | ✗     | MC           | Eng.   |
| FigureQA        | >1M    | 6.07          | None | ✗     | BC           | Eng.   |
| ScienceQA       | 6K     | 12.11         | None | ✗     | MC           | Eng.   |
| MMU             | 11.5K  | 59.23         | None | ✓     | MC+Open      | Eng.   |
| MM-Bench-CN     | 3K     | 15.48         | None | ✗     | MC           | T. Chi |
| GAOKAO-MM       | 0.65K  | 260.19        | None | ✓     | MC           | N. Chi |
| **Physics-Bench**      | **1.41K**  | **206.75**        | **239.74** | **✓**     | **MC**           | **N. Chi** |

## Evaluation results

Closed-source LMMs:

| Model             | Overall   | A     | B     | C     | D     | E     | F     | G     | H     | I     | J     | K     |
| --------------------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| yi-vision-v2 (20250107) | 0.166 | 0.14 | 0.116 | 0.177 | 0.201 | 0.177 | 0.204 | 0.116  | 0.238 | 0.202 | 0.177  | 0.115 |
| claude-3-5-sonnet (20241022) | 0.318 | 0.348 | 0.268 | 0.35 | 0.338 | 0.449 | 0.37 | 0.249  | 0.389 | 0.283 | 0.291  | 0.276 |
| moonshot-v1-128k-vision-preview (20250115) | 0.328 | 0.262 | 0.239 | 0.332 | 0.317 | 0.519 | 0.421 | 0.28  | 0.393 | 0.294 | 0.295  | 0.353 |
| o4-mini-2025-04-16  | 0.292 | 0.268 | 0.242 | 0.309 | 0.348 | 0.348 | 0.292 | 0.199  | 0.361 | 0.324 | 0.276  | 0.288 |
| gpt-4.1-2025-04-14  | 0.354 | 0.329 | 0.216 | 0.373 | 0.387 | 0.399 | 0.398 | 0.361  | 0.447 | 0.335 | 0.358  | 0.34 |
| ChatGPT-4o-latest (20250718)  | 0.365 | 0.311 | 0.29 | 0.341 | 0.372 | 0.411 | 0.403 | 0.353  | 0.463 | 0.404 | 0.331  | 0.362 |
| claude-4-sonnet-20250522 | 0.498 | 0.396 | 0.458 | 0.518 | 0.579 | 0.665 | 0.556 | 0.416  | 0.525 | 0.412 | 0.48  | 0.529 |
| qwen-vl-max-2025-04-08      | 0.575 | 0.549 | 0.552 | 0.6 | 0.585 | 0.791 | 0.667 | 0.462  | 0.561 | 0.5 | 0.555  | 0.628 |
| qvq-max-2025-05-15      | 0.613 | 0.622 | 0.519 | 0.682 | 0.662 | 0.741 | 0.699 | 0.529  | 0.656 | 0.533 | 0.622  | 0.599 |
| gemini-2.5-flash (20250617) | 0.716 | 0.744 | 0.752 | 0.755 | 0.759 | 0.88 | 0.824 | 0.72  | 0.73 | 0.566 | 0.591  | 0.651 |
| gemini-2.5-pro (20250617) | 0.784 | 0.726 | 0.758 | 0.845 | 0.79 | 0.93 | 0.926 | 0.818  | 0.758 | 0.706 | 0.736  | 0.712 |

Open-source LMMs:

| Model             | Overall   | A     | B     | C     | D     | E     | F     | G     | H     | I     | J     | K     |
| --------------------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| glm-4v-9b (20240605) | 0.204 | 0.195 | 0.206 | 0.214 | 0.226 | 0.184 | 0.213 | 0.199  | 0.193 | 0.176 | 0.256  | 0.173 |
| mistral-small-3.2-24b-instruct-2506 (20250620) | 0.207 | 0.232 | 0.165 | 0.232 | 0.198 | 0.177 | 0.199 | 0.173  | 0.324 | 0.217 | 0.169  | 0.218 |
| gemma-3-27b-it  (20250312) | 0.236 | 0.256 | 0.19 | 0.03 | 0.253 | 0.297 | 0.301 | 0.165  | 0.242 | 0.279 | 0.173  | 0.218 |
| internvl3-14b (20250411) | 0.39 | 0.372 | 0.352 | 0.409 | 0.402 | 0.544 | 0.458 | 0.303  | 0.48 | 0.357 | 0.335  | 0.385 |
| llama-4-scout-17b-16e-instruct (20250405)  | 0.404 | 0.311 | 0.352 | 0.418 | 0.43 | 0.538 | 0.519 | 0.364  | 0.426 | 0.364 | 0.335  | 0.439 |
| glm-4.1v-9b-thinking (20250702)  | 0.507 | 0.47 | 0.423 | 0.577 | 0.561 | 0.696 | 0.597 | 0.512  | 0.578 | 0.357 | 0.37  | 0.532 |
| llama-4-maverick-17b-128e-instruct (20250405) | 0.61 | 0.518 | 0.606 | 0.668 | 0.695 | 0.759 | 0.718 | 0.506  | 0.566 | 0.478 | 0.618  | 0.641 |

Evaluation results (Evaluation with CoT (Average Step Accuracy/Average Step Count))


## Method

### Different Model API

#### 1. Generate Answers

You can directly use the following command to invoke `Different Model API` for evaluation, and the generated results will be saved in `./Results/your model name`, please fill in `your api key` in the code file before doing so:

```bash
cd ./Bench
python choice_bench_model.py
```

#### 2. Calculate the Accuracy Rate

You can directly use the following command to calculate the accuracy rate of the answers generated by `Different Model API`, with the results saved in `./Results/your model name`:

```bash
python OBJ_score_evaluation.py --obj_output_dir=../Results/your model name
```

### Other Models

You can deploy other models for evaluation and store them in `./Models`. For specific methods, please refer to `./Models/glm.py`, please note that the environment needs to be configured as required when evaluating the model.

## Acknowledgements

The dataset was completed by many volunteers (Junhao Wu, Ya Gao, Yang Yu, Yuxi Sun, Mingxin Song, Yanzhe Fan, Peng Yang, Shuangtong Zhu, Zhongyang Cao, Qiwei Song, Zhongze Luo, Mingqi Shao, Jiaming Tian, and Yuting Song). Special thanks for their hard work.
