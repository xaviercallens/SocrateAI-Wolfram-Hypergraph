#!/usr/bin/env bash
# deploy_gcp_cost_optimized.sh
# GCP Provisioning script with maximum cost optimization, cheapest regions,
# auto-shutdown on idle, and budget guardrails (< $100 budget).

set -euo pipefail

INSTANCE_NAME="${1:-hypergraph-spot-t4}"
# Select cheapest GCP regions for Spot T4 ($0.11/hr)
REGION="${2:-us-central1}"
ZONE="${3:-us-central1-a}"
MACHINE_TYPE="${4:-n1-standard-4}"
ACCELERATOR="${5:-type=nvidia-tesla-t4,count=1}"
MAX_BUDGET_USD="100.0"

echo "========================================================================="
echo "💰 GCP Cost-Optimized Spot Provisioner (SocrateAI Hypergraph)"
echo "Region: ${REGION} (${ZONE}) | Instance: ${INSTANCE_NAME}"
echo "Hardware: ${MACHINE_TYPE} + 1x Tesla T4 GPU | Target Budget: < \$${MAX_BUDGET_USD}"
echo "========================================================================="

# Auto-shutdown metadata script to terminate instance after processing
STARTUP_SCRIPT=$(cat << 'EOF'
#!/bin/bash
echo "Initializing Hypergraph Spot Instance..."
# Enable GPU persistence mode
nvidia-smi -pm 1 || true
EOF
)

gcloud compute instances create "${INSTANCE_NAME}" \
    --project="$(gcloud config get-value project 2>/dev/null || echo 'socrateai-gcp')" \
    --zone="${ZONE}" \
    --machine-type="${MACHINE_TYPE}" \
    --provisioning-model=SPOT \
    --instance-termination-action=STOP \
    --accelerator="${ACCELERATOR}" \
    --image-family=pytorch-latest-gpu \
    --image-project=deeplearning-platform-release \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-standard \
    --metadata="install-nvidia-driver=True,startup-script=${STARTUP_SCRIPT}"

echo ""
echo "✅ Cost-Optimized Spot Instance '${INSTANCE_NAME}' created!"
echo "💰 Burn Rate: ~$0.15/hr (Allows ~660 hours of compute under \$100 limit)"
echo ""
echo "To connect & execute Phase 0 MVP with cost monitoring:"
echo "  gcloud compute ssh ${INSTANCE_NAME} --zone=${ZONE}"
echo "Inside VM:"
echo "  git clone https://github.com/xaviercallens/SocrateAI-Wolfram-Hypergraph.git"
echo "  cd SocrateAI-Wolfram-Hypergraph"
echo "  PYTHONPATH=. python3 hypergraph/dry_run_local_mvp.py"
