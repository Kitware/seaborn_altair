import json
import sys
import markdown

header = """
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
"""

vis = """
  <div id="%s"></div>
  <script type="text/javascript">
    var spec = %s;
    var opt = {"renderer": "canvas", "actions": false};
    vegaEmbed("#%s", spec, opt);
  </script>
"""

footer = """
</body>
</html>
"""

if __name__ == "__main__":
    with open(sys.argv[1]) as inp:
        nb = json.load(inp)

    if len(sys.argv) > 2:
        outf = sys.argv[2]
    else:
        outf = sys.argv[1].split(".")[0] + ".html"

    with open(outf, "w") as out:
        out.write(header)
        for i, c in enumerate(nb["cells"]):
            if c["cell_type"] == "markdown":
                out.write("<div>%s</div>" % markdown.markdown("".join(c["source"])))
            if c["cell_type"] == "code":
                source = "".join(c["source"]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                out.write("<div class=\"code\"><pre>%s</pre></div>" % source)
                for o in c["outputs"]:
                    vg = o["data"].get("application/vnd.vegalite.v2+json")
                    img = o["data"].get("image/png")
                    if vg:
                        visid = "vis%s" % i
                        out.write(vis % (visid, json.dumps(vg), visid))
                    elif img:
                        out.write("<img src=data:image/png;base64,%s>" % img)

        out.write(footer)

