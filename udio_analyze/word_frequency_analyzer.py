import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os
import numpy as np

def analyze_word_frequency(df, column_name, output_file, top_n=30):
    """分析指定列的词频并输出到Excel"""
    
    if column_name not in df.columns:
        print(f"列 {column_name} 不存在于数据中")
        return None
    
    print(f"正在分析 {column_name} 列的词频...")
    
    # 合并所有词汇
    all_words = []
    for text in df[column_name].dropna():
        if isinstance(text, str):
            all_words.extend(text.lower().split())
    
    print(f"共收集到 {len(all_words)} 个词汇")
    
    # 计算词频
    word_counts = Counter(all_words)
    most_common = word_counts.most_common(top_n)
    
    print(f"最常见的词汇: {', '.join([word for word, _ in most_common[:5]])}")
    
    # 创建DataFrame
    freq_df = pd.DataFrame(most_common, columns=['Word', 'Frequency'])
    
    # 保存到Excel
    freq_df.to_excel(output_file, index=False)
    print(f"词频分析结果已保存到: {output_file}")
    
    # 创建条形图
    try:
        plt.figure(figsize=(12, 8))
        plt.bar(range(len(most_common)), [count for _, count in most_common], align='center')
        plt.xticks(range(len(most_common)), [word for word, _ in most_common], rotation=90)
        plt.title(f'Top {top_n} Words in {column_name}')
        plt.tight_layout()
        
        # 保存图表
        chart_file = f"{os.path.splitext(output_file)[0]}_chart.png"
        plt.savefig(chart_file)
        print(f"词频图表已保存到: {chart_file}")
        plt.close()
    except Exception as e:
        print(f"创建图表时出错: {e}")
    
    return freq_df

def analyze_category_word_frequency(df, input_file, output_dir=None):
    """分析各个类别的词频"""
    
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
        if not output_dir:
            output_dir = '.'
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    results = {}
    
    # 分析prompt词频
    if 'cleaned_prompt' in df.columns:
        output_file = os.path.join(output_dir, "prompt_word_frequency.xlsx")
        results['prompt'] = analyze_word_frequency(df, 'cleaned_prompt', output_file)
    
    # 分析tags词频
    if 'cleaned_tags' in df.columns:
        output_file = os.path.join(output_dir, "tag_word_frequency.xlsx")
        results['tags'] = analyze_word_frequency(df, 'cleaned_tags', output_file)
    
    # 按类别分析词频
    for prefix in ['prompt', 'tag']:
        for category in ['genres', 'emotions', 'narrative', 'other']:
            column = f"{prefix}_{category}"
            if column in df.columns:
                output_file = os.path.join(output_dir, f"{column}_frequency.xlsx")
                results[column] = analyze_word_frequency(df, column, output_file, top_n=20)
    
    return results

def analyze_word_pairs(df, column_name, output_file, top_n=30):
    """分析词汇搭配频率"""
    
    if column_name not in df.columns:
        print(f"列 {column_name} 不存在于数据中")
        return None
    
    print(f"正在分析 {column_name} 列的词对搭配...")
    
    from itertools import combinations
    
    # 收集所有词对
    all_pairs = []
    for text in df[column_name].dropna():
        if isinstance(text, str):
            words = text.lower().split()
            # 去重，避免同一行中的重复词汇产生多个相同的词对
            unique_words = sorted(set(words))
            if len(unique_words) > 1:  # 确保至少有两个不同的词
                # 生成所有可能的词对组合
                pairs = list(combinations(unique_words, 2))
                all_pairs.extend(pairs)
    
    print(f"共收集到 {len(all_pairs)} 个词对")
    
    # 计算词对频率
    pair_counts = Counter(all_pairs)
    most_common_pairs = pair_counts.most_common(top_n)
    
    # 创建DataFrame
    pairs_df = pd.DataFrame(most_common_pairs, columns=['Word Pair', 'Frequency'])
    pairs_df['Word 1'] = pairs_df['Word Pair'].apply(lambda x: x[0])
    pairs_df['Word 2'] = pairs_df['Word Pair'].apply(lambda x: x[1])
    pairs_df = pairs_df[['Word 1', 'Word 2', 'Frequency']]
    
    # 保存到Excel
    pairs_df.to_excel(output_file, index=False)
    print(f"词对分析结果已保存到: {output_file}")
    
    # 创建热力图数据
    try:
        top_words = list(set([w for pair in most_common_pairs for w in pair]))
        heatmap_data = pd.DataFrame(0, index=top_words, columns=top_words)
        
        for (word1, word2), freq in most_common_pairs:
            if word1 in top_words and word2 in top_words:
                heatmap_data.loc[word1, word2] = freq
                heatmap_data.loc[word2, word1] = freq
        
        # 保存热力图数据
        heatmap_file = f"{os.path.splitext(output_file)[0]}_heatmap.xlsx"
        heatmap_data.to_excel(heatmap_file)
        print(f"词对热力图数据已保存到: {heatmap_file}")
        
        # 创建热力图
        plt.figure(figsize=(12, 10))
        plt.imshow(heatmap_data.values, cmap='YlOrRd')
        plt.colorbar(label='Frequency')
        plt.xticks(range(len(top_words)), top_words, rotation=90)
        plt.yticks(range(len(top_words)), top_words)
        plt.title(f'Word Pair Co-occurrence in {column_name}')
        plt.tight_layout()
        
        # 保存图表
        chart_file = f"{os.path.splitext(output_file)[0]}_heatmap.png"
        plt.savefig(chart_file)
        print(f"词对热力图已保存到: {chart_file}")
        plt.close()
    except Exception as e:
        print(f"创建热力图时出错: {e}")
    
    return pairs_df

