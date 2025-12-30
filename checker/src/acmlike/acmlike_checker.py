"""
Houses the definition of the ACMLikeChecker class.
"""

import sys
import re
from pathlib import Path
from PIL import ImageFont

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))

from src.parsed_paper import ParsedPaper
from src.acmlike.constants import PAGE_HEADER_FONT, DEFAULT_CONF_HEADER, \
    FONT_DATA_DIR, AUTHOR_BLOCK_FONT, SECTION_TITLE_FONT, COLUMN_SIZE, SUBSECTION_FONT_SIZE

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

        paper.outline = extract_acm_paper_outline(paper)
        if paper.get_language() is None:
            paper.update_language_from_outline(paper.get_outline())

        check_results = {} # For now, saves testing results in a dict structure.
        check_results = check_results | self._check_template_conformance(paper)

        if paper.get_language() is None or not check_results["acm_latex_template"]:
            check_results["references_section"] = False
            return check_results
        else:
            check_results["references_section"] = True
        
        check_results = check_results | self._check_no_ACM_elements(paper)
        check_results = check_results | self._check_author_blocks(paper)
        check_results = check_results | self._check_page_headers(paper)
        check_results = check_results | self._check_paper_outline(paper)
        check_results = check_results | self._check_abstract(paper)
        check_results = check_results | self._check_no_received_on_tags(paper)
        ## Check if metadata title matches first page title?
        
        return check_results
    
    def _check_template_conformance(self, paper: ParsedPaper) -> dict:
        """
        Checks whether a paper was compiled with the acmlike template, and without the
        'review' tag, which interferes with the remainder of the paper checking proccess.
        
        In the future, it might be interesting to add a min. version to the template
        """

        if re.match(r"LaTeX with acmart",paper.get_creator()) is None:
            return {"acm_latex_template" : False,
                    "acm_not_review": True}
        else:
            first_lines = paper.get_all_pages()[0][:3]
            compiled_on_review = False
            if first_lines[1][0][0] == '1' and first_lines[2][0][0] == '2':
                compiled_on_review = True
            return {"acm_latex_template" : True,
                    "acm_not_review": not compiled_on_review}

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

    def _check_author_blocks(self, paper: ParsedPaper) -> dict:
        """
        Checks whether the paper's authors are split into separate blocks,
        each with the author's email address.

        TODO: Also parse and save authors from title page into Paper object.
        """

        partial_results = {
            "author_blocks" : True,
            "author_emails" : True,
        }

        first_page = paper.get_all_pages()[0]

        authors_extracted = extract_authors_from_page_lines(first_page)
        
        if len(authors_extracted) == 0:
            partial_results["author_blocks"] = False
            partial_results["author_emails"] = False
        else:
            for author_dict in authors_extracted:
                if ',' in author_dict["name"] or 'anonymous' in author_dict["name"].lower():
                    partial_results["author_blocks"] = False
                found_email = False
                for info_line in author_dict["info"]:
                    if re.match(r'[^@]+@[^@]+\.[^@]',info_line) is not None:
                        found_email = True
                if not found_email:
                    partial_results["author_emails"] = False

        return partial_results

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
            if compute_line_length(line,PAGE_HEADER_FONT,header_font_size) > COLUMN_SIZE:
                authors_ok = False
                break

        title_ok = True
        for line in odd_header_lines:
            if compute_line_length(line,PAGE_HEADER_FONT,header_font_size) > COLUMN_SIZE:
                title_ok = False
                break
        
        header_results["short_authors_header"] = authors_ok
        header_results["short_title_header"] = title_ok

        return header_results

    def _check_paper_outline(self,paper: ParsedPaper) -> dict:
        """
        Checks if the paper outline respects section name formatting and contains
        the sections in the correct order.
        """

        outline_results = {
            "numbered_sections_lowercase": True,
            "correct_artifact_section" : False,
            "correctly_named_abstract" : False,
            "correctly_named_keywords": False,
            "artifact_sec_pos": False,
            "correct_acks_title": True 
        }

        outline_titles,_ = paper.get_outline() 
        paper_language = paper.get_language()
        acks_index = -1
        arifact_index = -1

        if paper_language is None:
            return outline_results
        
        for item_index in range(len(outline_titles)):
            item = outline_titles[item_index]
            first_char = item[0]
            try:
                _ = int(first_char)
                # In this case, we're in a numbered section
                word_by_word = item.split(' ')
                not_numbered = ' '.join(word_by_word[1:])
                if not_numbered == not_numbered.upper():
                    outline_results["numbered_sections_lowercase"] = False

                if not_numbered == paper_language.ACKS.value or \
                    not_numbered in paper_language.WRONG_ACKS.value: 

                    outline_results["correct_acks_title"] = False
                    acks_index = item_index
                elif not_numbered == paper_language.ARTIFACTS.value or \
                    not_numbered in paper_language.WRONG_ARTIFACTS.value:

                    arifact_index = item_index
            except:
                if acks_index == -1 and item == paper_language.ACKS.value:
                    acks_index = item_index
                elif acks_index == -1 and item in paper_language.WRONG_ACKS.value:
                    outline_results["correct_acks_title"] = False
                    acks_index = item_index
                elif arifact_index == -1 and item == paper_language.ARTIFACTS.value:
                    outline_results["correct_artifact_section"] = True
                    arifact_index = item_index
                elif arifact_index == -1 and item in paper_language.WRONG_ARTIFACTS.value:
                    arifact_index = item_index
        
        if arifact_index > -1:
            if acks_index > -1:
                if acks_index != arifact_index + 1: # Artifact must precede acks
                    outline_results["artifact_sec_pos"] = False
                else:
                    # And acks must precede refs
                    acks_followed_by_refs = outline_titles[acks_index+1] == paper_language.REFERENCES.value
                    outline_results["artifact_sec_pos"] = acks_followed_by_refs
            else: #If there are no acks, the artifact must be the last section here
                artifact_followed_by_refs = outline_titles[arifact_index+1] == paper_language.REFERENCES.value
                outline_results["artifact_sec_pos"] = artifact_followed_by_refs

        outline_results["correctly_named_abstract"] = paper_language.ABSTRACT.value in outline_titles
        outline_results["correctly_named_keywords"] = paper_language.KEYWORDS.value in outline_titles
        return outline_results

    def _check_abstract(self, paper: ParsedPaper) -> dict:
        """
        Checks whether the paper is correctly organized into a single paragraph, and also
        whether or not there is a link at the end of the abstract (useful for tracks
        that require video demos / tool links).

        Watch-out. This implementation gives of plenty of false positives, since there's no
        easy way of detecting a new paragraph. If any line of the abstract ends in a '.\\n'
        combo, this alert will be triggered.
        """

        _, pos_outlines = paper.get_outline()
        abstract_start = pos_outlines[0][1]#This is kinda risky, but it should be language inespecific;
        abstract_end = pos_outlines[1][1]

        abstract_lines = paper.get_all_pages()[0][abstract_start+2:abstract_end-1]
        last_lines = abstract_lines[-3:]

        one_single_paragraph = True

        for line in abstract_lines[:-3]:
            line_text = line[0]
            font_family = line[1]["/BaseFont"][8:]
            font_size = line[2]
            if line_text[-1] == "\n" and line_text[-2] == "." and \
                compute_line_length(line_text,font_family,font_size) < 0.9*COLUMN_SIZE: # This should false positives
                one_single_paragraph =  False
                break
        
        link_on_abstract = False
        for line in last_lines:
            line_text = line[0]
            if "https://" in line_text:
                link_on_abstract = True
                break

        return {"one_paragraph_on_abstract" : one_single_paragraph, "abstract_link": link_on_abstract}

    def _check_no_received_on_tags(self, paper: ParsedPaper) -> dict:
        """
        Checks whether the paper has no 'Received <date>' tags. Equivalent
        tags, such as "Revised" and "Accepted" are also tested.
        This method leverages the fact that these tags are usually left at 
        the end of the last column, on the last page of the manuscript. 
        """

        last_page = paper.get_all_pages()[-1]
        last_line  =  last_page[-1][0]

        if len(re.findall(r"(([Rr]eceived)|([Aa]ccepted)|([Rr]evised))",last_line)) > 0:
            return {"no_received_on_tags": False}

        return {"no_received_on_tags": True}

