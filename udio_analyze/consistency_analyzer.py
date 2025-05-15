import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def analyze_tag_prompt_consistency(df, output_dir=None):
    """分析标签和提示词之间的一致性"""
    
    print("开始分析标签和提示词的一致性...")
    
    if output_dir is None:
        output_dir = '.'
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 准备分析数据
    consistency_data = []
    
    # 对每个类别计算一致性
    for category in ['genres', 'emotions', 'narrative']:
        prompt_col = f'prompt_{category}'
        tag_col = f'tag_{category}'
        
        # 跳过缺失的列
        if prompt_col not in df.columns or tag_col not in df.columns:
            print(f"跳过 {category} 类别，因为缺少必要的列")
            continue
        
        print(f"正在分析 {category} 类别的一致性...")
        
        for i, row in df.iterrows():
            if isinstance(row[prompt_col], str) and isinstance(row[tag_col], str):
                # 分割词汇，并过滤掉空字符串
                prompt_words = set([w for w in row[prompt_col].lower().split(', ') if w.strip()])
                tag_words = set([w for w in row[tag_col].lower().split(', ') if w.strip()])
                
                if not prompt_words or not tag_words:
                    continue
                
                # 计算交集
                common_words = prompt_words.intersection(tag_words)
                
                # 计算Jaccard相似度 (交集/并集)
                union_words = prompt_words.union(tag_words)
                jaccard = len(common_words) / len(union_words) if union_words else 0
                
                # 计算重叠系数 (交集/较小集合)
                overlap = len(common_words) / min(len(prompt_words), len(tag_words)) if min(len(prompt_words), len(tag_words)) > 0 else 0
                
                # 记录数据
                consistency_data.append({
                    'row_id': i,
                    'category': category,
                    'prompt_words': ', '.join(prompt_words),
                    'tag_words': ', '.join(tag_words),
                    'common_words': ', '.join(common_words),
                    'prompt_count': len(prompt_words),
                    'tag_count': len(tag_words),
                    'common_count': len(common_words),
                    'jaccard_similarity': jaccard,
                    'overlap_coefficient': overlap
                })
    
    if not consistency_data:
        print("没有找到可以分析的数据")
        return None, None
    
    # 创建DataFrame
    consistency_df = pd.DataFrame(consistency_data)
    
    # 计算每个类别的平均一致性
    category_consistency = consistency_df.groupby('category').agg({
        'jaccard_similarity': ['mean', 'median', 'std'],
        'overlap_coefficient': ['mean', 'median', 'std'],
        'row_id': 'count'
    }).reset_index()
    
    # 重命名列
    category_consistency.columns = ['category', 'jaccard_mean', 'jaccard_median', 'jaccard_std', 
                                   'overlap_mean', 'overlap_median', 'overlap_std', 'count']
    
    # 保存结果
    details_file = os.path.join(output_dir, 'tag_prompt_consistency_details.xlsx')
    summary_file = os.path.join(output_dir, 'tag_prompt_consistency_summary.xlsx')
    
    consistency_df.to_excel(details_file, index=False)
    category_consistency.to_excel(summary_file, index=False)
    
    print(f"一致性详细数据已保存到: {details_file}")
    print(f"一致性摘要数据已保存到: {summary_file}")
    
    # 创建一致性分布直方图
    try:
        plt.figure(figsize=(10, 6))
        for category in consistency_df['category'].unique():
            subset = consistency_df[consistency_df['category'] == category]
            plt.hist(subset['jaccard_similarity'], alpha=0.5, label=category, bins=20)
        
        plt.xlabel('Jaccard Similarity')
        plt.ylabel('Frequency')
        plt.title('Tag-Prompt Consistency Distribution')
        plt.legend()
        plt.tight_layout()
        
        chart_file = os.path.join(output_dir, 'tag_prompt_consistency.png')
        plt.savefig(chart_file)
        print(f"一致性分布图表已保存到: {chart_file}")
        plt.close()
        
        # 创建箱线图
        plt.figure(figsize=(10, 6))
        data_to_plot = [consistency_df[consistency_df['category'] == cat]['jaccard_similarity'] 
                        for cat in consistency_df['category'].unique()]
        plt.boxplot(data_to_plot, labels=consistency_df['category'].unique())
        plt.ylabel('Jaccard Similarity')
        plt.title('Tag-Prompt Consistency by Category')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        boxplot_file = os.path.join(output_dir, 'tag_prompt_consistency_boxplot.png')
        plt.savefig(boxplot_file)
        print(f"一致性箱线图已保存到: {boxplot_file}")
        plt.close()
        
    except Exception as e:
        print(f"创建图表时出错: {e}")
    
    return consistency_df, category_consistency

def analyze_consistency(input_file, output_dir=None):
    """执行一致性分析"""
    
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
        
        # 执行一致性分析
        consistency_details, consistency_summary = analyze_tag_prompt_consistency(df, output_dir)
        
        if consistency_summary is not None:
            print("\n=== 一致性分析摘要 ===")
            print(consistency_summary)
        
        print("\n一致性分析完成！")
        
        return True
    
    except Exception as e:
        print(f"一致性分析过程中出错: {e}")
        return False

if __name__ == "__main__":
    # 测试函数
    input_file = "F:\\ai_program_2\\udio_analyze\\music_prompt_categorized.xlsx"
    analyze_consistency(input_file) 