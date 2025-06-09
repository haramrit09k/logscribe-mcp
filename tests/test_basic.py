#!/usr/bin/env python3
"""
Basic tests for logscribe MCP server
Just making sure the core functionality works
"""

import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path so we can import our server
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server import server, get_logs_directory


def test_server_exists():
    """Basic smoke test - make sure server imports"""
    assert server is not None
    assert server.name == "log-server"


def test_get_logs_directory_default():
    """Test default logs directory"""
    # Clear any existing args/env
    original_argv = sys.argv.copy()
    original_env = os.environ.get('LOGS_DIR')
    
    try:
        sys.argv = ['test']
        if 'LOGS_DIR' in os.environ:
            del os.environ['LOGS_DIR']
        
        logs_dir = get_logs_directory()
        
        # The function returns logs directory relative to mcp_server.py location
        # which should be in the parent directory from our tests/ folder
        expected = Path(__file__).parent.parent / "logs"
        assert logs_dir == expected, f"Expected {expected}, got {logs_dir}"
        
    finally:
        sys.argv = original_argv
        if original_env:
            os.environ['LOGS_DIR'] = original_env


def test_get_logs_directory_env_var():
    """Test logs directory from environment variable"""
    original_argv = sys.argv.copy()
    original_env = os.environ.get('LOGS_DIR')
    
    try:
        sys.argv = ['test']
        test_dir = "/tmp/test_logs"
        os.environ['LOGS_DIR'] = test_dir
        
        logs_dir = get_logs_directory()
        assert str(logs_dir) == test_dir
        
    finally:
        sys.argv = original_argv
        if original_env:
            os.environ['LOGS_DIR'] = original_env
        elif 'LOGS_DIR' in os.environ:
            del os.environ['LOGS_DIR']


def test_get_logs_directory_cmd_arg():
    """Test logs directory from command line argument"""
    original_argv = sys.argv.copy()
    original_env = os.environ.get('LOGS_DIR')
    
    try:
        # Create a temp directory that actually exists
        with tempfile.TemporaryDirectory() as temp_dir:
            sys.argv = ['test', temp_dir]
            if 'LOGS_DIR' in os.environ:
                del os.environ['LOGS_DIR']
            
            logs_dir = get_logs_directory()
            assert str(logs_dir) == temp_dir
        
    finally:
        sys.argv = original_argv
        if original_env:
            os.environ['LOGS_DIR'] = original_env


if __name__ == "__main__":
    # Simple test runner - no fancy framework needed
    test_functions = [
        test_server_exists,
        test_get_logs_directory_default,
        test_get_logs_directory_env_var,
        test_get_logs_directory_cmd_arg
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"✅ {test_func.__name__}")
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__}: {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 All tests passed!")