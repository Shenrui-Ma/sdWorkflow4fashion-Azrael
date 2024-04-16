'''
python接受一段中文
翻译成英文
去掉冗余的词
'''

from googletrans import Translator

def translate_to_english(text):
    translator = Translator(service_urls=['translate.google.cn'])
    translation = translator.translate(text, dest='en')
    return translation.text

def remove_redundant_words(text):
    common_words = ['I', 'like', 'to', 'you']  # 定义要去掉的常见词
    cleaned_text = ' '.join([word for word in text.split() if word.lower() not in common_words])
    return cleaned_text

def process_text(text):
    translated_text = translate_to_english(text)
    cleaned_text = remove_redundant_words(translated_text)
    return cleaned_text

input_text = '我想要你做一件衣服'  # 输入中文文本
processed_text = process_text(input_text)
print(processed_text)
