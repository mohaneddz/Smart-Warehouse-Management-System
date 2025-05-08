# Script to convert a Jupyter Notebook (.ipynb) to a Python (.py) script
import nbformat
import sys
import os

def notebook_to_python(ipynb_path, py_path=None):
    # Load the notebook
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Extract code cells
    code_cells = [cell['source'] for cell in nb.cells if cell['cell_type'] == 'code']
    code = '\n\n'.join(code_cells)

    # Determine output path
    if not py_path:
        py_path = os.path.splitext(ipynb_path)[0] + '.py'

    # Write to .py file
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Converted {ipynb_path} to {py_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python jupyterToPython.py <notebook.ipynb> [output.py]")
        sys.exit(1)
    ipynb_path = sys.argv[1]
    py_path = sys.argv[2] if len(sys.argv) > 2 else None
    notebook_to_python(ipynb_path, py_path)