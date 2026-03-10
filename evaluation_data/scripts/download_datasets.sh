#!/usr/bin/env bash
# Download evaluation datasets for Big5Loop simulated evaluation
# Run from: Big5Loop/evaluation_data/scripts/ or Big5Loop/evaluation_data/

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVAL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RAW_DIR="$EVAL_DIR/raw"
mkdir -p "$RAW_DIR"
cd "$EVAL_DIR"

echo "=== Big5Loop Evaluation Data Download ==="
echo "Target: $RAW_DIR"
echo ""

# --- BFI2: via R (ShinyItemAnalysis) ---
echo "[1/4] BFI2 (ShinyItemAnalysis)"
if command -v R &>/dev/null; then
  R -e "
    if (!require('ShinyItemAnalysis', quietly=TRUE)) install.packages('ShinyItemAnalysis', repos='https://cloud.r-project.org')
    library(ShinyItemAnalysis)
    data(BFI2)
    write.csv(BFI2, '$RAW_DIR/bfi2_dataset.csv', row.names=FALSE)
    cat('BFI2 saved to bfi2_dataset.csv\n')
  " 2>/dev/null || echo "  R/ShinyItemAnalysis not available. Install R and run: install.packages('ShinyItemAnalysis'); data(BFI2); write.csv(BFI2,'bfi2_dataset.csv')"
else
  echo "  R not found. Install R and run: install.packages('ShinyItemAnalysis'); data(BFI2); write.csv(BFI2,'bfi2_dataset.csv')"
fi

# --- BIG5-CHAT: Hugging Face ---
echo ""
echo "[2/4] BIG5-CHAT (Hugging Face)"
if command -v python3 &>/dev/null; then
  python3 -c "
import sys
try:
    from datasets import load_dataset
    ds = load_dataset('wenkai-li/big5_chat', split='train', trust_remote_code=True)
    out = '$RAW_DIR/big5_chat_dataset.csv'
    ds.to_csv(out, index=False)
    print('  BIG5-CHAT saved to big5_chat_dataset.csv')
except Exception as e:
    print('  Error:', e)
    print('  Run: pip install datasets && python -c \"from datasets import load_dataset; load_dataset('wenkai-li/big5_chat').to_csv('big5_chat_dataset.csv')\"')
" 2>/dev/null || echo "  Install: pip install datasets; then load wenkai-li/big5_chat"
else
  echo "  Python not found. Download from https://huggingface.co/datasets/wenkai-li/big5_chat"
fi

# --- PERSONAGE: source URL ---
echo ""
echo "[3/4] PERSONAGE"
PERSONAGE_BASE="https://farm2.user.srcf.net/research/personage"
for f in predefinedParams.xml randomParams.xml predefinedParams.tab randomParams.tab; do
  if [ ! -f "$RAW_DIR/$f" ]; then
    echo "  Fetching $f..."
    curl -f -s -o "$RAW_DIR/$f" "$PERSONAGE_BASE/$f" 2>/dev/null && echo "  Saved $f" || echo "  $f not found at $PERSONAGE_BASE (may need manual download)"
  else
    echo "  $f already present"
  fi
done

# --- NEO-PI-R: Pitt D-Scholarship (manual) ---
echo ""
echo "[4/4] NEO-PI-R (Pitt D-Scholarship)"
echo "  Manual download required:"
echo "  URL: https://d-scholarship.pitt.edu/35840/"
echo "  Files: 35840_Validity_NEO-Participant_NEW_FINAL.sav, 35840_Validity_NEO_codebook.docx"
echo "  License: CC BY-ND"

# --- BFI-2-R: IEEE DataPort (restricted) ---
echo ""
echo "=== BFI-2-R (IEEE DataPort) - RESTRICTED ==="
echo "  URL: https://ieee-dataport.org/documents/bfi-2-r"
echo "  Requires: IEEE account + DataPort subscription"
echo "  Steps: 1) Create account 2) Subscribe 3) Login to access dataset"
echo ""

echo "=== Done ==="
