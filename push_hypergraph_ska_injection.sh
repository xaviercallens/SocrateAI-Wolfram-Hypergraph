#!/bin/bash
rsync -av /home/xavkal/xdev/SocrateAI-Scientific-Hypergraph-K3*T2/paper/MFDM_Continuum_Limit_Paper.tex /tmp/test-clone2/paper/MFDM_Continuum_Limit_Paper.tex
rsync -av /home/xavkal/xdev/SocrateAI-Scientific-Hypergraph-K3*T2/scripts/ska_enterprise_injection.py /tmp/test-clone2/scripts/ska_enterprise_injection.py
cd /tmp/test-clone2
export PATH="/tmp/git-deb/usr/bin:$PATH"
export GIT_EXEC_PATH="/tmp/git-deb/usr/lib/git-core"
git add paper/MFDM_Continuum_Limit_Paper.tex scripts/ska_enterprise_injection.py
git commit -m "docs(phase8): Add libstempo/enterprise SKA injection pipeline to paper and scripts"
git push origin HEAD:main
