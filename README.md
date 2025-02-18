# Physics-MM

Physics-MM: A Chinese Benchmark for Evaluating Multimodal Large Language Models in Physics Problems
![https://github.com/luozhongze/Physics-MM/]

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
| **All**       | **Physics-MM**   | **1412**       | **206.75**       | **239.74**       |

## The comparison with other existing benchmarks

| Benchmark       | Size   | Avg. Q. Leng. | Average Analysis Length     | Expl. | Question     | Lang.  |
| --------------- | ------ | ------------- | ------------- | ----- | ------------ | ------ |
| Ai2D            | 5K     | 9.78          | None | ✗     | MC           | Eng.   |
| FigureQA        | >1M    | 6.07          | None | ✗     | BC           | Eng.   |
| ScienceQA       | 6K     | 12.11         | None | ✗     | MC           | Eng.   |
| MMU             | 11.5K  | 59.23         | None | ✓     | MC+Open      | Eng.   |
| MM-Bench-CN     | 3K     | 15.48         | None | ✗     | MC           | T. Chi |
| GAOKAO-MM       | 0.65K  | 260.19        | None | ✓     | MC           | N. Chi |
| Physics-MM      | 1.41K  | 206.75        | 239.74 | ✓     | MC           | N. Chi |

## Evaluation results

| Model              | Acc   | A     | B     | C     | D     | E     | F     | G     | H     | I     | J     | K     |
| ------------------ | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| gemini-2.0-flash   | 0.516 | 0.506 | 0.419 | 0.564 | 0.555 | 0.703 | 0.62  | 0.425 | 0.57  | 0.5   | 0.488 | 0.474 |
| gemini-2.0-pro-exp        | 0.572 | 0.561 | 0.516 | 0.582 | 0.625 | 0.785 | 0.639 | 0.488  | 0.635 | 0.526 | 0.52  | 0.542 |
| qwen-vl-max        | 0.524 | 0.378 | 0.481 | 0.582 | 0.521 | 0.797 | 0.681 | 0.39  | 0.574 | 0.485 | 0.48  | 0.542 |

## Acknowledgements

The dataset was completed by many volunteers (Junhao Wu, Ya Gao, Yang Yu, Yuxi Sun, Mingxin Song, Yanzhe Fan, Peng Yang, Shuangtong Zhu, Zhongyang Cao, Qiwei Song, Zhongze Luo, Mingqi Shao, Jiaming Tian, and Yuting Song). Special thanks for their hard work.
