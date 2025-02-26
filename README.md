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
| yi-vision-v2  | 0.166 | 0.14 | 0.116 | 0.177 | 0.201 | 0.177 | 0.204 | 0.116  | 0.238 | 0.202 | 0.177  | 0.115 |
| grok-2-vision-1212  | 0.252 | 0.244 | 0.226 | 0.282 | 0.271 | 0.329 | 0.264 | 0.197  | 0.254 | 0.276 | 0.189  | 0.285 |
| ChatGPT-4o-latest (2025-01-29)  | 0.292 | 0.268 | 0.242 | 0.309 | 0.348 | 0.348 | 0.292 | 0.199  | 0.361 | 0.324 | 0.276  | 0.288 |
| claude-3-5-sonnet-20241022  | 0.318 | 0.348 | 0.268 | 0.35 | 0.338 | 0.449 | 0.37 | 0.249  | 0.389 | 0.283 | 0.291  | 0.276 |
| qwen-vl-max-2025-01-25      | 0.524 | 0.378 | 0.481 | 0.582 | 0.521 | 0.797 | 0.681 | 0.39  | 0.574 | 0.485 | 0.48  | 0.542 |
| gemini-2.0-flash-001        | 0.516 | 0.506 | 0.419 | 0.564 | 0.555 | 0.703 | 0.62  | 0.425 | 0.57  | 0.5   | 0.488 | 0.474 |
| gemini-2.0-flash-thinking-exp-01-21    | 0.55 | 0.585 | 0.494 | 0.591 | 0.61 | 0.684 | 0.727 | 0.523  | 0.557 | 0.434 | 0.445  | 0.519 |
| gemini-2.0-pro-exp-02-05    | 0.572 | 0.561 | 0.516 | 0.582 | 0.625 | 0.785 | 0.639 | 0.488  | 0.635 | 0.526 | 0.52  | 0.542 |

Open-source LMMs:

| Model             | Overall   | A     | B     | C     | D     | E     | F     | G     | H     | I     | J     | K     |
| --------------------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| GLM-4V-9B         | 0.204 | 0.195 | 0.206 | 0.214 | 0.226 | 0.184 | 0.213 | 0.199  | 0.193 | 0.176 | 0.256  | 0.173 |

## Evaluation with CoT (Average Step Accuracy/Average Step Count)

| Model             | Overall   | A     | B     | C     | D     | E     | F     | G     | H     | I     | J     | K     |
| --------------------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| yi-vision-v2  | 0.306/5.34 | 0.276/5.55 | 0.264/6.48 | 0.323/5.39 | 0.348/6.32 | 0.393/5.06 | 0.301/5.39 | 0.365/5.61  | 0.398/6.43 | 0.377/6.10 | 0.378/5.01  | 0.338/5.36 |
| grok-2-vision-1212  | 0.406/5.00 | 0.383/4.84 | 0.338/6.16 | 0.356/5.32 | 0.440/5.04 | 0.557/4.42 | 0.367/4.92 | 0.388/4.66  | 0.437/5.07 | 0.395/5.13| 0.399/4.46  | 0.447/4.62 |
| ChatGPT-4o-latest (2025-01-29)  | 0.485/4.44 | 0.416/4.35 | 0.408/4.81 | 0.481/4.61 | 0.528/4.66 | 0.625/4.01 | 0.455/4.35 | 0.428/4.39  | 0.496/4.48 | 0.483/4.16 | 0.550/4.20  | 0.504/4.46 |
| claude-3-5-sonnet-20241022  | 0.526/4.93 | 0.460/4.84 | 0.457/4.98 | 0.500/5.05 | 0.525/5.07 | 0.697/4.50 | 0.522/5.12 | 0.545/4.91 | 0.518/4.96 | 0.525/5.04 | 0.533/4.66 | 0.545/4.92 |
| qwen-vl-max-2025-01-25      | 0.588/4.50 | 0.479/4.44 | 0.506/4.80 | 0.596/4.40 | 0.613/4.53 | 0.832/4.23 | 0.664/4.58 | 0.545/4.35  | 0.639/4.81 | 0.516/4.48 | 0.591/4.15 | 0.590/4.54 |
| gemini-2.0-flash-001        | 0.600/6.40 | 0.581/5.27 | 0.513/6.17 | 0.626/7.18 | 0.626/8.21 | 0.756/4.36 | 0.653/7.67  | 0.522/7.20 | 0.654/5.70 | 0.561/5.66 | 0.583/6.60 | 0.631/5.06 |
| gemini-2.0-flash-thinking-exp-01-21    | 0.626/6.18 | 0.555/5.84 | 0.555/6.97 | 0.656/6.31 | 0.681/6.87 | 0.782/5.22 | 0.673/5.85 | 0.605/5.51  | 0.659/6.99 | 0.540/6.35 | 0.606/5.43  | 0.631/6.06 |
| gemini-2.0-pro-exp-02-05    | 0.621/5.05 | 0.609/4.98 | 0.567/5.35 | 0.605/5.02 | 0.668/4.89 | 0.814/4.29 | 0.652/4.84 | 0.573/4.79 | 0.660/5.23 | 0.572/5.47 | 0.593/4.65 | 0.609/5.62 |

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
