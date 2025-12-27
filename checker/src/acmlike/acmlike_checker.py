"""
Houses the definition of the ACMLikeChecker class.
"""

import sys
import re
from pathlib import Path
from PIL import ImageFont

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))

from src.parsed_paper import ParsedPaper
from src.acmlike.constants import PAGE_HEADER_FONT, DEFAULT_CONF_HEADER, FONT_DATA_DIR

class ACMLikeChecker():
    """
    Class responsible for checking conformance to a ACM-like
    paper template.

    TODO: Implement config system so tests/checks can be 
    toggled on or off.
    """

    def __init__(self, conf_header=DEFAULT_CONF_HEADER):
        self.conf_header = conf_header

    def check_paper(self, paper: ParsedPaper) -> dict:
        """
        Checks whether a given paper conforms to the checks associated
        with this Template Checker. 
        """

        check_results = {} # For now, saves testing results in a dict structure.

        if paper.get_language() is None:
            check_results["references_section"] = False
            return check_results
        else:
            check_results["references_section"] = True
        
        check_results = check_results | self._check_no_ACM_elements(paper)

        # TODO: Parse authors from title page.

        check_results = check_results | self._check_page_headers(paper)

        ## Check if metadata title matches first page title?
        
        return check_results
    
    def _check_no_ACM_elements(self, paper: ParsedPaper) -> dict:
        """
        Checks whether a paper contains no ACM-exclusive components. Namely,
        we check whether the paper contains
        A) The CCS Concepts section;
        B) The ACM footnote with conf. information at the end of 1st column;
        C) The ACM Reference Format blob.
        """

        first_page = paper.get_all_pages()[0]

        partial_check_results = {}
        partial_check_results["acm_ref_format"] = True
        partial_check_results["acm_footnote"] = True
        partial_check_results["acm_ccs_concepts"] = True

        for line in first_page:
            if line[0] == "ACM Reference Format:":
                partial_check_results["acm_ref_format"] = False
            elif re.search(r"20\d{2}. ACM ISBN [A-Z\d]{3}-[A-Z\d]-[A-Z\d]{4}-[A-Z\d]{4}-[A-Z\d]\/\d{4}\/\d{2}",line[0]) is not None:
                partial_check_results["acm_footnote"] = False
            elif line[0] == "CCS Concepts":
                partial_check_results["acm_ccs_concepts"] = False

        return partial_check_results

    def _check_template_conformance(self, paper: ParsedPaper) -> dict:
        """
        Checks whether a paper was compiled with the acmlike template.
        """
        return {}

    def _check_page_headers(self, paper: ParsedPaper) -> dict:
        """
        Checks whether the paper's page headers contain the correct informations, including:
        A) The left column of odd pages include the paper's short title;
        B) The right column of even pages include the short list of authors;
        C) The remaining columns should contain the date and place the conf. was held in.

        ACM-like column width: ~220'pt'. (Harcoded af, good luck adapting this to another template)
        """

        header_results = {
            "conf_header": False,
            "short_title_header": False,
            "short_authors_header": False,
        }

        even_header_lines,_ = get_page_header_lines(paper,1)
        odd_header_lines, header_font_size = get_page_header_lines(paper,2) # This line assumes we're only treating papers with more than 2 pages

        if len(even_header_lines) == 0 or len(odd_header_lines) == 0:
            return header_results

        conf_index_on_even_page = even_header_lines[0].find(self.conf_header)
        
        #   If it is not found OR is not at the beginning of header;
        #  Purposely left in this redundant form, so future maintainers
        #   can remove the second clause if they so desire.
        if conf_index_on_even_page < 0 or conf_index_on_even_page > 0:
            return header_results
        
        conf_index_on_odd_page = odd_header_lines[-1].find(self.conf_header)

        if conf_index_on_odd_page < 0:
            return header_results

        header_results["conf_header"] = True

        even_header_lines[0] = even_header_lines[0][len(self.conf_header):]
        odd_header_lines[-1] = odd_header_lines[-1][0:conf_index_on_odd_page]

        authors_ok = True
        for line in even_header_lines:
            if is_line_too_long(line,PAGE_HEADER_FONT,header_font_size,220):
                authors_ok = False
                break

        title_ok = True
        for line in odd_header_lines:
            if is_line_too_long(line,PAGE_HEADER_FONT,header_font_size,220):
                title_ok = False
                break
        
        header_results["short_authors_header"] = authors_ok
        header_results["short_title_header"] = title_ok

        return header_results

    def _check_keyword_lang_consistency(self, paper: ParsedPaper) -> dict:
        """
        Checks whether all keywords in a paper are in the same language.
        """
        return {}

def get_page_header_lines(paper: ParsedPaper, page_index: int) -> tuple[list[str],float]:
    """
    Given a ParserPaper object with an acm-like paper, retrieves the header lines
    of a given page, and the font size used.
    """

    page = paper.get_all_pages()[page_index]

    header_lines = []
    size = -1
    for line in page:
        font_info = line[1]
        if font_info is None:
            continue
        
        if font_info["/BaseFont"][8:] == PAGE_HEADER_FONT:
            header_lines.append(line[0])
            size = line[2]
        else:
            break
    
    return header_lines,size

def is_line_too_long(line: str, font_family: str, font_size: float, max_length: float):
    """
    Given a font family name, a string, and a width threshold in pt, 
    checks whether the string in the given font family is shorter than
    the threshold.

    Uses the Pillow image manipulation lib.
    """

    true_font_path = FONT_DATA_DIR + font_family + ".ttf"

    try:
        loaded_font = ImageFont.truetype(true_font_path, int(font_size))
    except OSError:
        raise Exception("Font .ttf not found in the data/fonts dir")
    
    width = loaded_font.getlength(line)

    return width > max_length