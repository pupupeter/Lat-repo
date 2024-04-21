#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install transformers -U -q')


# In[2]:


get_ipython().system(' pip install sentencepiece')


# In[3]:


get_ipython().system('pip install transformers')


# In[4]:


from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


# In[10]:


from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
article_en = "The head of the United Nations says there is no military solution in Syria"
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")

model_inputs = tokenizer(article_en, return_tensors="pt")

generated_tokens = model.generate(
    **model_inputs,
    forced_bos_token_id=tokenizer.lang_code_to_id["zh_CN"]
)
tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)


# In[22]:


from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import gradio as gr
from PyPDF2 import PdfReader 

# 載入模型和 tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
tokenizer = AutoTokenizer.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")

# 定義提取 PDF 文本的函數
def extract_all_text_from_pdf(pdf_file):
    try:
        text = ""
        with open(pdf_file.name, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        return str(e)



# 定義 Gradio 介面
with gr.Blocks() as demo:
    # 顯示說明訊息
    gr.Markdown("上傳 PDF 檔案，並提取全部文字。")

    # 設定使用者上傳 PDF 的元件
    with gr.Tab("pdf"):
        with gr.Column():
            pdf_input = gr.File(label="上傳 PDF", type="filepath")
            pdf_output = gr.Textbox(placeholder="翻譯後的文字將顯示在這裡", label="翻譯")

    # 設定提取文字的按鈕
    pdf_button = gr.Button("翻譯")
    pdf_button.click(extract_all_text_from_pdf, inputs=pdf_input, outputs=pdf_output)

# 啟動 Gradio 介面
demo.launch()


# In[6]:


from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import gradio as gr
from PyPDF2 import PdfReader 

# 載入模型和 tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
tokenizer = AutoTokenizer.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")

# 定義提取 PDF 文本並翻譯的函數
def extract_and_translate_text_from_pdf(pdf_file):
    try:
        text = ""
        with open(pdf_file.name, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        # 翻譯提取的文本
        model_inputs = tokenizer(text, return_tensors="pt")
        generated_tokens = model.generate(
            **model_inputs,
            forced_bos_token_id=tokenizer.lang_code_to_id["zh_CN"]
        )
        translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return translated_text
    except Exception as e:
        return str(e)

# 定義 Gradio 介面
with gr.Blocks() as demo:
    # 顯示說明訊息
    gr.Markdown("上傳 PDF 檔案，並提取全部文字，然後進行翻譯。")

    # 設定使用者上傳 PDF 的元件
    with gr.Tab("pdf"):
        with gr.Column():
            pdf_input = gr.File(label="上傳 PDF", type="filepath")
            pdf_output = gr.Textbox(placeholder="翻譯後的文字將顯示在這裡", label="翻譯")

    # 設定提取文字並翻譯的按鈕
    pdf_button = gr.Button("提取並翻譯")
    pdf_button.click(extract_and_translate_text_from_pdf, inputs=pdf_input, outputs=pdf_output)

# 啟動 Gradio 介面
demo.launch()


# In[5]:


from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import gradio as gr
from PyPDF2 import PdfReader 

# 載入模型和 tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
tokenizer = AutoTokenizer.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")

# 定義提取 PDF 文本並翻譯的函數
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

# 定義 Gradio 介面
with gr.Blocks() as demo:
    # 顯示說明訊息
    gr.Markdown("上傳 PDF 檔案，並提取全部文字，然後進行翻譯。")

    # 設定使用者上傳 PDF 的元件
    with gr.Tab("pdf"):
        with gr.Column():
            pdf_input = gr.File(label="上傳 PDF", type="filepath")
            pdf_output = gr.Textbox(placeholder="翻譯後的文字將顯示在這裡", label="翻譯")

    # 設定提取文字並翻譯的按鈕
    pdf_button = gr.Button("提取並翻譯")
    pdf_button.click(extract_and_translate_text_from_pdf, inputs=pdf_input, outputs=pdf_output)

# 啟動 Gradio 介面
demo.launch()


# In[ ]:




