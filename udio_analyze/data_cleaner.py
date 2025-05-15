import pandas as pd
import re
import string
import os
import nltk
from nltk.corpus import words, stopwords

def download_nltk_resources():
    """下载必要的NLTK资源"""
    try:
        nltk.download('words', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("NLTK资源下载完成")
    except Exception as e:
        print(f"NLTK资源下载失败: {e}")
        print("继续使用简单的英文过滤方法")

def clean_text(text):
    """清洗文本，只保留英语词汇"""
    if not isinstance(text, str):
        return ""
    
    # 转为小写
    text = text.lower()
    
    # 移除标点符号
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 分词
    words_list = text.split()
    
    # 尝试使用NLTK过滤非英语词汇
    try:
        english_words = set(words.words())
        # 保留英语词汇和短词(可能是缩写或音乐术语)
        english_only = [word for word in words_list if word.lower() in english_words or len(word) <= 2]
    except:
        # 如果NLTK资源加载失败，使用简单的过滤方法
        # 这里只是简单地过滤掉明显的非英文字符
        english_only = [word for word in words_list if all(c.isalpha() or c.isspace() for c in word)]
    
    return ' '.join(english_only)

def clean_data(input_file, output_file=None):
    """清洗Excel文件数据"""
    print(f"正在读取文件: {input_file}")
    
    try:
        # 读取Excel文件
        df = pd.read_excel(input_file)
        
        print(f"文件读取成功，共 {len(df)} 行数据")
        print(f"列名: {', '.join(df.columns)}")
        
        # 清洗prompt列
        if 'prompt' in df.columns:
            print("正在清洗prompt列...")
            df['cleaned_prompt'] = df['prompt'].apply(clean_text)
            print(f"prompt列清洗完成，有效数据 {df['cleaned_prompt'].str.len().gt(0).sum()} 行")
        
        # 清洗tags列
        if 'tags' in df.columns:
            print("正在清洗tags列...")
            df['cleaned_tags'] = df['tags'].apply(clean_text)
            print(f"tags列清洗完成，有效数据 {df['cleaned_tags'].str.len().gt(0).sum()} 行")
        
        # 保存清洗后的数据
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_cleaned.xlsx"
        
        df.to_excel(output_file, index=False)
        print(f"清洗后的数据已保存到: {output_file}")
        
        return df, output_file
    
    except Exception as e:
        print(f"数据清洗过程中出错: {e}")
        return None, None

if __name__ == "__main__":
    # 测试函数
    input_file = "F:\\ai_program_2\\udio_analyze\\music_prompt.xlsx"
    download_nltk_resources()
    clean_data(input_file) 