def extract_authors_from_page_lines(page_lines: list[tuple[str,dict,float]]) -> list[dict]:
    """
    Given a list of tuples corresponding to lines of a page, collects author info.
    For each author, a dict is created containing two keys: name, and info.

    Based on the following heuristic:
    Author information in a ACM-like paper is parsed in the following format: 
    
    Paper Title [on LinLibertineTB]
        {for every author} [all on LinLibertineT]
        \n 
        Author Name
        \n
        Author Affiliation
        Author City/Country
        Author email
    ABSTRACT [on LinLibertineTB]
    """

    authors_read = []
    line_index = 2 # Jump first (empty) line and (maybe) paper title
    while line_index < len(page_lines):
        this_line = page_lines[line_index]
        line_text = this_line[0]
        font_family = this_line[1]["/BaseFont"][8:]

        if font_family == AUTHOR_BLOCK_FONT:
            if line_text == "\n":
                line_index +=1
                continue
            next_line = page_lines[line_index]
            if font_family != AUTHOR_BLOCK_FONT:
                break
            authors_read.append({
                "name" : next_line[0],
                "info" : []
            })

            line_index = line_index + 2 # Skipping newline here
            while page_lines[line_index][0] != "\n":
                authors_read[-1]["info"].append(page_lines[line_index][0])
                line_index += 1
            line_index -= 1
            
        elif len(authors_read) > 0:
            # In this case, I have read an author block and now it has come to an end
            break
            
        line_index += 1

    return authors_read

def extract_acm_paper_outline(paper: ParsedPaper) -> tuple[list[str],list[tuple[int,int]]]:
    """
    Given a paper in an ACM-like format, extracts its outline containing
    every section, subsection and the page it appears on.
    """
    
    outline_titles = []
    outline_pages = [] 
    pages = paper.get_all_pages()
    for page_index in range(len(pages)): 
        page = pages[page_index]
        for line_index in range(len(page)):
            line = page[line_index]
            line_text = line[0]
            font_info = line[1]
            if font_info is None or len(line_text) < 2:
                continue
            if font_info["/BaseFont"][8:] == SECTION_TITLE_FONT and line[2] > SUBSECTION_FONT_SIZE:
                outline_titles.append(line_text)
                outline_pages.append((page_index,line_index))

    return outline_titles,outline_pages

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

def compute_line_length(line: str, font_family: str, font_size: float) -> float:
    """
    Given a font family name, a string and a font-size, computes the string length
     in the given font family.

    Uses the Pillow image manipulation lib.
    """

    true_font_path = FONT_DATA_DIR + font_family + ".ttf"

    try:
        loaded_font = ImageFont.truetype(true_font_path, int(font_size))
    except OSError:
        raise Exception("Font .ttf not found in the data/fonts dir")
    
    width = loaded_font.getlength(line)

    return width