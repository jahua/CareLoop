#!/usr/bin/env python3
import sys
from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def autofit_docx(in_path: Path, out_path: Path):
    doc = Document(str(in_path))

    def set_autofit(table):
        tbl = table._tbl
        tblPr = tbl.tblPr
        if tblPr is None:
            tblPr = OxmlElement('w:tblPr')
            tbl.append(tblPr)
        # remove fixed layout if present and set to autofit
        for el in list(tblPr):
            if el.tag == qn('w:tblLayout'):
                tblPr.remove(el)
        tblLayout = OxmlElement('w:tblLayout')
        tblLayout.set(qn('w:type'), 'autofit')
        tblPr.append(tblLayout)

    for t in doc.tables:
        set_autofit(t)
        # remove fixed widths in cells
        for node in t._tbl.iter():
            if node.tag == qn('w:tcPr'):
                for child in list(node):
                    if child.tag == qn('w:tcW'):
                        node.remove(child)

    doc.save(str(out_path))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: autofit_tables.py INPUT_DOCX [OUTPUT_DOCX]")
        sys.exit(1)
    inp = Path(sys.argv[1])
    outp = Path(sys.argv[2]) if len(sys.argv) > 2 else inp
    autofit_docx(inp, outp)
    print("Auto-fit applied:", outp)


























