import os
import markdown

index_content = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/vega@3"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite@2"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed@3"></script>
  <style>
  .code {
    padding: 10px;
    margin: 5px;
    border-radius: 5px;
    background: #f7f7f7;
    border-color: #cfcfcf;
    border-style: solid;
    border-width: 1px;
  }
  body {
    font-family: -apple-system,BlinkMacSystemFont,avenir next,avenir,helvetica,helvetica neue,ubuntu,roboto,noto,segoe ui,arial,sans-serif
  }
  .code > pre {
    margin: 0px;
  }
  </style>
</head>
<body>
%s
</body>
</html>
"""

with open('README.md') as readme:
    with open('docs/index.html', 'w') as index:
        md = readme.read().replace('```python', '```')
        index.write(index_content % markdown.markdown(md))

for p in os.listdir('./notebooks'):
    sp = os.path.splitext(p)
    if sp[1] == 'ipynb':
        os.system('python scripts/nb2html.py notebooks/%s.ipynb docs/%s.html' % (sp[0], sp[0]))
