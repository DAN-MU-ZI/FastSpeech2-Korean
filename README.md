# DAN-MU-ZI/FastSpeech2-for-research

# CUDA 설치
인공지능환경에서 그래픽카드의 자원을 활용한다. 그래서 자원을 활용하기 위한 환경설정 중의 하나로 

# 1. conda 환경 설치  
파이썬 환경을 구축하기 위한 [다운로드 링크](https://github.com/DAN-MU-ZI/DAN-MU-ZI-FastSpeech2-for-research/tree/main/textgrid)  
설치후 재부팅을 해주고 윈도우(좌측 Ctrl의 우측에 위치하는 키) + r 키를 누른후 cmd입력하면 나타나는 창을 확인할 수 있다.  
 이를 `명령프롬프트` 창이라 하며 앞으로 `cmd`이라 한다.  
`cmd`에 아래의 명령을 실행한다.

1. conda에서 python 3.7 버전으로 가상환경 설치   
```
conda create --name fastsp2 python=3.7
```
만일 중간에 다른 문구가 나타난다면 엔터를 입력하여 그대로 진행한다.  

2. 가상환경 활성화
```
conda activate fastsp2
```
3. 패키지 설치
```
pip install -r requirements.txt
```
4. 예외 패키지 강제 설치
```
pip install g2pK --no-deps
```
아래 링크에서 cuda 환경에 맞는 명령어를 찾고 복사하여 앞의 과정에서 띄운 `명령프롬프트` 창에서 입력  
https://pytorch.org/get-started/locally/

## mecab설정
아래 링크는 환경에 맞게 설치해서 C드라이브에 압축풀기  
https://github.com/Pusnow/mecab-ko-dic-msvc/releases/tag/mecab-ko-dic-2.1.1-20180720-msvc-2   
이후 추가 패키지 설치위치를 찾기위해 `명령프롬프트` 창에서 아래 명령을 입력한다.  
```
cd %CONDA_PREFIX%
cd Lib\site-packages
```
입력하는 줄의 화살표 왼쪽부분에 경로가 바뀌었음을 볼 수 있고 이 경로를 `site-packages`폴더라고 한다.  

그리고 윈도우키를 누르고 `시스템 정보`라고 입력하면 시스템의 환경을 알 수 있는데  
여기서 `시스템 종류`를 보고 비트환경을 알 수 있다.  
`64비트`면 `x64로` 시작하고 `32비트`면 `x86`으로 시작한다.  

아래 링크에서 파일을 설치하는데 PC환경에 따라 해당하는 파일을 설치한다.     
https://github.com/Pusnow/mecab-python-msvc/releases/tag/mecab_python-0.996_ko_0.9.2_msvc-3  
1. `32비트` 버전 ``mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win32.whl``  
2. `64비트` 버전 ``mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64.whl``  
`시스템 정보`에서 확인한 환경에 맞는 버전을 아까의 `site-packages` 폴더에 저장하고 conda 환경에서 다음코드 실행

[설치방법]  
64비트 버전
```
pip install mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64.whl
```
32비트 버전
```
pip install mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win32.whl
```
## g2pK 수정
``site-packages`` 폴더에 ``g2pk``에 진입하고 ``g2pk.py`` 파일의 내용을 아래와 같이 수정
```
#9번째 줄을 다음과 같이 수정
#import mecab
from konlpy.tag import Mecab
#38번째줄을 다음과 같이 수정
#return mecab.MeCab()
return Mecab([mecab 설정에서 처음 링크의 mecab-ko-dic-msvc\mecab-ko-dic 경로])
```

# 2. 데이터 전처리
## 1) text alignment
TextGrid파일을 만들기 위해 [가이드라인](https://github.com/DAN-MU-ZI/DAN-MU-ZI-FastSpeech2-for-research/tree/main/textgrid)을 따른다.  

## 2) 파일정보 파일
내부 양식은 "파일명.wav" + "대사" 형태로이루어 져 있으며 자세한 사항은 아래와 같다.  
               ㄴ``'[folder_num]/[folder_num]_[filename].wav' : [content]  ``형식으로 ``.json``확장자로 저장한다.  
예시는 아래와 같다.  
예) 파일명 : 1/1_Test_001.wav  
대사 : 케이비에스 쿨 에프엠 유인나의 볼륨을 높여요  
~  
파일명 : 1/1_Test_010.wav  
대사 : 어 미안해라 진짜 이렇게 이렇게 못 참아서 어떡해요
```
{
  "1/1_Test_001.wav": "케이비에스 쿨 에프엠 유인나의 볼륨을 높여요",

  ~

  "1/1_Test_010.wav": "어 미안해라 진짜 이렇게 이렇게 못 참아서 어떡해요",
}
```
## 3) 환경설정
데이터 세트의 이름이 바뀔때마다 압축해제한 폴더에 `hparams.py`를 수정해야하며 예시는 아래와 같다.  
수정 전
```
dataset = "kss"
meta_name = "transcript.v.1.4.txt"
```
수정 후
```
dataset = "jaehun" 
meta_name = "jaehun.json"
```
`dataset`은 `.wav`파일을 모아놓을 폴더의 이름이며
`meta_name`은 파일들의 내용을 정규화한 양식이며 2번과정의 파일이다.
## 4) 파일배치
전처리한 데이터는 아래와 같은 구조로 데이터를 배치해야한다. 기준은 압축해제한 폴더 기준이다.  

    .
    |-- train.py
    |-- dataset
        |-- [hparams.dataset].json
        |-- [hparams.dataset]
            |-- 1
                |-- 1_[filename].wav
                |-- 1_[filename].wav
                .
                .
            |-- 2
                |-- 2_[filename].wav
                |-- 2_[filename].wav
                .
                .
    |-- TextGrid.zip
``hparams.py`` 파일의 내용을 데이터셋에 맞게 변경
```
dataset = '[데이터셋 이름]'
meta_name = '[데이터셋 이름].json'
```
배치한 이후 아래 명령어 실행
```
python preprocess.py
```

# 3. 학습
## 1) Vocoder 설치
모델 학습 전 사전학습된 vocoder 모델을 [다운로드](https://drive.google.com/file/d/1GxaLlTrEhq0aXFvd_X1f4b-ev7-FH8RB/view)하여 ``vocoder/pretrained_models/`` 경로에 배치하고 ``hparams.py`` 의 74번째 줄 ``vocoder_pretrained_model_name``변수에 다운받은 파일의 이름으로 변경

```
# hparams.py 74번째 줄
vocoder_pretrained_model_name = "checkpoint_f93129e_5840.pt"
```
## 2) 모델학습
``train.py`` 파일을 실행하여 학습을 진행하고 이전에 학습한 내용이 있다면 ``--restore_step`` 옵션 사용(chpt폴더에서 횟수를 확인할 수 있다)
```
python train.py --restore_step [step]
```

## 3) Pretrained model
``checkpoint_460000.pth.tar`` 파일과 같이 ``.pth.tar``확장자로 되어있는 사전학습 파일을 ``hparams.py``에 있는 ``checkpoint_path`` 변수에 기록된 경로에 위치시켜주면 사전학습된 모델을 사용할 수 있다.

## 4) 추론
`synthesis.py`파일로 학습된 파라미터를 기반으로 음성을 생성할 수 있다.  
`hparams.py` 이전단계의 환경설정에서 했던 `dataset`변수의 저장된 학습을 따라가므로 유의할것
```
python synthesis.py --step [step]
```
합성된 음성은 `results` 폴더에서 확인할 수 있다.