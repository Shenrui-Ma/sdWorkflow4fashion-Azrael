import requests
import json
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize
from nltk import pos_tag

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = '378c255bb73242fc'
# 您的应用密钥
APP_SECRET = 'oq3xZxjEVpUi2j5bFDHAyNEdvyqLUGdq'

def createRequest(q):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    # q = '蓝色的长裙，镶嵌着蓝色的宝石'
    lang_from = 'zh-CHS'
    lang_to = 'en'
    vocab_id = '83067295C87C4CE7BCCE95220644240E'

    data = {'q': q, 'from': lang_from, 'to': lang_to, 'vocabId': vocab_id}

    addAuthParams(APP_KEY, APP_SECRET, data)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # 修改变量名为headers以匹配requests库的参数名
    res = doCall('https://openapi.youdao.com/api', headers, data, 'post')
    
    # 解析响应
    response_data = json.loads(res.text)
    original_text = response_data.get('query', '')  # 获取原文本
    translation_result = response_data.get('translation', [''])[0]  # 获取翻译结果
    
    prompt = decorate(translation_result)
    
    print(f"原文本: {original_text}")
    print(f"翻译结果: {translation_result}")
    print(f"prompt: {prompt}")

def doCall(url, headers, params, method):
    if 'get' == method:
        return requests.get(url, params=params, headers=headers)
    elif 'post' == method:
        return requests.post(url, data=params, headers=headers)  # 修改参数名和参数传递方式以匹配requests库的要求
    
def decorate(s):
    to_del = {'I', 'want', 'you', 'to', 'me', 'a', 'an', 'draw'}
    words = word_tokenize(s)
    tagged_words = pos_tag(words)
    
    processed_words = []
    nouns = []  # 用于记录所有的名词
    for word, tag in tagged_words:
        if word not in to_del:
            if tag.startswith('NN'):
                nouns.append(word)
                processed_words.append(word)
                processed_words.append(',')  # 在名词后直接添加逗号
            else:
                processed_words.append(word)
    
    # 遍历记录的名词，将每个名词插入到上一个逗号之后
    for noun in nouns:
        # 找到第一个逗号的位置
        first_comma_index = next((i for i, word in enumerate(processed_words) if ',' in word), -1)
        if first_comma_index != -1:
            # 如果有逗号，将名词插入到第一个逗号之后
            processed_words.insert(first_comma_index + 1, noun)
        else:
            # 如果没有逗号，将名词放在第一位
            processed_words.insert(0, noun)
    
    # 移除列表中所有的逗号，然后在每个名词后重新添加逗号
    processed_words = [word for word in processed_words if word != ',']
    for i, word in enumerate(processed_words[:-1]):  # 避免在列表最后一个元素后添加逗号
        if word in nouns:
            processed_words[i] = word + ','

    return ' '.join(processed_words).replace(' ,', ',')

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
if __name__ == '__main__':
    createRequest(q='我想要你给我画一件蓝色的长裙，镶嵌着蓝色的宝石')