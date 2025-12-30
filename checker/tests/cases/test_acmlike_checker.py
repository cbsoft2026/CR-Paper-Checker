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
WRONG_ABSTRACT_KEYWORD = "/data/wrong_abstract.pdf"
WRONG_KEYWORDS_KEYWORD = "/data/wrong_keywords.pdf"
TWO_PARAGRAPHED_ABSTRACT = "/data/wrong_abstract.pdf"
NUMBERED_ARTIFACTS = "/data/mock2.pdf"
ARTIFACTS_BEFORE_CONCLUSION = "/data/artifacts_too_soon.pdf"
ARTIFACTS_AFTER_ACKS = "/data/acks_soon_wrong.pdf"
ARTIFACTS_NO_ACKS = "/data/artifact_ok_no_acks.pdf"
NUMBERED_ACKS = "/data/numbered_acks.pdf"
WRONG_ACKS_KEYWORD = "/data/acks_soon_wrong.pdf"
RECEIVED_ON_MOCK = "/data/acm_received.pdf"
NO_TEMPLATE_MOCK = "/data/acm-interim.pdf"

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

def test_sections_not_uppercase():
    uppercase_sections_paper = ParsedPaper.from_pdf(WRONG_CONF_MOCK_PATH)
    ok_sections_paper = ParsedPaper.from_pdf(ACM_REF_FORMAT_MOCK_PATH)

    checker = ACMLikeChecker()

    uppercase_sections_results = checker.check_paper(uppercase_sections_paper)
    ok_sections_results = checker.check_paper(ok_sections_paper)

    assert not uppercase_sections_results["numbered_sections_lowercase"]
    assert ok_sections_results["numbered_sections_lowercase"]

def test_correct_artifact_sec():
    wrongly_named_paper = ParsedPaper.from_pdf(WRONG_CONF_MOCK_PATH)
    artifacts_ok_paper = ParsedPaper.from_pdf(ACM_REF_FORMAT_MOCK_PATH)
    nubmered_artifacts_paper = ParsedPaper.from_pdf(NUMBERED_ARTIFACTS)

    checker = ACMLikeChecker()

    wrongly_named_results = checker.check_paper(wrongly_named_paper)
    artifacts_ok_results = checker.check_paper(artifacts_ok_paper)
    numbered_artifacts_results =  checker.check_paper(nubmered_artifacts_paper)

    assert not wrongly_named_results["correct_artifact_section"]
    assert not numbered_artifacts_results["correct_artifact_section"]
    assert artifacts_ok_results["correct_artifact_section"]
    

def test_artifact_sec_positioning():
    artifacts_ok_paper = ParsedPaper.from_pdf(LONG_AUTHOR_HEADER)
    artifacts_no_aks_paper =  ParsedPaper.from_pdf(ARTIFACTS_NO_ACKS)
    artifacts_too_soon_paper = ParsedPaper.from_pdf(ARTIFACTS_BEFORE_CONCLUSION)
    artifacts_too_late_paper = ParsedPaper.from_pdf(ARTIFACTS_AFTER_ACKS)

    checker = ACMLikeChecker()

    artifacts_ok_results = checker.check_paper(artifacts_ok_paper)
    artifacts_no_aks_results = checker.check_paper(artifacts_no_aks_paper)
    artifacts_too_soon_results = checker.check_paper(artifacts_too_soon_paper)
    artifacts_too_late_results = checker.check_paper(artifacts_too_late_paper)

    assert artifacts_ok_results["artifact_sec_pos"]
    assert artifacts_no_aks_results["artifact_sec_pos"]
    assert not artifacts_too_soon_results["artifact_sec_pos"]
    assert not artifacts_too_late_results["artifact_sec_pos"]

def test_correct_abstract_keyword():
    wrongly_named_abstract = ParsedPaper.from_pdf(WRONG_ABSTRACT_KEYWORD)
    ok_abstract = ParsedPaper.from_pdf(WRONG_KEYWORDS_KEYWORD)

    checker = ACMLikeChecker()

    wrongly_named_results = checker.check_paper(wrongly_named_abstract)
    ok_results = checker.check_paper(ok_abstract)

    assert not wrongly_named_results["correctly_named_abstract"]
    assert ok_results["correctly_named_abstract"]

def test_one_paragraph_abstract():
    two_paragraphed_abstract = ParsedPaper.from_pdf(TWO_PARAGRAPHED_ABSTRACT)
    ok_abstract = ParsedPaper.from_pdf(WRONG_CONF_MOCK_PATH)

    checker = ACMLikeChecker()

    two_paragraphed_results = checker.check_paper(two_paragraphed_abstract)
    ok_results = checker.check_paper(ok_abstract)

    assert not two_paragraphed_results["one_paragraph_on_abstract"]
    assert ok_results["one_paragraph_on_abstract"]

def test_correct_keywords_keyword():
    wrongly_named_keywords = ParsedPaper.from_pdf(WRONG_KEYWORDS_KEYWORD)
    ok_named_keywords = ParsedPaper.from_pdf(WRONG_ABSTRACT_KEYWORD)

    checker = ACMLikeChecker()

    wrong_keywords_results = checker.check_paper(wrongly_named_keywords)
    ok_keywords_results = checker.check_paper(ok_named_keywords)

    assert not wrong_keywords_results["correctly_named_keywords"]
    assert ok_keywords_results["correctly_named_keywords"]

def test_detects_wrong_acks():
    no_acks_paper = ParsedPaper.from_pdf(ARTIFACTS_NO_ACKS)
    ok_acks = ParsedPaper.from_pdf(ACM_REF_FORMAT_MOCK_PATH)
    numbered_acks = ParsedPaper.from_pdf(NUMBERED_ACKS)
    wrong_acks = ParsedPaper.from_pdf(WRONG_ACKS_KEYWORD)

    checker = ACMLikeChecker()

    no_acks_result = checker.check_paper(no_acks_paper)
    ok_acks_results =  checker.check_paper(ok_acks)
    numbered_acks_results = checker.check_paper(numbered_acks)
    wrong_acks_results = checker.check_paper(wrong_acks )

    assert no_acks_result["correct_acks_title"]
    assert ok_acks_results["correct_acks_title"]
    assert not numbered_acks_results["correct_acks_title"]
    assert not wrong_acks_results["correct_acks_title"]

def test_received_on():
    received_on_paper = ParsedPaper.from_pdf(RECEIVED_ON_MOCK)
    ok_paper = ParsedPaper.from_pdf(LONG_AUTHOR_HEADER)

    checker = ACMLikeChecker()

    received_on_results = checker.check_paper(received_on_paper)
    ok_results = checker.check_paper(ok_paper)

    assert not received_on_results["no_received_on_tags"]
    assert ok_results["no_received_on_tags"]

def test_compiled_with_template():
    no_template_paper = ParsedPaper.from_pdf(NO_TEMPLATE_MOCK)
    template_paper = ParsedPaper.from_pdf(LONG_AUTHOR_HEADER)

    checker = ACMLikeChecker()
    
    no_template_results = checker.check_paper(no_template_paper)
    template_results = checker.check_paper(template_paper)

    assert not no_template_results["acm_latex_template"]
    assert template_results["acm_latex_template"]