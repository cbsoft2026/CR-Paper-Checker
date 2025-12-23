"""
Houses the definition of the ACMLikeChecker class.
"""

import sys
import re
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from src.parsed_paper import ParsedPaper

class ACMLikeChecker():
    """
    Class responsible for checking conformance to a ACM-like
    paper template.

    TODO: Implement config system so tests/checks can be 
    toggled on or off.
    """

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
        
        check_results = self._check_no_ACM_elements(paper,check_results)

        ## Check if title matches first page title?
        
        return check_results
    
    def _check_no_ACM_elements(self, paper: ParsedPaper, partial_check_results: dict) -> dict:
        """
        Checks whether a paper contains no ACM-exclusive components. Namely,
        we check whether the paper contains
        A) The CCS Concepts section;
        B) The ACM footnote with conf. information at the end of 1st column;
        C) The ACM Reference Format blob.
        """

        first_page = paper.get_all_pages()[0]

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

    def _check_template_conformance(self, paper: ParsedPaper, partial_check_results: dict) -> dict:
        """
        Checks whether a paper conforms
        """

    def _check_keyword_lang_consistency(self, paper: ParsedPaper, partial_check_results: dict) -> dict:
        """
        Checks whether all keywords in a paper are in the same language.
        """
        return partial_check_results