import pandas as pd
from collections import Counter
import re

def analyze_prompts():
    try:
        # 读取Excel文件
        print("正在读取Excel文件...")
        df = pd.read_excel('music_prompt.xlsx')
        
        # 检查是否存在prompt列
        if 'prompt' not in df.columns:
            print("文件中没有找到'prompt'列")
            return
        
        # 提取所有提示词
        prompts = df['prompt'].dropna().tolist()
        print(f"共找到 {len(prompts)} 个有效提示词")
        
        # 提示词长度分析
        prompt_lengths = [len(p) for p in prompts]
        avg_length = sum(prompt_lengths) / len(prompt_lengths) if prompt_lengths else 0
        print(f"提示词平均长度: {avg_length:.1f} 字符")
        
        # 提取常见词汇
        all_words = []
        for prompt in prompts:
            # 将提示词分割成单词
            words = re.findall(r'\b\w+\b', prompt.lower())
            all_words.extend(words)
        
        # 计算最常见的词
        common_words = Counter(all_words).most_common(20)
        
        # 输出结果
        print("\n最常见的20个词:")
        for word, count in common_words:
            print(f"{word}: {count}次")
        
        # 将结果保存到文件
        with open('prompt_analysis.txt', 'w', encoding='utf-8') as f:
            f.write(f"共分析了 {len(prompts)} 个有效提示词\n")
            f.write(f"提示词平均长度: {avg_length:.1f} 字符\n\n")
            
            f.write("最常见的20个词:\n")
            for word, count in common_words:
                f.write(f"{word}: {count}次\n")
            
            f.write("\n示例提示词(前5个):\n")
            for i, prompt in enumerate(prompts[:5], 1):
                f.write(f"{i}. {prompt}\n")
        
        print("\n分析结果已保存到 prompt_analysis.txt")
        
    except Exception as e:
        print(f"分析过程中出错: {e}")

if __name__ == "__main__":
    analyze_prompts() 