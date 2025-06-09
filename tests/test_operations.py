# Tests for MCP server operations
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server import (
    list_files,
    read_file,
    search_logs,
    filter_by_level,
    search_all_logs,
    log_summary,
)


def test_list_files_contains_sample_logs():
    output = asyncio.run(list_files())
    assert output and output[0].type == "text"
    text = output[0].text
    assert "app1.log" in text
    assert "app2.log" in text


def test_read_file_last_lines():
    lines = Path("logs/app1.log").read_text().splitlines()
    expected = lines[-2:]
    result = asyncio.run(read_file("app1.log", lines=2))[0].text
    assert f"showing last 2 of {len(lines)} lines" in result
    assert f"{len(lines)-1:4d} | {expected[0]}" in result
    assert f"{len(lines):4d} | {expected[1]}" in result


def test_read_file_missing():
    text = asyncio.run(read_file("missing.log"))[0].text
    assert "not found" in text


def test_search_logs_found():
    text = asyncio.run(search_logs("app2.log", "Unhandled exception"))[0].text
    assert "Search results" in text
    assert "Unhandled exception" in text


def test_search_logs_not_found():
    text = asyncio.run(search_logs("app2.log", "doesnotexist"))[0].text
    assert "No matches" in text


def test_filter_by_level_error():
    count = sum("[ERROR]" in l for l in Path("logs/app1.log").read_text().splitlines())
    text = asyncio.run(filter_by_level("app1.log", "ERROR"))[0].text
    assert f"{count} found" in text


def test_filter_by_level_invalid():
    text = asyncio.run(filter_by_level("app1.log", "TRACE"))[0].text
    assert "Invalid level" in text


def test_search_all_logs():
    text = asyncio.run(search_all_logs("Service started", max_results=10))[0].text
    assert "across all logs" in text
    assert "app1.log" in text or "app2.log" in text


def test_log_summary_contains_counts():
    lines = Path("logs/app2.log").read_text().splitlines()
    total = len(lines)
    text = asyncio.run(log_summary("app2.log"))[0].text
    assert f"Summary for app2.log ({total} total lines)" in text
    assert "Log Levels:" in text
    assert "PaymentService" in text


def test_log_summary_missing_file():
    text = asyncio.run(log_summary("no.log"))[0].text
    assert "not found" in text
