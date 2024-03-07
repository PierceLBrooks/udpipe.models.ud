import os
import sys
import json
import subprocess
import spacy_udpipe

if (len(sys.argv) < 1):
    sys.exit()
if not ("." in sys.argv[0]):
    sys.exit()
text = ""
if (len(sys.argv) < 2):
    text += "Charles Darwin studied at the University of Edinburgh in 1825."
else:
    if ((len(sys.argv) == 2) and (" " in sys.argv[1])):
        text = sys.argv[1]
    else:
        text += " ".join(sys.argv[1:])
text = text.strip()
nlp = None
path = os.path.join(os.getcwd(), "models", "english-ud-2.1-20180111.udpipe")
if (os.path.exists(path)):
    nlp = spacy_udpipe.load_from_path(lang="en", path=path, meta={"description": "Custom \"en\" model"})
else:
    nlp = spacy_udpipe.load("en")
doc = nlp(text)
"""
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_)
"""
data = doc.to_json()
path = os.path.join(os.getcwd(), os.path.basename(sys.argv[0])+".dot")
fd = open(path, "w")
path = os.path.basename(sys.argv[0])
fd.write("digraph "+path[:path.index(".")]+" {\n")
for token in data["tokens"]:
    fd.write("\tnode_"+str(token["id"])+" [ label = \""+text[token["start"]:token["end"]]+"\" ] ; \n")
    if (token["id"] == token["head"]):
        continue
    fd.write("\tnode_"+str(token["id"])+" -> node_"+str(token["head"])+" [ label = \""+token["dep"]+"\" ] ; \n")
fd.write("}\n")
fd.close()
path = os.path.join(os.getcwd(), path+".out")
fd = open(path, "w")
fd.write(json.dumps(data))
fd.close()
try:
    args = [sys.executable, "-m", "json.tool", path]
    print(str(args))
    result = subprocess.check_output(args)
    lines = result.decode().split("\n")
    fd = open(path+".json", "w")
    for line in lines:
        fd.write(line.rstrip()+"\n")
    fd.close()
except:
    pass

