# 音乐提示词偏好分析系统

这是一个用于分析音乐提示词偏好的数据分析系统，可以对音乐生成平台的提示词数据进行全面分析。

## 功能特点

1. **数据清洗**：排除非英语词汇，确保分析数据的质量
2. **数据分类**：将词汇分为音乐类型、音乐情绪、场景叙述和其他四个类别
3. **词频分析**：分析各类别词汇的出现频率
4. **高频搭配分析**：分析词汇之间的搭配关系
5. **一致性分析**：分析标签(tag)和提示词(prompt)之间的一致性
6. **综合报告生成**：生成包含图表和数据表格的Excel综合报告

## 系统要求

- Python 3.6+
- pandas
- matplotlib
- numpy
- nltk
- xlsxwriter

## 安装依赖

```bash
pip install pandas matplotlib numpy nltk xlsxwriter
```

## 使用方法

### 基本用法

```bash
python main.py [输入文件路径]
```

默认情况下，系统会使用 `F:\ai_program_2\udio_analyze\music_prompt.xlsx` 作为输入文件。

### 高级选项

```bash
python main.py [输入文件路径] -o [输出目录] -s [跳过步骤]
```

参数说明：
- `-o, --output`：指定输出目录（默认会创建一个以时间戳命名的目录）
- `-s, --skip`：跳过指定的分析步骤，可选值包括：
  - `clean`：跳过数据清洗
  - `categorize`：跳过数据分类
  - `frequency`：跳过词频分析
  - `consistency`：跳过一致性分析
  - `report`：跳过报告生成

例如，如果只想执行词频分析和报告生成：

```bash
python main.py -s clean categorize consistency
```

## 输出文件

分析完成后，系统会在输出目录中生成以下文件：

1. `music_prompt_cleaned.xlsx`：清洗后的数据
2. `word_categories.xlsx`：词汇分类词典
3. `music_prompt_categorized.xlsx`：分类后的数据
4. 各种词频分析结果（如`prompt_word_frequency.xlsx`）
5. 词对分析结果（如`prompt_word_pairs.xlsx`）
6. 一致性分析结果（`tag_prompt_consistency_details.xlsx`和`tag_prompt_consistency_summary.xlsx`）
7. `music_prompt_analysis_report.xlsx`：综合分析报告

## 分析流程

1. **数据清洗**：使用NLTK的英语词典过滤非英语词汇
2. **数据分类**：根据预定义的分类词典，将词汇分为不同类别
3. **词频分析**：计算各类别词汇的出现频率，生成词频表和图表
4. **高频搭配分析**：分析词汇之间的搭配关系，生成词对频率表和热力图
5. **一致性分析**：计算标签和提示词之间的Jaccard相似度和重叠系数
6. **报告生成**：整合所有分析结果，生成包含图表的Excel报告

## 自定义分类词典

系统会自动生成一个默认的分类词典（`word_categories.xlsx`），您可以根据需要修改这个文件，添加或删除各类别的词汇。修改后的词典将在下次运行时自动加载。

## 注意事项

- 输入文件必须是Excel格式（.xlsx）
- 输入文件应至少包含`prompt`和`tags`列
- 首次运行时，系统会下载NLTK资源，可能需要一些时间
- 生成图表需要matplotlib，如果遇到图形界面相关错误，可以尝试使用无头模式运行 
