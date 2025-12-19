"""
Module defining the ParsedPaper class.
"""

from pypdf import PdfReader

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

        return new_parsed_paper

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
    
    def get_outline(self) -> list:
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