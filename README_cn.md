A bert powered bot help you identify users.

## Overview

这个项目的目标是通过用户发布的文本信息，寻找“孙笑川”的模式。

## Background

2019年11月，一大堆疑似troll的中文帐号开始在twitter活跃，他们都使用类似“孙笑川258”之类的名字。我不知道他们的背景，也不知道他们从哪来，如何组织，但是他们的语言模式看起来非常相似。这给了我一个很好的实验深度学习和自然语言处理的学习实验环境。

## Training Dataset

20,000 条推文，来自”孙笑川“以及他们的follower
20,000 条推文，来自普通正常用户。

抓取脚本在 tools/fetch.py and tools/tweets.py

## Fine-Tuning the language model

* BERT-Base, Chinese 
* Chinese-BERT-wwm

## Results

* BERT-Base, Chinese 82.4%
* Chinese-BERT-wwm 83.6% 

## How to use

* Clone this repository
* 下载模型数据: https://drive.google.com/file/d/1DcvRmZceOewUiY-7gsqKuYQzn_xUHShN/view?usp=sharing 解压到model目录
* pip install -r requirements.txt or  pip install -r requirements-gpu.txt
* cp config.json.sample config.json
* python server.py
* 打开浏览器，访问 http://127.0.0.1:5002 使用简单的web界面
* 使用API: http://localhost:5002/api/iden?screen_name=a_screen_name 

## Result samples

疑似孙笑川样例: result_samples/positive

 | Result | Name |
 | :----- | :--- |
 | 74.32% | linglala1 |
 | 75.34% | MinatoNaim |
 | 76.19% | lalala3796 |
 | 81.08% | makoaaaag |
 | 100% | Razorhott |
 | 100% | xianjizhe1 |

非孙笑川样例 : result_samples/negative

 | Result | Name |
 | :----- | :--- |
 | 6.34% | StarKnight |
 | 5.26% | hawking197428 |
 | 4.03% | rijingzhongwen |
 | 5.55% | recatm |
 | 3.7% | HectorPlumber |
 | 24.48% | mranti |

## FAQ 常见问题

* 为什么要做它？因为在学习NLP/AI相关技术。合适的数据集不好找，twitter的长度有限制，非常适合使用。”孙笑川“们的特征创造了一个相当理想的数据集。
* 这个结果准确吗？不一定准确，一切数值都是仅供参考。我使用的测试数据集显示准确率大约是83%，所以肯定会有大量误判
* 还能提高吗？ 能。我目前使用的数据集比较粗糙，如果有更好的预处理会有更好的准确度。以及一些推文（比如互相打招呼问好）在两类用户中都有出现，这些数据我没有精力一一筛选去掉。
* 只支持简体中文吗？支持繁体和简体中文，也可以处理包含emoji的内容。但是目前英文内容处理不正确。


## Dependencies 

 | Dependency  | License |
 | :------------- | :------------- |
 | [github.com/tensorflow/tensorflow](https://github.com/tensorflow/tensorflow) |  Apache-2.0 |
 | [github.com/google-research/bert](https://github.com/google-research/bert) | Apache-2.0 |
 | [github.com/ymcui/Chinese-BERT-wwm](https://github.com/ymcui/Chinese-BERT-wwm) | Apache-2.0 |
