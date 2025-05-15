import pandas as pd
import os
import json

# 预定义分类词典
DEFAULT_CATEGORIES = {
    'music_genres': [
        'house', 'phonk', 'pop', 'rock', 'electronic', 'rap', 'jazz', 'classical', 
        'hip', 'hop', 'techno', 'trance', 'ambient', 'folk', 'country', 'rb', 'soul',
        'metal', 'punk', 'indie', 'edm', 'dubstep', 'trap', 'lofi', 'blues', 'disco',
        'reggae', 'funk', 'dance', 'electro', 'synth', 'bass', 'drum', 'instrumental',
        'orchestral', 'vocal', 'choir', 'acapella', 'acoustic', 'ballad', 'progressive',
        'alternative', 'experimental', 'psychedelic', 'industrial', 'grunge', 'hardcore',
        'house', 'techno', 'dnb', 'drill', 'grime', 'garage', 'tropical', 'latin', 'salsa',
        'bossa', 'nova', 'flamenco', 'opera'
    ],
    
    'music_emotions': [
        'happy', 'sad', 'energetic', 'calm', 'relaxing', 'upbeat', 'melancholic',
        'angry', 'peaceful', 'nostalgic', 'dramatic', 'romantic', 'epic', 'dark',
        'emotional', 'uplifting', 'dreamy', 'intense', 'joyful', 'atmospheric',
        'aggressive', 'mellow', 'soothing', 'exciting', 'passionate', 'haunting',
        'ethereal', 'groovy', 'hypnotic', 'inspiring', 'mysterious', 'sensual',
        'tender', 'triumphant', 'whimsical', 'bittersweet', 'cheerful', 'contemplative',
        'ecstatic', 'frantic', 'gloomy', 'hopeful', 'laid', 'back', 'majestic', 'melancholy',
        'moody', 'optimistic', 'playful', 'reflective', 'serene', 'somber', 'tense',
        'tranquil', 'vibrant', 'wistful'
    ],
    
    'narrative_elements': [
        'story', 'journey', 'adventure', 'love', 'night', 'day', 'summer', 'winter',
        'ocean', 'mountain', 'city', 'space', 'dream', 'memory', 'fantasy', 'party',
        'dance', 'travel', 'nature', 'rain', 'sunset', 'morning', 'evening', 'time',
        'life', 'death', 'birth', 'childhood', 'youth', 'age', 'future', 'past',
        'present', 'history', 'war', 'peace', 'fight', 'battle', 'victory', 'defeat',
        'success', 'failure', 'beginning', 'end', 'forest', 'desert', 'sea', 'river',
        'lake', 'sky', 'stars', 'moon', 'sun', 'light', 'dark', 'shadow', 'fire', 'water',
        'earth', 'air', 'spring', 'autumn', 'fall', 'season', 'holiday', 'celebration',
        'ritual', 'ceremony', 'wedding', 'funeral', 'birth', 'graduation', 'anniversary'
    ]
}

def create_category_dictionary(output_file='word_categories.xlsx'):
    """创建分类词典并保存为Excel文件"""
    try:
        # 创建DataFrame
        max_len = max(len(v) for v in DEFAULT_CATEGORIES.values())
        categories_df = pd.DataFrame()
        
        for category, words in DEFAULT_CATEGORIES.items():
            # 确保所有列长度一致
            padded_words = words + [''] * (max_len - len(words))
            categories_df[category] = padded_words
        
        # 保存到Excel
        categories_df.to_excel(output_file, index=False)
        print(f"分类词典已保存到: {output_file}")
        
        return output_file
    except Exception as e:
        print(f"创建分类词典时出错: {e}")
        return None

def load_category_dictionary(input_file='word_categories.xlsx'):
    """从Excel文件加载分类词典"""
    try:
        if not os.path.exists(input_file):
            print(f"分类词典文件 {input_file} 不存在，使用默认分类词典")
            return DEFAULT_CATEGORIES
        
        # 读取Excel文件
        categories_df = pd.read_excel(input_file)
        
        # 转换为字典
        categories = {}
        for column in categories_df.columns:
            # 过滤掉空值和NaN
            categories[column] = categories_df[column].dropna().tolist()
            # 转换为小写
            categories[column] = [str(word).lower() for word in categories[column] if str(word).strip()]
        
        print(f"从 {input_file} 加载了分类词典")
        print(f"类别: {', '.join(categories.keys())}")
        print(f"每个类别的词汇数量: {', '.join([f'{k}: {len(v)}' for k, v in categories.items()])}")
        
        return categories
    except Exception as e:
        print(f"加载分类词典时出错: {e}")
        return DEFAULT_CATEGORIES

def categorize_words(text, categories):
    """将文本中的词汇按照预定义的类别进行分类"""
    if not isinstance(text, str) or not text.strip():
        return {cat: [] for cat in categories.keys()}
    
    words = text.lower().split()
    result = {cat: [] for cat in categories.keys()}
    
    # 创建一个单词到类别的映射，加速查找
    word_to_category = {}
    for category, word_list in categories.items():
        for word in word_list:
            word_to_category[word] = category
    
    # 分类每个单词
    categorized_words = set()
    for word in words:
        if word in word_to_category:
            category = word_to_category[word]
            if word not in result[category]:  # 避免重复
                result[category].append(word)
            categorized_words.add(word)
    
    # 添加"其他"类别
    result['other'] = [w for w in words if w not in categorized_words]
    
    return result

def categorize_data(input_file, category_file='word_categories.xlsx', output_file=None):
    """对Excel文件中的数据进行分类"""
    print(f"正在读取文件: {input_file}")
    
    try:
        # 读取Excel文件
        df = pd.read_excel(input_file)
        
        # 加载分类词典
        categories = load_category_dictionary(category_file)
        
        # 对prompt进行分类
        if 'cleaned_prompt' in df.columns:
            print("正在对prompt进行分类...")
            prompt_categories = df['cleaned_prompt'].apply(lambda x: categorize_words(x, categories))
            
            # 将分类结果展开到单独的列
            df['prompt_genres'] = prompt_categories.apply(lambda x: ', '.join(x['music_genres']))
            df['prompt_emotions'] = prompt_categories.apply(lambda x: ', '.join(x['music_emotions']))
            df['prompt_narrative'] = prompt_categories.apply(lambda x: ', '.join(x['narrative_elements']))
            df['prompt_other'] = prompt_categories.apply(lambda x: ', '.join(x['other']))
            
            print("prompt分类完成")
        
        # 对tags进行分类
        if 'cleaned_tags' in df.columns:
            print("正在对tags进行分类...")
            tag_categories = df['cleaned_tags'].apply(lambda x: categorize_words(x, categories))
            
            # 将分类结果展开到单独的列
            df['tag_genres'] = tag_categories.apply(lambda x: ', '.join(x['music_genres']))
            df['tag_emotions'] = tag_categories.apply(lambda x: ', '.join(x['music_emotions']))
            df['tag_narrative'] = tag_categories.apply(lambda x: ', '.join(x['narrative_elements']))
            df['tag_other'] = tag_categories.apply(lambda x: ', '.join(x['other']))
            
            print("tags分类完成")
        
        # 保存分类结果
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_categorized.xlsx"
        
        df.to_excel(output_file, index=False)
        print(f"分类后的数据已保存到: {output_file}")
        
        return df, output_file
    
    except Exception as e:
        print(f"数据分类过程中出错: {e}")
        return None, None

if __name__ == "__main__":
    # 测试函数
    input_file = "F:\\ai_program_2\\udio_analyze\\music_prompt_cleaned.xlsx"
    create_category_dictionary()
    categorize_data(input_file) 