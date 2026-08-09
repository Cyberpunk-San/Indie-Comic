import json
import sys
import os

print("Testing notebook JSON format and compilation...")

with open("Indie_Comic_pipeline.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Loaded notebook successfully. Total cells: {len(nb['cells'])}")

# Concatenate all code cells and test syntax py_compile
code_cells = [cell for cell in nb['cells'] if cell['cell_type'] == 'code']
full_code = ""

for idx, cell in enumerate(code_cells):
    cell_code = "".join(cell['source'])
    full_code += f"\n# --- CELL {idx} ---\n" + cell_code

with open("scratch/compiled_notebook_test.py", "w", encoding="utf-8") as f:
    f.write(full_code)

import sys
import py_compile

try:
    py_compile.compile("scratch/compiled_notebook_test.py", doraise=True)
    print("SUCCESS: All notebook code cells compiled successfully without syntax errors!")
except py_compile.PyCompileError as e:
    print(f"ERROR: Syntax Error in notebook compilation: {e}")
    sys.exit(1)