def analyze_cross_category_pairs(df, cat1, cat2, output_file):
    """分析不同类别之间的词汇搭配"""
    
    if cat1 not in df.columns or cat2 not in df.columns:
        print(f"列 {cat1} 或 {cat2} 不存在于数据中")
        return None
    
    print(f"正在分析 {cat1} 和 {cat2} 之间的词汇搭配...")
    
    all_pairs = []
    for i, row in df.iterrows():
        if isinstance(row[cat1], str) and isinstance(row[cat2], str):
            words1 = row[cat1].lower().split(', ')
            words2 = row[cat2].lower().split(', ')
            
            # 过滤掉空字符串
            words1 = [w for w in words1 if w.strip()]
            words2 = [w for w in words2 if w.strip()]
            
            if words1 and words2:  # 确保两个列表都不为空
                # 生成跨类别词对
                cross_pairs = [(w1, w2) for w1 in words1 for w2 in words2]
                all_pairs.extend(cross_pairs)
    
    print(f"共收集到 {len(all_pairs)} 个跨类别词对")
    
    # 计算词对频率
    pair_counts = Counter(all_pairs)
    most_common_pairs = pair_counts.most_common(30)
    
    # 创建DataFrame
    pairs_df = pd.DataFrame(most_common_pairs, columns=['Word Pair', 'Frequency'])
    pairs_df['Category 1 Word'] = pairs_df['Word Pair'].apply(lambda x: x[0])
    pairs_df['Category 2 Word'] = pairs_df['Word Pair'].apply(lambda x: x[1])
    pairs_df = pairs_df[['Category 1 Word', 'Category 2 Word', 'Frequency']]
    
    # 保存到Excel
    pairs_df.to_excel(output_file, index=False)
    print(f"跨类别词对分析结果已保存到: {output_file}")
    
    return pairs_df

def analyze_all_word_frequencies(input_file, output_dir=None):
    """执行所有词频分析"""
    
    print(f"正在读取文件: {input_file}")
    
    try:
        # 读取Excel文件
        df = pd.read_excel(input_file)
        
        if output_dir is None:
            output_dir = os.path.dirname(input_file)
            if not output_dir:
                output_dir = '.'
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. 分析各列词频
        print("\n===== 开始词频分析 =====")
        freq_results = analyze_category_word_frequency(df, input_file, output_dir)
        
        # 2. 分析词对搭配
        print("\n===== 开始词对搭配分析 =====")
        # 分析prompt中的词对
        if 'cleaned_prompt' in df.columns:
            output_file = os.path.join(output_dir, "prompt_word_pairs.xlsx")
            prompt_pairs = analyze_word_pairs(df, 'cleaned_prompt', output_file)
        
        # 分析tags中的词对
        if 'cleaned_tags' in df.columns:
            output_file = os.path.join(output_dir, "tag_word_pairs.xlsx")
            tag_pairs = analyze_word_pairs(df, 'cleaned_tags', output_file)
        
        # 3. 分析跨类别词对
        print("\n===== 开始跨类别词对分析 =====")
        # 分析音乐类型和情绪的搭配
        if 'prompt_genres' in df.columns and 'prompt_emotions' in df.columns:
            output_file = os.path.join(output_dir, "genre_emotion_pairs.xlsx")
            genre_emotion_pairs = analyze_cross_category_pairs(
                df, 'prompt_genres', 'prompt_emotions', output_file
            )
        
        # 分析音乐类型和叙事元素的搭配
        if 'prompt_genres' in df.columns and 'prompt_narrative' in df.columns:
            output_file = os.path.join(output_dir, "genre_narrative_pairs.xlsx")
            genre_narrative_pairs = analyze_cross_category_pairs(
                df, 'prompt_genres', 'prompt_narrative', output_file
            )
        
        print("\n词频分析全部完成！")
        
        return True
    
    except Exception as e:
        print(f"词频分析过程中出错: {e}")
        return False

if __name__ == "__main__":
    # 测试函数
    input_file = "F:\\ai_program_2\\udio_analyze\\music_prompt_categorized.xlsx"
    analyze_all_word_frequencies(input_file) 