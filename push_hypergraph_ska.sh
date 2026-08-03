#!/bin/bash
rsync -av /home/xavkal/xdev/SocrateAI-Scientific-Hypergraph-K3*T2/data_benchmarks/ska_pta_loader.py /tmp/test-clone2/data_benchmarks/ska_pta_loader.py
rsync -av /home/xavkal/xdev/SocrateAI-Scientific-Hypergraph-K3*T2/scripts/ska_spectral_comparison.py /tmp/test-clone2/scripts/ska_spectral_comparison.py
cd /tmp/test-clone2
export PATH="/tmp/git-deb/usr/bin:$PATH"
export GIT_EXEC_PATH="/tmp/git-deb/usr/lib/git-core"
git add data_benchmarks/ska_pta_loader.py scripts/ska_spectral_comparison.py
git commit -m "feat(phase8): SKA/IPTA data loader and spectral index cross-validation pipeline"
git push origin HEAD:main
