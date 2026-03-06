# Statistical Analysis Scripts

**位置**: `prism_export/scripts/`  
**更新**: 2026-02-03  
**状态**: ✅ 组织良好，生产就绪

这个目录包含了人格适应性聊天机器人的完整统计分析流程。

## 🆕 重要更新（2026-02-03）

### 新增内容
- ⭐ **主生成脚本**: `generate_all_figures.py` - 使用 Cliff's delta 生成所有图表
- 📚 **完整指南**: `FIGURE_GENERATION_GUIDE.md` - 图表生成完整文档
- 🗂️ **整理的生成器**: `generators/` - 来自 V8.3/generators 的整理脚本

### 推荐使用
对于新工作，使用主生成脚本：
```bash
python3 generate_all_figures.py
```

此脚本：
- ✅ 使用 Cliff's delta（不是 Cohen's d）
- ✅ 生成所有出版图表
- ✅ 包含对话插图
- ✅ 完整文档和验证

## 📁 目录结构

```
scripts/
├── README.md                              # 本文件
├── generate_all_figures.py                # ⭐ 主图表生成器（Cliff's delta）
├── statistical_analysis_enhanced.ipynb    # 主要分析笔记本
├── enhanced_statistical_analysis.py       # 核心分析函数库
├── visualization_config.py                # 可视化配置（MDPI 标准）
├── FIGURE_GENERATION_GUIDE.md             # 图表生成完整指南
├── generators/                            # 整理的生成器脚本
│   ├── README.md                          # 生成器文档
│   ├── analysis/                          # 统计分析脚本
│   ├── diagrams/                          # 系统架构图生成器
│   ├── submission/                        # 提交准备工具
│   └── maintenance/                       # 维护工具
├── archive/                               # 归档的示例和文档
│   ├── docs/
│   └── examples/
├── data/                                  # 数据目录
│   ├── merged/                            # 合并后的数据（用于分析）
│   │   ├── baseline.csv                   # 基线组数据
│   │   └── regulated.csv                  # 调节组数据
│   └── raw/                               # 原始数据
│       ├── A-1.csv ... A-5.csv            # 人格类型 A 对话
│       ├── B-1.csv ... B-5.csv            # 人格类型 B 对话
│       └── 1-Evaluation-Simulated-Conversations.xlsx
├── figures/                               # 生成的图表
│   ├── 01_sample_distribution.*           # 样本分布
│   ├── 02_missing_data_heatmap.*          # 缺失数据热图
│   ├── 03_performance_comparison.*        # 性能对比
│   ├── 04_effect_sizes.*                  # 效应量（Cliff's delta）
│   ├── 06_personality_dimensions.*        # 人格维度分布
│   ├── 07_personality_heatmap.*           # 人格热图
│   ├── 08_weighted_scores.*               # 加权分数
│   ├── 09_total_score_boxplot.*           # 总分箱线图
│   ├── 10_selective_enhancement_paired.*  # 选择性增强
│   ├── 11_metric_composition.*            # 指标组成
│   ├── data_quality_*.png                 # 数据质量图表
│   └── mdpi/                              # MDPI 标准图表
│       ├── system_architecture_mdpi.png
│       ├── detection_pipeline_mdpi.png
│       └── ...
├── *.csv                                  # 分析结果输出
│   ├── analysis_results_summary.csv       # 综合汇总
│   ├── analysis_results_advanced_tests.csv # 高级统计检验
│   ├── regulated_with_scores.csv          # 调节组+分数
│   ├── baseline_with_scores.csv           # 基线组+分数
│   └── regulated_with_personality.csv     # 调节组+人格向量
└── archive/                               # 归档文件
    ├── docs/                              # 文档文件
    ├── examples/                          # 示例和测试脚本
    └── output_old/                        # 旧的输出文件

```

## 🚀 快速开始

### 1. 运行完整分析

在 Jupyter 中打开主笔记本：

```bash
jupyter notebook statistical_analysis_enhanced.ipynb
```

然后执行：
- `Kernel` → `Restart & Run All`

### 2. 重新加载模块（如果修改了代码）

运行笔记本中的 **Cell 3**（模块重新加载单元格）。

### 3. 查看结果

- **图表**: `figures/` 目录（PNG + PDF 格式）
- **数据**: `*.csv` 文件
- **解释**: 笔记本中的 Markdown 单元格

---

## 📊 主要分析内容

### STEP 1-2: 数据加载与质量评估
- 加载 Regulated 和 Baseline 数据
- 评估数据完整性和质量

### STEP 3: 人格向量分析
- 解析 OCEAN 人格维度
- 可视化人格分布

### STEP 4-5: 加权评分系统
- YES=2, NOT SURE=1, NO=0
- 计算描述统计

### STEP 6-7: 效应量分析 ⭐
- **Cliff's delta** (δ) - 非参数效应量
- YES-rate 效应（风险差、比值比、Cohen's h）
- 适合有界/序数数据

### STEP 8: 高级统计检验
- 配对 t 检验
- Wilcoxon 符号秩检验
- Bootstrap 置信区间

