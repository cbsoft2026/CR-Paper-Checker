"""
Tests for the ACMLike paper checker.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from src.parsed_paper import ParsedPaper
from src.acmlike.acmlike_checker import ACMLikeChecker


ACM_REF_FORMAT_MOCK_PATH = "/data/acm_ref_format.pdf"
ACM_FOOTNOTE_MOCK_PATH = "/data/acm_footnote.pdf"
ACM_CCS_CONCEPTS_MOCK_PATH = "/data/acm_ccs_concepts.pdf"
WRONG_CONF_MOCK_PATH = "/data/mock2.pdf"
LONG_AUTHOR_HEADER = "/data/long_author_header.pdf"
LONG_TITLE_HEADER = "/data/long_title_header.pdf"
INVALID_AUTHOR_BLOCKS = "/data/acm_invalid_auth_block.pdf"
INVALID_AUTHOR_EMAIL = "/data/acm_missing_email.pdf"

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

def test_acm_conf_header():
    wrong_conf = ParsedPaper.from_pdf(WRONG_CONF_MOCK_PATH)
    ok_conf = ParsedPaper.from_pdf(LONG_AUTHOR_HEADER)

    checker = ACMLikeChecker()

    wrong_results = checker.check_paper(wrong_conf)
    ok_results = checker.check_paper(ok_conf)

    assert not wrong_results["conf_header"]
    assert ok_results["conf_header"]

def test_acm_long_shorttitle_header():
    long_title_header = ParsedPaper.from_pdf(LONG_TITLE_HEADER)
    ok_title_header = ParsedPaper.from_pdf(LONG_AUTHOR_HEADER)

    checker = ACMLikeChecker()

    long_title_results = checker.check_paper(long_title_header)
    ok_title_results = checker.check_paper(ok_title_header)

    assert not long_title_results["short_title_header"]
    assert ok_title_results["short_title_header"]

def test_acm_long_shorauthors_header():
    long_authors_header = ParsedPaper.from_pdf(LONG_AUTHOR_HEADER)
    ok_authors_header = ParsedPaper.from_pdf(LONG_TITLE_HEADER)

    checker = ACMLikeChecker()

    long_authors_results = checker.check_paper(long_authors_header)
    ok_authors_results = checker.check_paper(ok_authors_header)

    assert not long_authors_results["short_authors_header"]
    assert ok_authors_results["short_authors_header"]
   
def test_acm_invalid_author_blocks():
    invalid_author_blocks = ParsedPaper.from_pdf(INVALID_AUTHOR_BLOCKS)
    ok_author_blocks = ParsedPaper.from_pdf(ACM_FOOTNOTE_MOCK_PATH)

    checker = ACMLikeChecker()

    invalid_block_results = checker.check_paper(invalid_author_blocks)
    ok_results = checker.check_paper(ok_author_blocks)

    assert not invalid_block_results["author_blocks"] 
    assert ok_results["author_blocks"] 

def test_acm_author_email():
    invalid_author_email = ParsedPaper.from_pdf(INVALID_AUTHOR_EMAIL)
    ok_author_email = ParsedPaper.from_pdf(ACM_CCS_CONCEPTS_MOCK_PATH)

    checker = ACMLikeChecker()

    invalid_email_results = checker.check_paper(invalid_author_email)
    ok_results = checker.check_paper(ok_author_email)

    assert not invalid_email_results["author_emails"] 
    assert ok_results["author_emails"] 
