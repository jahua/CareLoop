# 🚀 Quick Start: Figure Integration

## What Changed?

The MDPI converter now **automatically finds and embeds all figures** from `@figures/` directory.

## ✅ One-Command Conversion

```bash
cd "/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/MDPI converter"
bash convert_revised_manuscript.sh
```

**That's it!** The converter will:

1. ✅ Auto-detect `../statistical analyis/figures/` directory
2. ✅ Find all 11 PNG files
3. ✅ Insert them into the Word document
4. ✅ Create proper captions
5. ✅ Save to `../docoutput/V5_Healthcare_Submission_REVISED_MDPI.docx`

## 📊 What Gets Embedded?

All 11 publication-quality figures:

```
01_sample_distribution.png          → Figure 1
02_missing_data_heatmap.png         → Figure 2
06_personality_dimensions.png       → Figure 3
07_personality_heatmap.png          → Figure 4
03_performance_comparison.png       → Figure 5
04_effect_sizes.png                 → Figure 6
05_percentage_improvement.png       → Figure 7
08_weighted_scores.png              → Figure 8
09_total_score_boxplot.png          → Figure 9
10_system_overview.png              → Figure 10
11_study_workflow.png               → Figure 11
```

## 🎯 Features

✅ **Automatic Detection**: Finds figures without manual specification
✅ **Smart Paths**: Checks multiple locations automatically
✅ **Figure Before Caption**: Proper academic format
✅ **300 DPI**: Publication-grade quality
✅ **Embedded**: Figures inside the Word file (no external links)
✅ **MDPI Compliant**: All formatting standards met
✅ **Error Handling**: Color-coded status messages
✅ **Verification**: Reports embedded media count

## 📝 Output

After running the script:

```
✓ Output file created: 2.5 MB
✓ Embedded media objects: 11
```

Open in Microsoft Word and verify:
- [ ] All figures visible
- [ ] Captions properly formatted
- [ ] Figure quality looks good
- [ ] No placeholder text remaining

## 🔧 If Figures Don't Appear

### Check 1: Verify figures exist

```bash
ls -la "../statistical analyis/figures/"
# Should show 11 PNG files
```

### Check 2: Run with verbose output

```bash
python3 mdpi_template_converter.py \
    ../V5_Healthcare_Submission_REVISED.md \
    -o ../docoutput/output.docx \
    -f "../statistical analyis/figures"
```

### Check 3: Check Word file size

```bash
ls -lh ../docoutput/V5_Healthcare_Submission_REVISED_MDPI.docx
# Should be > 1 MB if figures embedded
```

### Check 4: Verify embedded media

```bash
unzip -l ../docoutput/V5_Healthcare_Submission_REVISED_MDPI.docx | grep "word/media/"
# Should show multiple entries
```

## 📚 Full Documentation

See `FIGURES_INTEGRATION_GUIDE.md` for:
- Detailed setup instructions
- Troubleshooting guide
- Technical details
- Common workflows
- Best practices

## 🎓 Quality Standards

✅ Resolution: 300 DPI (MDPI requirement)
✅ Format: PNG lossless compression
✅ Width: 6 inches (fits A4 page)
✅ Colorblind-friendly: Yes
✅ Professional fonts: Times New Roman
✅ Caption format: **Figure X.** Caption text

## ⏱️ Time Required

- **First run**: 2-3 minutes (auto-detection + conversion)
- **Subsequent runs**: 1-2 minutes (faster)
- **Verification**: 5 minutes (check Word document)

## 💡 Pro Tips

1. **Always keep figures backed up**
   ```bash
   cp -r "../statistical analyis/figures" "../statistical analyis/figures.backup"
   ```

2. **Regenerate figures if analysis changes**
   ```bash
   cd ../statistical\ analyis
   python3 statistical_analysis_publication.py
   ```

3. **Test conversion without figures first**
   ```bash
   python3 mdpi_template_converter.py input.md -o test.docx
   ```

4. **Use absolute paths for reliability**
   ```bash
   python3 mdpi_template_converter.py \
       /absolute/path/input.md \
       -f /absolute/path/figures
   ```

## 📞 Need Help?

1. Check console output (color-coded messages)
2. Verify file paths and directory structure
3. See `FIGURES_INTEGRATION_GUIDE.md` for detailed troubleshooting
4. Ensure PNG files are not corrupted: `file figures/*.png`

---

**Status**: ✅ Production Ready
**Figures**: 11 (300 DPI, publication-grade)
**Last Updated**: October 27, 2025
