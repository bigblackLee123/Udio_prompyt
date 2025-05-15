import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def generate_analysis_report(input_file, output_dir=None):
    """生成综合分析报告"""
    
    print("开始生成综合分析报告...")
    
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
        if not output_dir:
            output_dir = '.'
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 读取原始数据
        df = pd.read_excel(input_file)
        
        # 报告文件名
        report_file = os.path.join(output_dir, 'music_prompt_analysis_report.xlsx')
        
        # 创建Excel工作簿
        writer = pd.ExcelWriter(report_file, engine='xlsxwriter')
        workbook = writer.book
        
        # 添加数据摘要
        print("正在生成数据摘要...")
        
        # 计算基本统计信息
        total_rows = len(df)
        valid_prompts = df['cleaned_prompt'].notna().sum() if 'cleaned_prompt' in df.columns else 0
        avg_prompt_len = df['cleaned_prompt'].str.len().mean() if 'cleaned_prompt' in df.columns else 0
        
        # 尝试加载词频数据
        try:
            prompt_freq_file = os.path.join(output_dir, "prompt_word_frequency.xlsx")
            if os.path.exists(prompt_freq_file):
                prompt_freq = pd.read_excel(prompt_freq_file)
                top_word = prompt_freq['Word'].iloc[0] if len(prompt_freq) > 0 else '未知'
            else:
                top_word = '未知'
        except:
            top_word = '未知'
        
        # 尝试加载类别词频数据
        try:
            genres_file = os.path.join(output_dir, "prompt_genres_frequency.xlsx")
            emotions_file = os.path.join(output_dir, "prompt_emotions_frequency.xlsx")
            narrative_file = os.path.join(output_dir, "prompt_narrative_frequency.xlsx")
            
            top_genre = pd.read_excel(genres_file)['Word'].iloc[0] if os.path.exists(genres_file) else '未知'
            top_emotion = pd.read_excel(emotions_file)['Word'].iloc[0] if os.path.exists(emotions_file) else '未知'
            top_narrative = pd.read_excel(narrative_file)['Word'].iloc[0] if os.path.exists(narrative_file) else '未知'
        except:
            top_genre = top_emotion = top_narrative = '未知'
        
        # 创建摘要DataFrame
        summary = pd.DataFrame({
            '指标': ['数据总量', '有效提示词数量', '平均提示词长度', '最常见词汇', '最常见音乐类型', '最常见情绪词', '最常见叙事元素'],
            '值': [
                total_rows,
                valid_prompts,
                f"{avg_prompt_len:.1f} 字符",
                top_word,
                top_genre,
                top_emotion,
                top_narrative
            ]
        })
        
        # 写入摘要工作表
        summary.to_excel(writer, sheet_name='摘要', index=False)
        
        # 格式化摘要工作表
        summary_sheet = writer.sheets['摘要']
        summary_sheet.set_column('A:A', 20)
        summary_sheet.set_column('B:B', 30)
        
        # 添加标题格式
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # 应用标题格式
        for col_num, value in enumerate(summary.columns.values):
            summary_sheet.write(0, col_num, value, header_format)
        
        # 添加词频分析结果
        print("正在添加词频分析结果...")
        
        # 加载词频数据
        for file_name in os.listdir(output_dir):
            if file_name.endswith('_frequency.xlsx') and not file_name.endswith('_heatmap.xlsx'):
                try:
                    sheet_name = os.path.splitext(file_name)[0]
                    if len(sheet_name) > 31:  # Excel工作表名称长度限制
                        sheet_name = sheet_name[:31]
                    
                    freq_df = pd.read_excel(os.path.join(output_dir, file_name))
                    freq_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    
                    # 格式化工作表
                    sheet = writer.sheets[sheet_name]
                    sheet.set_column('A:A', 20)
                    sheet.set_column('B:B', 10)
                    
                    # 应用标题格式
                    for col_num, value in enumerate(freq_df.columns.values):
                        sheet.write(0, col_num, value, header_format)
                    
                    # 添加条形图
                    chart = workbook.add_chart({'type': 'column'})
                    
                    # 设置图表数据范围
                    row_count = min(15, len(freq_df))  # 最多显示前15个
                    chart.add_series({
                        'name': '词频',
                        'categories': f'={sheet_name}!$A$2:$A${row_count+1}',
                        'values': f'={sheet_name}!$B$2:$B${row_count+1}',
                    })
                    
                    # 设置图表标题和标签
                    chart.set_title({'name': f'{sheet_name} 词频分析'})
                    chart.set_x_axis({'name': '词汇'})
                    chart.set_y_axis({'name': '频率'})
                    
                    # 插入图表
                    sheet.insert_chart('D2', chart, {'x_scale': 1.5, 'y_scale': 1})
                    
                except Exception as e:
                    print(f"添加 {file_name} 时出错: {e}")
        
        # 添加词对分析结果
        print("正在添加词对分析结果...")
        
        # 加载词对数据
        for file_name in os.listdir(output_dir):
            if '_pairs.xlsx' in file_name and not '_heatmap.xlsx' in file_name:
                try:
                    sheet_name = os.path.splitext(file_name)[0]
                    if len(sheet_name) > 31:  # Excel工作表名称长度限制
                        sheet_name = sheet_name[:31]
                    
                    pairs_df = pd.read_excel(os.path.join(output_dir, file_name))
                    pairs_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    
                    # 格式化工作表
                    sheet = writer.sheets[sheet_name]
                    sheet.set_column('A:A', 15)
                    sheet.set_column('B:B', 15)
                    sheet.set_column('C:C', 10)
                    
                    # 应用标题格式
                    for col_num, value in enumerate(pairs_df.columns.values):
                        sheet.write(0, col_num, value, header_format)
                    
                except Exception as e:
                    print(f"添加 {file_name} 时出错: {e}")
        
        # 添加一致性分析结果
        print("正在添加一致性分析结果...")
        
        # 加载一致性摘要数据
        consistency_file = os.path.join(output_dir, 'tag_prompt_consistency_summary.xlsx')
        if os.path.exists(consistency_file):
            try:
                consistency_df = pd.read_excel(consistency_file)
                consistency_df.to_excel(writer, sheet_name='一致性摘要', index=False)
                
                # 格式化工作表
                sheet = writer.sheets['一致性摘要']
                sheet.set_column('A:H', 12)
                
                # 应用标题格式
                for col_num, value in enumerate(consistency_df.columns.values):
                    sheet.write(0, col_num, value, header_format)
                
                # 添加条形图
                chart = workbook.add_chart({'type': 'column'})
                
                # 设置图表数据范围
                row_count = len(consistency_df)
                chart.add_series({
                    'name': 'Jaccard相似度',
                    'categories': f'=一致性摘要!$A$2:$A${row_count+1}',
                    'values': f'=一致性摘要!$B$2:$B${row_count+1}',
                })
                
                # 设置图表标题和标签
                chart.set_title({'name': '各类别Jaccard相似度'})
                chart.set_x_axis({'name': '类别'})
                chart.set_y_axis({'name': '相似度'})
                
                # 插入图表
                sheet.insert_chart('J2', chart, {'x_scale': 1.2, 'y_scale': 1})
                
            except Exception as e:
                print(f"添加一致性摘要时出错: {e}")
        
        # 添加信息工作表
        print("正在添加报告信息...")
        
        # 创建信息DataFrame
        info_data = {
            '项目': ['报告生成时间', '数据文件', '分析脚本版本'],
            '值': [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                os.path.basename(input_file),
                '1.0'
            ]
        }
        info_df = pd.DataFrame(info_data)
        
        # 写入信息工作表
        info_df.to_excel(writer, sheet_name='报告信息', index=False)
        
        # 格式化信息工作表
        info_sheet = writer.sheets['报告信息']
        info_sheet.set_column('A:A', 15)
        info_sheet.set_column('B:B', 30)
        
        # 应用标题格式
        for col_num, value in enumerate(info_df.columns.values):
            info_sheet.write(0, col_num, value, header_format)
        
        # 保存并关闭
        writer.close()
        
        print(f"综合分析报告已生成: {report_file}")
        
        return report_file
    
    except Exception as e:
        print(f"生成报告过程中出错: {e}")
        return None

def generate_report(input_file, output_dir=None):
    """生成分析报告的入口函数"""
    
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
        if not output_dir:
            output_dir = '.'
    
    return generate_analysis_report(input_file, output_dir)

if __name__ == "__main__":
    # 测试函数
    input_file = "F:\\ai_program_2\\udio_analyze\\music_prompt_categorized.xlsx"
    generate_report(input_file) 