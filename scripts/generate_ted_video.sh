#!/bin/bash
# -----------------------------------------------------------------------------
# Script: generate_ted_video.sh
# Purpose: Orchestrates the Antigravity Rendering Pipeline.
# Ensures scratch/out directories exist and triggers the python pipeline.
# -----------------------------------------------------------------------------

set -e

echo "=========================================================="
echo "🚀 Google Antigravity Rendering Pipeline - Video Generator"
echo "=========================================================="
echo "Target Sequence: Almkvist-Zudilin #1 (P=18)"
echo "Target Cosmology: Omega_m = 0.315"
echo ""

# 1. Setup directories
WORKSPACE="$(pwd)"
SCRATCH_DIR="${WORKSPACE}/scratch/frames"
OUT_DIR="${WORKSPACE}/out"

mkdir -p "$SCRATCH_DIR"
mkdir -p "$OUT_DIR"

echo "Directory structure initialized."
echo "Scratch: $SCRATCH_DIR"
echo "Output:  $OUT_DIR"
echo ""

# 2. Check dependencies
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ Warning: FFmpeg is not installed in this environment."
    echo "Please install it via 'apt-get install ffmpeg' to assemble the final MP4."
fi

# 3. Execute the Python Orchestrator
echo "Executing Core Generation & Plotting Engine..."
python3 scripts/antigravity_video_pipeline.py

echo ""
echo "✅ Pipeline Execution Complete!"
echo "Check $OUT_DIR for the final geometry_evolution_talk.mp4"
echo "=========================================================="
