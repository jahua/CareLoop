# Prism Import Package

This folder contains all necessary files for importing your research paper and references into Prism (https://prism.openai.com).

## 📁 Contents

- **`references.bib`** - BibTeX file with all 68 references from your paper
- **`V8.2.7_MDPI_APA.tex`** - Your main LaTeX paper file
- **`figures/`** - All 16 figures used in the paper (~6.7 MB)
  - `mdpi/` - 7 MDPI-formatted diagrams (method/design)
  - [root] - 9 results plots and dialogue illustrations
- **`FIGURES_INDEX.md`** - Complete guide to all figures
- **`README.md`** - This file

## 🚀 How to Import to Prism

### Option 1: Import BibTeX File

1. Go to https://prism.openai.com/?d=2
2. Click on **"Import"** or **"Add References"**
3. Select **"BibTeX"** as the import format
4. Upload `references.bib`
5. Prism will automatically parse and organize all 68 references

### Option 2: Manual Upload

1. Drag and drop `references.bib` directly into Prism
2. Prism will detect it's a BibTeX file and process accordingly

### Option 3: Import Main Paper

1. Upload `V8.2.7_MDPI_APA.tex` to Prism
2. Prism can extract citations and metadata from LaTeX files

## 📚 Reference Statistics

Total references: **68**

### Key References by Category:

**Personality Psychology:**
- Roberts et al. (2007) - Power of Personality [4]
- Quirin et al. (2023) - Zurich Model [10]
- McCrae & Costa (1992, 2003) - Big Five [3, 40]

**Digital Mental Health:**
- Ahmad et al. (2022) - Personality-Adaptive Agents [66] ⭐ NEW
- Wanniarachchi et al. (2025) - Personalization Review [67] ⭐ NEW
- Soni et al. (2023) - Personality-Adaptive Chatbots [68] ⭐ NEW
- Shah et al. (2019, 2021) - Digital Interventions [23, 24]

**LLMs & AI:**
- OpenAI (2023) - GPT-4 Technical Report [46]
- Brown et al. (2020) - Few-Shot Learners [47]
- Ouyang et al. (2022) - RLHF [65]

**Frameworks:**
- Wu et al. (2024) - PROMISE Framework [7]

**Statistics & Methods:**
- Cohen (1988) - Statistical Power Analysis [60]
- Montgomery (2017) - Experimental Design [31]
- Faul et al. (2009) - G*Power [34]

## 🔍 BibTeX Entry Types

The bibliography includes:
- **Articles** (journal papers): 45 entries
- **Books**: 11 entries
- **Conference proceedings**: 9 entries
- **Technical reports**: 3 entries

## 💡 Tips for Prism

1. **Tag your references** after import:
   - Tag by topic: "personality", "LLMs", "mental-health", etc.
   - Tag by importance: "key-reference", "methodology", "background"

2. **Create collections**:
   - Core Theory (Big Five, Zurich Model)
   - Technical Implementation (PROMISE, GPT-4)
   - Related Work (digital health interventions)
   - Evaluation Methods (LLM-as-judge, statistics)

3. **Add notes** to key references:
   - Why it's cited
   - Key findings
   - How it relates to your work

4. **Link references** that cite each other or discuss similar topics

## 📊 Figures

The package includes **16 high-resolution figures** (~6.7 MB total):

### Method & Design (7 figures)
- Study workflow and experimental design
- System architecture (D-R-E modules)
- Detection pipeline and trait mapping
- Regulation workflow and evaluation framework

### Results (9 figures)
- Data quality and detection accuracy
- **Selective enhancement plot** (key finding) ⭐
- Dialogue illustrations showing personality adaptation

See `FIGURES_INDEX.md` for complete descriptions and locations in paper.

## 📝 Citation Format

The BibTeX file uses standard entry types and fields compatible with:
- Prism
- Zotero
- Mendeley
- EndNote
- LaTeX/BibTeX
- Other reference managers

## ⚠️ Important Notes

- **DOIs included** for [66], [67], [68] (new references)
- **arXiv identifiers** preserved for preprints
- **Complete author lists** for all entries
- **Page numbers** formatted as `--` (en-dash) per BibTeX standard

## 🔗 Related Files

Main paper location:
```
../MDPI_template_APA/V8.2.7_MDPI_APA.tex
```

## 📧 Support

If you encounter any issues importing:
1. Ensure the `.bib` file is UTF-8 encoded
2. Check for special characters (already handled with LaTeX escapes)
3. Try importing in smaller batches if Prism has size limits

---

**Generated:** February 1, 2026  
**Paper:** Personality-Adaptive Conversational AI for Emotional Support  
**Version:** V8.2.7
