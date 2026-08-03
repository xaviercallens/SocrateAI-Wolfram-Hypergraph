#!/bin/bash
rsync -av /home/xavkal/xdev/SocrateAI-Scientific-Hypergraph-K3*T2/MEMORY.md /tmp/test-clone2/MEMORY.md
cd /tmp/test-clone2
export PATH="/tmp/git-deb/usr/bin:$PATH"
export GIT_EXEC_PATH="/tmp/git-deb/usr/lib/git-core"
git add MEMORY.md
git commit -m "docs: Update MEMORY.md with Phase 6, 7, 8 milestones and note Euclid data availability"
git push origin HEAD:main
