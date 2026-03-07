# tests/test_save_pos.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
import save_pos

def test_is_save_position_valid():
    assert save_pos.is_save_position([0.1, 0.2, 0.3]) is True

def test_is_save_position_invalid():
    assert save_pos.is_save_position([10, 20, 30]) is False