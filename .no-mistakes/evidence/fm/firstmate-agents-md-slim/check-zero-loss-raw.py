import subprocess, json, os, sys, collections

REPO="/Users/tony/.no-mistakes/worktrees/9dab86943ee0/01M3C1J294KRT11SZ08VMEQGEF"
BASE="c643b57"; TARGET="cb2d56d"

def show(rev, p):
    return subprocess.run(["git","-C",REPO,"show",f"{rev}:{p}"],capture_output=True,text=True,check=True).stdout

base_agents = show(BASE,"AGENTS.md")
tgt_agents = show(TARGET,"AGENTS.md")
base_lines = [l.rstrip("\n") for l in base_agents.split("\n") if l.strip()]
tgt_set = collections.Counter(l.rstrip("\n") for l in tgt_agents.split("\n"))
removed = [l for l in base_lines if tgt_set[l] == 0]

# Build the target tree text corpus: all .md files tracked at target
files = subprocess.run(["git","-C",REPO,"ls-tree","-r","--name-only",TARGET],capture_output=True,text=True,check=True).stdout.split()
md = [f for f in files if f.endswith((".md",".mdx"))]
corpus = collections.Counter()
for f in md:
    for line in show(TARGET,f).split("\n"):
        corpus[line.rstrip("\n")] += 1

missing=[]
present=[]
for l in removed:
    (present if corpus[l]>0 else missing).append(l)

print(f"removed_nonblank_lines={len(removed)} present_in_target_tree={len(present)} missing={len(missing)}")
print("=== MISSING ===")
for l in missing:
    print(repr(l))
print("=== dup-count sanity (removed lines whose target AGENTS.md count changed but still present) ===")
