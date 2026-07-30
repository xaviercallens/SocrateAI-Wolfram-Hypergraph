#!/usr/bin/env bash
# deploy_gcp_phase0.sh
# GCP Provisioning script for Phase 0 MVP Single-Node Tensor Validation
# Budget Target: < $100 (~$0.15/hr Spot Tesla T4 VM)

set -euo pipefail

INSTANCE_NAME="${1:-hypergraph-mvp-t4}"
ZONE="${2:-us-central1-a}"
MACHINE_TYPE="${3:-n1-standard-4}"
ACCELERATOR="${4:-type=nvidia-tesla-t4,count=1}"

echo "============================================================"
echo "Provisioning GCP Spot Deep Learning VM for Phase 0 MVP"
echo "Instance: ${INSTANCE_NAME} | Zone: ${ZONE} | GPU: Tesla T4"
echo "============================================================"

gcloud compute instances create "${INSTANCE_NAME}" \
    --zone="${ZONE}" \
    --machine-type="${MACHINE_TYPE}" \
    --provisioning-model=SPOT \
    --accelerator="${ACCELERATOR}" \
    --image-family=pytorch-latest-gpu \
    --image-project=deeplearning-platform-release \
    --boot-disk-size=50GB \
    --metadata="install-nvidia-driver=True"

echo ""
echo "✅ Instance ${INSTANCE_NAME} created successfully!"
echo "To SSH into the instance and run Phase 0 MVP benchmark:"
echo "  gcloud compute ssh ${INSTANCE_NAME} --zone=${ZONE}"
echo "Inside instance:"
echo "  git clone https://github.com/xaviercallens/SocrateAI-Wolfram-Hypergraph.git"
echo "  cd SocrateAI-Wolfram-Hypergraph"
echo "  PYTHONPATH=. python3 hypergraph/phase0_tensor_masking.py"
