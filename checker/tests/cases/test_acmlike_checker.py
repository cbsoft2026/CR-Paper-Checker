"""
Tests for the ACMLike paper checker.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from src.parsed_paper import ParsedPaper
from src.acmlike_checker import ACMLikeChecker


ACM_REF_FORMAT_MOCK_PATH = "/data/acm_ref_format.pdf"
ACM_FOOTNOTE_MOCK_PATH = "/data/acm_footnote.pdf"
ACM_CCS_CONCEPTS_MOCK_PATH = "/data/acm_ccs_concepts.pdf"


def test_acm_ref_format(): 

    ref_paper = ParsedPaper.from_pdf(ACM_REF_FORMAT_MOCK_PATH)
    footnote_paper = ParsedPaper.from_pdf(ACM_FOOTNOTE_MOCK_PATH)

    checker = ACMLikeChecker()

    ref_results = checker.check_paper(ref_paper)
    footnote_results = checker.check_paper(footnote_paper)

    assert not ref_results["acm_ref_format"]
    assert footnote_results["acm_ref_format"]

def test_acm_footnote():

    ref_paper = ParsedPaper.from_pdf(ACM_REF_FORMAT_MOCK_PATH)
    footnote_paper = ParsedPaper.from_pdf(ACM_FOOTNOTE_MOCK_PATH)

    checker = ACMLikeChecker()

    ref_results = checker.check_paper(ref_paper)
    footnote_results = checker.check_paper(footnote_paper)

    assert ref_results["acm_footnote"]
    assert not footnote_results["acm_footnote"]

def test_acm_ccs_concepts():
    footnote_paper = ParsedPaper.from_pdf(ACM_FOOTNOTE_MOCK_PATH)
    ccs_concepts_paper = ParsedPaper.from_pdf(ACM_CCS_CONCEPTS_MOCK_PATH)

    checker = ACMLikeChecker()

    footnote_results = checker.check_paper(footnote_paper)
    ccs_concepts_results = checker.check_paper(ccs_concepts_paper)

    assert footnote_results["acm_ccs_concepts"]
    assert not ccs_concepts_results["acm_ccs_concepts"]