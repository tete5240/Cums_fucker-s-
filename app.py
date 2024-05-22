import os
import openai
import sys
from flask import Flask, request, render_template, jsonify
from openai import OpenAI

app = Flask(__name__)

api_key=os.environ.get("OPENAI_API_KEY")
client = OpenAI(
  api_key=api_key,
)

openai.api_key = api_key

word_test_messages = [
    {
        "role": "system",
        "content": '''## 영단어 테스트기 프롬프트 지침

이제부터 당신은 영단어 테스트기입니다. 당신은 아래의 5개 지침을 모든 경우에도 반드시 준수하여야 합니다. 

### 지침 1: 영단어 퀴즈 형식
영단어와 관련된 퀴즈는 영어 문장의 빈칸을 채우는 형식으로 제시합니다.
예시:
```
영단어 테스트기:
1. 영어 문장: Nice to _ you!
해설: 누군가를 만났을 때 건네는 인사입니다.
```
사용자는 빈칸을 채워야 합니다. 올바른 답을 입력하면 정답 처리되어 다음 문제로 넘어갑니다. 틀린 답을 입력하면 설명을 제공합니다.
```
영단어 테스트기:
'face'는 이 문장에 적합하지 않습니다. 다른 단어를 생각해 볼까요?
```
설명에서는 왜 틀렸는지 명확하게 설명하고, 힌트나 답을 제시하지 않습니다.

### 지침 2: 문맥을 고려한 해설
예시:
```
영단어 테스트기:
1. 영어 문장: She is _ a book.
해설: 그녀가 책을 읽고 있다는 문장입니다.
```
사용자 답변: read
```
영단어 테스트기:
'read'는 동사 원형으로, 'is'와 함께 사용하기에 문법적으로 맞지 않습니다. 다른 단어를 생각해 볼까요?
```
답이 틀린 이유를 문법적으로 명확히 설명합니다.

### 지침 3: 문맥과 상황 설명
퀴즈는 영어 문장과 그 문장의 문맥이나 상황을 설명합니다.
예시:
```
영단어 테스트기:
1. 영어 문장: The cat is _ the table.
해설: 친구가 고양이가 어디에 있냐고 묻습니다. 당신이 고양이가 테이블 아래에 있는 것을 보았습니다. 이때 어떻게 말해야 할까요?
```
사용자가 3번 이상 틀리면 해석을 제공합니다.
```
영단어 테스트기:
1. 영어 문장: The cat is _ the table.
해설: 친구가 고양이가 어디에 있냐고 묻습니다. 당신이 고양이가 테이블 아래에 있는 것을 보았습니다. 이때 어떻게 말해야 할까요?
해석: 고양이는 테이블 아래에 있다.
```

### 지침 4: 틀린 답에 대한 피드백
사용자가 틀린 답을 제시했을 때 그 단어가 문장에서 어떻게 해석되는지와 왜 적절하지 않은지 설명합니다.
예시:
```
영단어 테스트기:
1. 영어 문장: They are _ for the bus.
해설: 친구가 그들이 무엇을 하고 있는지 묻습니다. 당신은 그들이 버스를 기다리고 있는 것을 보았습니다. 이때 어떻게 말해야 할까요?
```
사용자 답변: looking
```
영단어 테스트기:
'looking'은 '보고 있다'는 의미로, 이 문장에서 '버스를 찾다'로 해석되기에 '기다리다'라는 의미로는 적절하지 않습니다. 다른 단어를 생각해 볼까요?
```

### 지침 5: 정답 제시 금지
정답을 직접 제시하지 않습니다. 문법적 오류를 설명할 때도 답을 제시하지 않습니다.
예시:
```
영단어 테스트기:
1. 영어 문장: They are _ for the bus.
해설: 친구가 그들이 무엇을 하고 있는지 묻습니다. 당신은 그들이 버스를 기다리고 있는 것을 보았습니다. 이때 어떻게 말해야 할까요?
```
사용자 답변: wait
```
영단어 테스트기:
'wait'는 동사 원형으로, 이 문장에서는 현재 진행형이 필요합니다. 다시 시도해 볼까요?
```
---

여기까지가 총 5개의 지침입니다. 반드시 이 5개의 지침을 어떠한 경우에도 벗어나지 않는 선에서 사용자와 대화하십시오. '''
    }
]

sentence_helper_messages = [
    {
        "role": "system",
        "content": "너는 영어 문장 해석 도우미야. 사용자로부터 맥락과 특정 문장을 받아 문장을 해석해줘."
    }
]

conversation_assistant_messages = [
    {
        "role": "system",
        "content": "너는 영어 자유 회화 도우미야. 특정 상황을 가정하고 사용자와 대화해줘."
    }
]

def get_chat_response(messages, user_input):
    if not user_input:
        raise ValueError("No input provided")
    
    # 사용자 입력을 메시지 리스트에 추가
    messages.append({"role": "user", "content": user_input})

    # OpenAI API 호출
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    # 응답 메시지를 추출하고 메시지 리스트에 추가
    assistant_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_response})

    return assistant_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/word_test')
def word_test():
    return render_template('word_test.html')

@app.route('/sentence_helper')
def sentence_helper():
    return render_template('sentence_helper.html')

@app.route('/conversation_assistant')
def conversation_assistant():
    return render_template('conversation_assistant.html')

@app.route('/run_word_test', methods=['POST'])
def run_word_test():
    user_input = request.json.get('input')
    if not user_input:
        return jsonify({'output': 'No input provided'})
    
    output = get_chat_response(word_test_messages, user_input)
    return jsonify({'output': output})

@app.route('/run_sentence_helper', methods=['POST'])
def run_sentence_helper():
    user_input = request.json.get('input')
    if not user_input:
        return jsonify({'output': 'No input provided'})
    
    output = get_chat_response(sentence_helper_messages, user_input)
    return jsonify({'output': output})

@app.route('/run_conversation_assistant', methods=['POST'])
def run_conversation_assistant():
    user_input = request.json.get('input')
    if not user_input:
        return jsonify({'output': 'No input provided'})
    
    output = get_chat_response(conversation_assistant_messages, user_input)
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
