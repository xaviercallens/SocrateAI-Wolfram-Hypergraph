#!/bin/bash
rsync -av /home/xavkal/xdev/SocrateAI-Scientific-Hypergraph-K3*T2/paper/MFDM_Continuum_Limit_Paper.tex /tmp/test-clone2/paper/MFDM_Continuum_Limit_Paper.tex
cd /tmp/test-clone2
export PATH="/tmp/git-deb/usr/bin:$PATH"
export GIT_EXEC_PATH="/tmp/git-deb/usr/lib/git-core"
git add paper/MFDM_Continuum_Limit_Paper.tex
git commit -m "docs(phase8): Fix hexadecapole terminology and add SKA projection results"
git push origin HEAD:main
