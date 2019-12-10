A bert powered bot help you identify users.

## Overview

The goal of this project is to identify users who publish messages with the "SunXiaoChuan" pattern.

## Background

Nov 2019, a new wave of troll army named of "Sunxiaochuan 258" had reached twitter chinese users. Where they came from, how they organized and their background are unknown. However, they have very similar language behavior. It was a great opportunity to learn how to use NLP with Deep Learning to identify them.

## Training Dataset

20,000 tweets from "Sun XiaoChuan" and their followers network.
20,000 tweets from normal twitter users.

The crawler scripts is tools/fetch.py and tools/tweets.py

## Fine-Tuning the language model

* BERT-Base, Chinese 
* Chinese-BERT-wwm

## Results

* BERT-Base, Chinese 82.4%
* Chinese-BERT-wwm 83.6% 

## Result samples

Sunxiaochuan positive : result_samples/positive

 | Result | Name |
 | :----- | :--- |
 | 74.32% | linglala1 |
 | 75.34% | MinatoNaim |
 | 76.19% | lalala3796 |
 | 81.08% | makoaaaag |
 | 100% | Razorhott |
 | 100% | xianjizhe1 |

Sunxiaochuan negatives : result_samples/negative

 | Result | Name |
 | :----- | :--- |
 | 6.34% | StarKnight |
 | 5.26% | hawking197428 |
 | 4.03% | rijingzhongwen |
 | 5.55% | recatm |
 | 3.7% | HectorPlumber |
 | 24.48% | mranti |

## How to use

* Clone this repository
* Download the fine-turned model: https://drive.google.com/uc?id=1DcvRmZceOewUiY-7gsqKuYQzn_xUHShN&export=download and Unpack to the directory model
* pip install -r requirements.txt or  pip install -r requirements-gpu.txt
* cp config.json.sample config.json
* python server.py
* Open a web browser, open http://127.0.0.1:5200 for webui.
* API: http://localhost:5002/api/iden?screen_name=a_screen_name 


## Dependencies 

 | Dependency  | License |
 | :------------- | :------------- |
 | [github.com/tensorflow/tensorflow](https://github.com/tensorflow/tensorflow) |  Apache-2.0 |
 | [github.com/google-research/bert](https://github.com/google-research/bert) | Apache-2.0 |
 | [github.com/ymcui/Chinese-BERT-wwm](https://github.com/ymcui/Chinese-BERT-wwm) | Apache-2.0 |
