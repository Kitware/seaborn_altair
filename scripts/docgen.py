import os

for p in os.listdir('./notebooks'):
  sp = os.path.splitext(p)
  if sp[1] == 'ipynb':
    os.system('python scripts/nb2html.py notebooks/%s.ipynb docs/%s.html' % (sp[0], sp[0]))
