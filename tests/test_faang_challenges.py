"""
Unit Tests for FAANG Challenges
-------------------------------
Usage: pytest tests/test_faang_challenges.py

Demonstrates:
- Pytest Fixtures
- Parametrized Testing (Data Driven Tests)
- Testing Custom Data Structures
"""

import pytest
from collections import deque
import sys
import os

# Ensure scripts folder is importable
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from faang_interview_challenges import (
    RateLimiter, 
    validate_config_brackets, 
    top_k_ips,
    Codec, 
    ServiceNode
)

# ==========================================
# 1. TEST RATE LIMITER
# ==========================================
@pytest.fixture
def rate_limiter():
    # 2 requests per 1 second
    return RateLimiter(limit=2, window_seconds=1.0)

def test_rate_limiter_logic(rate_limiter):
    # Time 0.0: Allowed (1/2)
    assert rate_limiter.allow_request(timestamp=100.0) is True
    # Time 0.1: Allowed (2/2)
    assert rate_limiter.allow_request(timestamp=100.1) is True
    # Time 0.2: Blocked (2/2 active)
    assert rate_limiter.allow_request(timestamp=100.2) is False
    
    # Time 1.1: Allowed (First request at 100.0 expired)
    assert rate_limiter.allow_request(timestamp=101.1) is True

# ==========================================
# 2. TEST BRACKET VALIDATOR (Parametrized)
# ==========================================
@pytest.mark.parametrize("input_str,expected", [
    ("{}", True),
    ("{[]}", True),
    ("{[()]}", True),
    ("{[(])}", False), # Mismatch nesting
    ("{[", False),     # Unclosed
    ("}", False),      # No opener
    ("", True),        # Empty is valid
    ("var x = [1, 2];", True) # With text
])
def test_validate_config_brackets(input_str, expected):
    assert validate_config_brackets(input_str) == expected

# ==========================================
# 3. TEST TOP K IPs
# ==========================================
def test_top_k_ips():
    stream = ["10.0.0.1", "10.0.0.2", "10.0.0.1", "10.0.0.3", "10.0.0.2", "10.0.0.1"]
    # 10.0.0.1: 3
    # 10.0.0.2: 2
    # 10.0.0.3: 1
    
    result = top_k_ips(stream, k=2)
    assert result == ["10.0.0.1", "10.0.0.2"]
    
    result_k1 = top_k_ips(stream, k=1)
    assert result_k1 == ["10.0.0.1"]

# ==========================================
# 4. TEST TREE SERIALIZATION
# ==========================================
def test_service_tree_serialization():
    codec = Codec()
    
    # Gateway -> (Auth, DB)
    root = ServiceNode("Gateway", [
        ServiceNode("Auth"),
        ServiceNode("DB")
    ])
    
    serialized = codec.serialize(root)
    assert serialized is not None
    assert "Gateway" in serialized
    
    deserialized = codec.deserialize(serialized)
    assert deserialized.name == "Gateway"
    assert len(deserialized.children) == 2
    assert deserialized.children[0].name == "Auth"
    assert deserialized.children[1].name == "DB"

def test_empty_tree():
    codec = Codec()
    assert codec.deserialize("") is None
    assert codec.deserialize(None) is None
