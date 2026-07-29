"""
Unit tests for GlobalCostMonitor and WolframRateLimiter
"""

import pytest
import time
from hypergraph.cost_monitoring import GlobalCostMonitor
from hypergraph.rate_limiter import WolframRateLimiter, rate_limited


def test_cost_monitor_initialization(tmp_path):
    monitor = GlobalCostMonitor(
        region="us-central1",
        vcpus=4,
        ram_gb=15.0,
        gpus=1,
        disk_gb=500.0,
        max_budget_usd=100.0,
        storage_dir=tmp_path / "test_logs"
    )

    cost_info = monitor.calculate_current_cost()
    assert cost_info["region"] == "us-central1"
    assert cost_info["hourly_burn_rate_usd"] > 0.0
    assert cost_info["remaining_budget_usd"] == 100.0
    assert monitor.enforce_budget_guardrails() is True


def test_cost_monitor_telemetry_logging(tmp_path):
    storage_dir = tmp_path / "test_logs"
    monitor = GlobalCostMonitor(storage_dir=storage_dir)
    log_file = monitor.log_telemetry(step_info={"step": 1, "status": "ok"})

    assert log_file.exists()
    assert log_file.name == "cost_telemetry.json"


def test_wolfram_rate_limiter():
    limiter = WolframRateLimiter(max_requests_per_minute=600, burst_capacity=5)

    @rate_limited(limiter)
    def test_query(x):
        return x * 2

    res = test_query(5)
    assert res == 10
    assert limiter.total_queries_issued == 1