### STEP 9: 信度分析
- Cronbach's Alpha
- 项间相关

### STEP 10-11: 综合汇总与导出
- 创建完整汇总表
- 导出所有结果（CSV + 图表）

---

## 🔧 核心函数 (`enhanced_statistical_analysis.py`)

### 数据处理
- `load_and_prepare_data()` - 加载数据
- `assess_data_quality()` - 评估质量
- `convert_to_numeric()` - 转换为数值

### 统计分析
- `calculate_descriptive_statistics()` - 描述统计
- `calculate_effect_sizes()` - 效应量（**Cliff's delta**）
- `perform_advanced_statistical_tests()` - 高级检验
- `perform_reliability_analysis()` - 信度分析

### 人格分析
- `analyze_personality_vectors()` - 解析人格向量
- `analyze_weighted_scores()` - 加权评分

### 可视化
- `visualize_results()` - 主要结果可视化
- `visualize_personality_vectors()` - 人格可视化
- `visualize_weighted_scores()` - 分数可视化
- `visualize_selective_enhancement()` - 选择性增强可视化

---

## 📈 可视化标准

所有图表遵循 **MDPI 出版标准**：
- ✅ 分辨率: 300 DPI (PNG) / Vector (PDF)
- ✅ 宽度: 单栏 85mm (3.35"), 双栏 170mm (6.69")
- ✅ 字体大小: 8-9 pt (标签), 9-10 pt (图例)
- ✅ 线宽: 1.0-1.5 pt
- ✅ 色彩: Okabe-Ito 配色（色盲友好）
- ✅ 格式: PNG + PDF 双格式输出

参考：
- [matplotlib_for_papers](https://github.com/jbmouret/matplotlib_for_papers)
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information*

---

## 🎯 关键发现

### 效应量（Cliff's delta）

| 指标 | Cliff's δ | 解释 | YES率提升 |
|------|-----------|------|-----------|
| **Emotional Tone** | 0.000 | negligible | 0.0% |
| **Relevance & Coherence** | 0.017 | negligible | 1.7% |
| **Personality Needs** | 0.917 | **large** ⭐ | 91.7% |

**核心结论**: 人格适应性调节在"满足人格需求"维度上展现出**大效应量**（δ=0.917），表明系统能够显著改善对用户人格特征的响应。

---

## ⚠️ 重要说明

### 为什么使用 Cliff's Delta 而非 Cohen's d？

1. **数据特征**:
   - 有界数据 [0, 1]
   - 离散评分 (0, 0.5, 1)
   - 天花板效应（Regulated 组 → 1.0）

2. **Cohen's d 的问题**:
   - ❌ 方差接近 0 → d 暴涨至 4.58（无意义）
   - ❌ 假设正态分布（实际为离散分布）
   - ❌ 不适用于有界数据

3. **Cliff's delta 的优势**:
   - ✅ 专为序数/有界数据设计
   - ✅ 稳健的非参数方法
   - ✅ 概率解释：δ=0.917 = "Regulated 组在 91.7% 的配对比较中优于 Baseline"

### Cliff's Delta 阈值（Romano et al., 2006）
- |δ| < 0.147: negligible
- |δ| < 0.33: small
- |δ| < 0.474: medium
- |δ| ≥ 0.474: **large**

---

## 📚 引用

如果使用本分析框架，请引用：

```bibtex
@misc{personality_adaptive_chatbot_2026,
  title={Statistical Analysis Framework for Personality-Adaptive Chatbot Evaluation},
  author={Your Name},
  year={2026},
  note={Enhanced with Cliff's delta for bounded ordinal data}
}
```

**关键方法引用**:
- Cliff, N. (1993). Dominance statistics: Ordinal analyses to answer ordinal questions. *Psychological Bulletin*, 114(3), 494-509.
- Romano, J., et al. (2006). Appropriate statistics for ordinal level data. *Psychological Methods*, 11(4), 639-652.

---

## 🆘 故障排除

### AttributeError: 'PublicationStandards' object has no attribute 'FONT_SIZE_BASE'

**解决方案**:
1. 运行笔记本中的 **Cell 3** (模块重新加载)
2. 或重启内核: `Kernel` → `Restart & Run All`

### NameError: name 'df_stats' is not defined

**解决方案**: 按顺序运行所有单元格（Cell 21 必须在 Cell 23 之前运行）

### FileNotFoundError: data/merged/regulated.csv

**解决方案**: 确保在 `scripts/` 目录下运行，数据文件存在于 `data/merged/`

---

## 📝 更新日志

### v1.0 (2026-02-03)
- ✅ 替换 Cohen's d 为 Cliff's delta
- ✅ 添加 YES-rate 效应量（OR, RD, Cohen's h）
- ✅ 修复 `PublicationStandards` 字体大小属性
- ✅ 更新综合汇总表和解释
- ✅ 清理和组织目录结构

---

## 👥 联系方式

如有问题或建议，请联系项目维护者。

---

**最后更新**: 2026-02-03
**Python 版本**: 3.11+
**主要依赖**: pandas, numpy, matplotlib, scipy, seaborn
