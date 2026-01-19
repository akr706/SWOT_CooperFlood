#!/usr/bin/env python3
from bs4 import BeautifulSoup
import json
import re
import html

# Read the HTML file
with open('SWOT_Water_Depth_Analysis_Public (1).html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find all cells
cells = []
cell_divs = soup.find_all('div', class_=re.compile(r'jp-Cell jp-(Markdown|Code)Cell jp-Notebook-cell'))

for cell_div in cell_divs:
    cell = {}
    
    # Check if it's a markdown or code cell
    if 'jp-MarkdownCell' in cell_div.get('class', []):
        cell['cell_type'] = 'markdown'
        cell['metadata'] = {}
        
        # Find the markdown content from the rendered output
        markdown_div = cell_div.find('div', class_='jp-MarkdownOutput')
        if markdown_div:
            # Convert HTML back to markdown (simplified)
            text = markdown_div.get_text()
            cell['source'] = text.split('\n')
        else:
            cell['source'] = []
            
    elif 'jp-CodeCell' in cell_div.get('class', []):
        cell['cell_type'] = 'code'
        cell['execution_count'] = None
        cell['metadata'] = {}
        
        # Find the code content - look for the input area
        input_area = cell_div.find('div', class_='jp-InputArea')
        if input_area:
            code_pre = input_area.find('pre')
            if code_pre:
                code_text = code_pre.get_text()
                # Split into lines while preserving empty lines
                cell['source'] = code_text.split('\n')
            else:
                cell['source'] = []
        else:
            cell['source'] = []
        
        # Find outputs
        outputs = []
        output_wrapper = cell_div.find('div', class_='jp-OutputArea-output')
        if output_wrapper:
            # Check for text/stream output
            output_pre = output_wrapper.find('pre')
            if output_pre:
                outputs.append({
                    'name': 'stdout',
                    'output_type': 'stream',
                    'text': output_pre.get_text().split('\n')
                })
            
            # Check for plots/HTML output
            if not output_pre:
                output_html = str(output_wrapper)
                outputs.append({
                    'data': {
                        'text/html': [output_html]
                    },
                    'metadata': {},
                    'output_type': 'display_data'
                })
        
        cell['outputs'] = outputs
    
    if cell:
        cells.append(cell)

# Create the notebook structure
notebook = {
    'cells': cells,
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'codemirror_mode': {
                'name': 'ipython',
                'version': 3
            },
            'file_extension': '.py',
            'mimetype': 'text/x-python',
            'name': 'python',
            'nbconvert_exporter': 'python',
            'pygments_lexer': 'ipython3',
            'version': '3.12.1'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 5
}

# Save the notebook
with open('SWOT_Water_Depth_Analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"✓ Converted HTML to Jupyter notebook")
print(f"✓ Created {len(cells)} cells")
print(f"✓ Saved as: SWOT_Water_Depth_Analysis.ipynb")
