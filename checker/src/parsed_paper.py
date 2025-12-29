"""
Module defining the ParsedPaper class and the associated PaperParsingException class.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from enum import Enum
from pypdf import PdfReader

from src.locale_keywords import LANGUAGES

class ParsedPaper():
    """
    Class responsible for representing a single paper, condensing 
    the data that has been parsed and will be used for conformance
    checking. 
    """

    @staticmethod
    def from_pdf(pdf_path: str):

        reader = PdfReader(pdf_path)

        new_parsed_paper = ParsedPaper()
        new_parsed_paper.path_to = pdf_path
        new_parsed_paper.num_pages = len(reader.pages)
        new_parsed_paper.title = reader.metadata.title
        new_parsed_paper.creator = reader.metadata.creator

        parsed_outline = []
        for outline_item in reader.outline:
            if isinstance(outline_item,list):
                continue
            parsed_outline.append(outline_item.get("/Title","ERROR_PARSING_OUTLINE_ITEM"))

        new_parsed_paper.outline = parsed_outline

        pages = []
        for page in reader.pages:
            parsed_page = []
            page.extract_text(visitor_text=lambda text, cm, tm, font_dict, font_size: 
                              parsed_page.append((text, font_dict,font_size)))
            pages.append(parsed_page)

        new_parsed_paper.pages = pages

        new_parsed_paper._detect_language()

        return new_parsed_paper

    def _detect_language(self) -> Enum | None:
        """
        Detects the language the paper is written in based on the language 
        of its 'References' keyword.

        This heuristic assumes that every paper has an unnumbered 'References'
        secion present in the paper's outline.

        If no language is detected, returns None.
        """

        return self.update_language_from_outline(self.get_outline())

    def update_language_from_outline(self,outline: list[str]) -> Enum | None:
        """
        Detects the language the paper is written in based on a given
         list of paper sections, and looking for the language of its 
        'References' keyword.

        This heuristic assumes that every paper has an unnumbered 'References'
        secion present in the paper's outline.

        If no language is detected, returns None.
        """
        for language in LANGUAGES:
            for outline_item in outline:
                if language.REFERENCES.value == str(outline_item).upper():
                    self.language = language
                    return language
        self.language = None
        
    def get_language(self) -> Enum | None:
        """
        Returns the language used in the paper's keywords.
        """
        return self.language

    def get_num_pages(self) -> int:
        """
        Returns the paper's total number of pages.
        """

        return self.num_pages
    
    def get_title(self) -> str:
        """
        Returns the paper's title as extracted from its metadata.
        """
        return self.title
    
    def get_creator(self) -> str:
        """
        Returns the paper's creator as extracted from its metadata.
        """
        return self.creator
    
    def get_outline(self) -> list | tuple[list[str],list[tuple[int,int]]]:
        """
        Returns a list with the highest order PDF outline items (Chapters/Sections)
         in the order they appear in the paper. Note that subchapters/subsections are NOT
        captured. 
        """

        return self.outline
    
    def get_all_pages(self) -> list:
        """
        Returns a list where, for every page in the paper, every line is parsed onto a tuple
        containing the line text, a dict with font info, and a third value with font size.
        """

        return self.pages