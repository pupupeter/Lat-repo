#!/usr/bin/env python
# coding: utf-8

# In[9]:


get_ipython().system('pip install gTTS')


# In[10]:


pip install -U gradio


# In[11]:


get_ipython().system(' pip install sentencepiece')


# In[12]:


get_ipython().system('pip install PyPDF2')


# In[13]:


get_ipython().system('pip install openai==0.28')


# In[14]:


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# In[19]:


import gradio as gr
import openai
from gtts import gTTS
from IPython.display import Audio
import os
from PyPDF2 import PdfReader 

openai.api_key = "你的api"
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
tokenizer = AutoTokenizer.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")


def translate_text(text, wordtype, target_language="Korean"):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"請直接給我對應的翻譯字，且不需要給我音譯音，使用 {target_language} 以 {wordtype} 執行: {text}\n",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()
def extract_and_translate_text_from_pdf(pdf_file, max_length=200):
    try:
        text = ""
        with open(pdf_file.name, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        
        # 分割文本以确保不超过模型的最大输入长度
        chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        
        # 翻譯提取的文本
        translated_text = ""
        for chunk in chunks:
            model_inputs = tokenizer(chunk, return_tensors="pt")
            generated_tokens = model.generate(
                **model_inputs,
                forced_bos_token_id=tokenizer.lang_code_to_id["zh_CN"]
            )
            translated_chunk = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            translated_text += translated_chunk + " "  # 在每段翻译结果之间加上空格
        
        return translated_text
    except Exception as e:
        return str(e)
examples = [
    ["晚安我要來睡覺了"],
    ["我想讓我的韓文變厲害"]
]

def remove_semilang(sentence):

    if sentence.endswith("하다"):
        return sentence[:-2] + "해"
    elif sentence.endswith("다"):
        return sentence[:-1]
    elif sentence.endswith("합니다"):
        return sentence[:-3]
    elif sentence.endswith("세요"):
        return sentence[:-2]
    elif sentence.endswith("하기"):
        return sentence[:-1] + "해"
    elif sentence.endswith("기"):
        return sentence[:-1]
    else:
        return sentence



def translate_text_half(sentence,verb, wordtype, target_language="Korean"):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"請直接給我對應的翻譯字，且不需要給我音譯音，使用 {target_language} 以 {wordtype} 執行: {text}\n",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    translated = response.choices[0].text.strip()

    return remove_semilang(translated)
def text_to_speech(text):
    language = "ko"
    gtts_object = gTTS(text=text, lang=language, slow=False)
    gtts_object.save("/content/gtts6.wav")
    return "/content/gtts6.wav"

def translate_text2(text, target_language="Japanese"):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"if I utilize a kind of language,please help me translate to Japanese:  {text}\n",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()
def translate_text3(text, target_language="Chinese"):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"if I utilize a kind of language,please help me translate to Tradionnal chinese,and do not give me the Hanyu Pinyin System:  {text}\n",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()
with gr.Blocks() as demo:
    gr.Markdown("翻譯成韓文，不然我真的會gg耶，拜託拜託")

    with gr.Tab("一般"):
        with gr.Column():
            text_input = gr.Textbox(label="請輸入文本")
            wordtype_input = gr.Radio(choices=["動詞", "名詞","形容詞"], label="請選擇詞類")
            text_output = gr.Textbox(label="翻譯結果")
            text_button = gr.Button("翻譯")

    with gr.Tab("半語"):
        with gr.Column():
            text_input1 = gr.Textbox(label="請輸入文本")
            wordtype_input1 = gr.Radio(choices=["動詞", "名詞","形容詞"], label="請選擇詞類")
            text_output1 = gr.Textbox(label="翻譯結果")
            text_button1 = gr.Button("翻譯")
    with gr.Tab("音檔"):
        with gr.Column():
            text_input2 = gr.Textbox(label="請輸入文本")
            text_output2 = gr.Audio(label="音檔")
            text_button2 = gr.Button("轉換")
    with gr.Tab("日文"):
        with gr.Column():
            text_input3 = gr.Textbox(label="請輸入文本")
            text_output3 = gr.Textbox(label="翻譯結果")
            text_button3 = gr.Button("翻譯")
    with gr.Tab("中文"):
        with gr.Column():
            text_input4 = gr.Textbox(label="請輸入文本")
            text_output4 = gr.Textbox(label="翻譯結果")
            text_button4 = gr.Button("翻譯")
    with gr.Tab("pdf的翻譯"):      
        with gr.Column():
            pdf_input = gr.File(label="上傳 PDF", type="filepath")
            pdf_output = gr.Textbox(placeholder="翻譯後的文字將顯示在這裡", label="翻譯")
    text_button.click(translate_text, inputs=[text_input, wordtype_input], outputs=text_output)
    text_button1.click(translate_text_half, inputs=[text_input1, wordtype_input1], outputs=text_output1)
    text_button2.click(text_to_speech, inputs=text_input2, outputs=text_output2)
    text_button3.click(translate_text2, inputs=text_input3, outputs=text_output3)
    text_button4.click(translate_text3, inputs=text_input4, outputs=text_output4)
    pdf_button = gr.Button("翻譯")
    pdf_button.click(extract_and_translate_text_from_pdf, inputs=pdf_input, outputs=pdf_output)
demo.launch(share=True)


# In[ ]:




