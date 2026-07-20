"""
Tests track info loading.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from src.ruleset_info import RuleSetInfo

def test_loads_first():
    loaded_info = RuleSetInfo.load_track_by_name("sbes_26_rt", True)
    assert loaded_info.get_track_header() == "SBES’26, September 08–12, 2026, São Paulo, SP"

def test_loads_second():
    loaded_info = RuleSetInfo.load_track_by_name("sbes_24_nier", True)
    assert loaded_info.get_track_header() == "SBES’24, September 30 – October 04, 2024, Curitiba, PR"