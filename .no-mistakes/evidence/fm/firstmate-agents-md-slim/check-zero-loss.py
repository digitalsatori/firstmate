import subprocess, collections, json
REPO="."; B="c643b57"; T="cb2d56d"
def show(rev,p): return subprocess.run(["git","-C",REPO,"show",f"{rev}:{p}"],capture_output=True,text=True,check=True).stdout
files=subprocess.run(["git","-C",REPO,"ls-tree","-r","--name-only",T],capture_output=True,text=True,check=True).stdout.split()
md=[f for f in files if f.endswith((".md",".mdx"))]
corpus=collections.Counter()
for f in md:
    for l in show(T,f).split("\n"): corpus[l.rstrip("\n")]+=1
tgt_ag=set(l.rstrip("\n") for l in show(T,"AGENTS.md").split("\n"))
base_lines=[l.rstrip("\n") for l in show(B,"AGENTS.md").split("\n")]
removed=[l for l in base_lines if l.strip() and l.strip() and l not in tgt_ag and l.strip() not in tgt_ag]
# removed = base non-blank lines absent from target AGENTS.md
removed=[l for l in base_lines if l.strip() and l not in tgt_ag]
present=[l for l in removed if corpus[l]>0]
missing=[l for l in removed if corpus[l]==0]
def classify(l):
    if ("- "+l) in tgt_ag: return "e3 section-9 bullet rewrite (in place, authorized)"
    if "single owner of the top-level operational-home layout" in l: return "round-3/4 authorized wording narrowing (ownership/overstatement)"
    if "section 13's process-event-sources trigger" in l: return "round-1 authorized repoint (now in home-layout, names agent-only-skills)"
    if "[account and scope matching rules" in l: return "the one relocated relative markdown link, rewritten for the deeper skill dir"
    return "UNACCOUNTED"
rows=[{"line":l,"classification":classify(l)} for l in missing]
print(json.dumps({"base_agents_nonblank_lines":len([l for l in base_lines if l.strip()]),
 "removed_nonblank":len(removed),"present_verbatim_in_target_tree":len(present),
 "differing":rows,"unaccounted":sum(1 for r in rows if r['classification']=='UNACCOUNTED')},indent=2))
