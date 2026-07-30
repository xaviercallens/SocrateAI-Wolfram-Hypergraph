# SocrateAI-Wolfram-Hypergraph Makefile

.PHONY: test lint lean4 pipeline clean install

test:
	export PYTHONPATH=. && pytest tests/ --cov=hypergraph --cov=scripts

lint:
	flake8 hypergraph/ mcp/ scripts/
	mypy hypergraph/ mcp/ --ignore-missing-imports

lean4:
	@echo "Verifying Lean 4 proofs..."
	@cd proofs/Lean4 && \
	for f in *.lean; do \
		if grep -q "sorry" "$$f"; then \
			echo "Error: Found 'sorry' token in $$f"; \
			exit 1; \
		fi; \
		if grep -q "admit" "$$f"; then \
			echo "Error: Found 'admit' token in $$f"; \
			exit 1; \
		fi; \
		lean "$$f" || exit 1; \
	done
	@echo "All Lean 4 proofs verified successfully."

pipeline:
	export PYTHONPATH=. && python scripts/run_phase1b_nanograv_proof.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf coverage.xml

install:
	pip install -r requirements-lock.txt
	pip install -e .
