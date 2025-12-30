from pypdf import PdfReader
from parsed_paper import ParsedPaper
from acmlike.acmlike_checker import ACMLikeChecker

def main():

    parsed_paper = ParsedPaper.from_pdf("/data/link_on_abstract.pdf")
    checker = ACMLikeChecker()

    checker.check_paper(parsed_paper)

if __name__ == "__main__":
    main()