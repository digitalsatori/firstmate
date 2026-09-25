import fs from "node:fs";
import path from "node:path";
import { loadProjectSkills, skillDescriptionTokens, parseFrontmatter } from "/Users/tony/.bun/install/global/node_modules/backpass/src/skills.js";
import { estimateTokens } from "/Users/tony/.bun/install/global/node_modules/backpass/src/tokens.js";

const root = process.argv[2];
const agents = fs.readFileSync(path.join(root, "AGENTS.md"), "utf8");
const skills = loadProjectSkills(root);
const desc = skillDescriptionTokens(skills);
const mem = estimateTokens(agents);
console.log(JSON.stringify({
  root,
  agentsBytes: Buffer.byteLength(agents, "utf8"),
  agentsTokens: mem,
  skillCount: skills.length,
  descriptionTokens: desc,
  alwaysLoadedTokens: mem + desc,
  newSkills: skills.filter(s => ["home-layout","dispatch-profiles","crewmate-briefs","agent-only-skills"].includes(s.name)).map(s=>({name:s.name,descTokens:s.descriptionTokens}))
}, null, 2));
