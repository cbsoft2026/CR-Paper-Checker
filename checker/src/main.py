from pypdf import PdfReader
from parsed_paper import ParsedPaper
from acmlike.acmlike_checker import ACMLikeChecker

def main():

    parsed_paper = ParsedPaper.from_pdf("/data/acm_barely_not_ok.pdf")
    checker = ACMLikeChecker("sbes_26_rt")

    checker.check_paper(parsed_paper)

if __name__ == "__main__":
    main()