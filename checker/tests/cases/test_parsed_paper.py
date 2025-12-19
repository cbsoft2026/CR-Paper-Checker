"""
Tests for the ParsedPaper class.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from src.parsed_paper import ParsedPaper

WORD_MOCK_PATH = "/data/acm-interim.pdf"
LATEX_MOCK_PATH = "/data/mock1.pdf"

def test_class_exists():
    instance = ParsedPaper()
    assert True

def test_parsed_pdf_basic_info():
    word_mock = ParsedPaper.from_pdf(WORD_MOCK_PATH)
    latex_mock = ParsedPaper.from_pdf(LATEX_MOCK_PATH)

    assert isinstance(word_mock,ParsedPaper)

    assert word_mock.path_to == WORD_MOCK_PATH
    assert latex_mock.path_to == LATEX_MOCK_PATH

    assert word_mock.get_num_pages() == 2
    assert latex_mock.get_num_pages() == 5

    assert word_mock.get_title() == "Insert Your Title Here"
    assert latex_mock.get_title() == "The Name of the Title Is Hope The Name of the Title Is Hope The Name of the Title Is Hope The Name of the Title Is Hope The Name of the Title Is Hope"

    assert word_mock.get_creator() == "Acrobat PDFMaker 25 for Word"
    assert latex_mock.get_creator() == "LaTeX with acmart 2025/05/30 v2.14 Typesetting articles for the Association for Computing Machinery and hyperref 2025-05-20 v7.01m Hypertext links for LaTeX"

    assert latex_mock.get_outline() == ['ABSTRACT', '1 Introduction', '2 Template Overview', '3 Modifications', '4 Typefaces', '5 Title Information', '6 Authors and Affiliations', '7 Sectioning Commands', '8 Tables', '9 Math Equations', '10 Figures', '11 Citations and Bibliographies', '12 Recommendations for Appendices', '13 Conclusion and Future Work', 'REFERENCES', 'A APPENDICES EXAMPLE 1', 'B APPENDICES EXAMPLE 2']

    assert len(latex_mock.get_all_pages()) == 5
    assert len(latex_mock.get_all_pages()[4]) == 156
    assert len(latex_mock.get_all_pages()[4][0]) == 3
