import os
import sys
import time
import argparse
from datetime import datetime

# 导入各个模块
import data_cleaner
import data_categorizer
import word_frequency_analyzer
import consistency_analyzer
import report_generator

def create_output_dir(base_dir=None):
    """创建输出目录"""
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建以时间戳命名的输出目录
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(base_dir, f'analysis_results_{timestamp}')
    
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def run_full_analysis(input_file, output_dir=None, skip_steps=None):
    """运行完整的分析流程"""
    
    if skip_steps is None:
        skip_steps = []
    
    start_time = time.time()
    
    print("\n" + "="*60)
    print("音乐提示词偏好分析系统")
    print("="*60)
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 输入文件 '{input_file}' 不存在")
        return False
    
    # 创建输出目录
    if output_dir is None:
        output_dir = create_output_dir()
    
    print(f"分析结果将保存到: {output_dir}\n")
    
    # 步骤1: 数据清洗
    if 'clean' not in skip_steps:
        print("\n" + "-"*60)
        print("步骤1: 数据清洗 - 排除非英语词汇")
        print("-"*60)
        
        data_cleaner.download_nltk_resources()
        cleaned_df, cleaned_file = data_cleaner.clean_data(input_file, os.path.join(output_dir, 'music_prompt_cleaned.xlsx'))
        
        if cleaned_df is None:
            print("数据清洗失败，无法继续分析")
            return False
    else:
        print("\n跳过数据清洗步骤...")
        cleaned_file = input_file
    
    # 步骤2: 数据分类
    if 'categorize' not in skip_steps:
        print("\n" + "-"*60)
        print("步骤2: 数据分类 - 将词汇分为音乐类型、音乐情绪、场景叙述和其他四个类别")
        print("-"*60)
        
        # 创建分类词典
        category_file = os.path.join(output_dir, 'word_categories.xlsx')
        data_categorizer.create_category_dictionary(category_file)
        
        # 对数据进行分类
        categorized_df, categorized_file = data_categorizer.categorize_data(
            cleaned_file, 
            category_file,
            os.path.join(output_dir, 'music_prompt_categorized.xlsx')
        )
        
        if categorized_df is None:
            print("数据分类失败，无法继续分析")
            return False
    else:
        print("\n跳过数据分类步骤...")
        categorized_file = cleaned_file
    
    # 步骤3: 词频分析
    if 'frequency' not in skip_steps:
        print("\n" + "-"*60)
        print("步骤3: 词频分析 - 分析词频、高频搭配")
        print("-"*60)
        
        success = word_frequency_analyzer.analyze_all_word_frequencies(categorized_file, output_dir)
        
        if not success:
            print("词频分析失败，但将继续执行后续步骤")
    else:
        print("\n跳过词频分析步骤...")
    
    # 步骤4: 一致性分析
    if 'consistency' not in skip_steps:
        print("\n" + "-"*60)
        print("步骤4: 一致性分析 - 分析tag和prompt的一致性")
        print("-"*60)
        
        success = consistency_analyzer.analyze_consistency(categorized_file, output_dir)
        
        if not success:
            print("一致性分析失败，但将继续执行后续步骤")
    else:
        print("\n跳过一致性分析步骤...")
    
    # 步骤5: 生成报告
    if 'report' not in skip_steps:
        print("\n" + "-"*60)
        print("步骤5: 生成报告 - 整合所有分析结果")
        print("-"*60)
        
        report_file = report_generator.generate_report(categorized_file, output_dir)
        
        if report_file:
            print(f"分析报告已成功生成: {report_file}")
        else:
            print("生成报告失败")
    else:
        print("\n跳过报告生成步骤...")
    
    # 计算总耗时
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "="*60)
    print(f"分析完成! 总耗时: {total_time:.2f} 秒")
    print(f"结果保存在: {output_dir}")
    print("="*60 + "\n")
    
    return True

def main():
    """主函数，处理命令行参数"""
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='音乐提示词偏好分析系统')
    
    parser.add_argument('input_file', nargs='?', default="F:\\ai_program_2\\udio_analyze\\music_prompt.xlsx",
                        help='输入Excel文件路径 (默认: F:\\ai_program_2\\udio_analyze\\music_prompt.xlsx)')
    
    parser.add_argument('-o', '--output', dest='output_dir',
                        help='输出目录路径 (默认: 自动创建时间戳目录)')
    
    parser.add_argument('-s', '--skip', dest='skip_steps', nargs='+',
                        choices=['clean', 'categorize', 'frequency', 'consistency', 'report'],
                        help='跳过指定的分析步骤 (可选: clean, categorize, frequency, consistency, report)')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 运行分析
    run_full_analysis(args.input_file, args.output_dir, args.skip_steps)

if __name__ == "__main__":
    main() 