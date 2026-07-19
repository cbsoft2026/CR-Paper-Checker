from pypdf import PdfReader
from parsed_paper import ParsedPaper
from acmlike.acmlike_checker import ACMLikeChecker

def main():

    parsed_paper = ParsedPaper.from_pdf("/data/acm_barely_not_ok.pdf")
    checker = ACMLikeChecker("sbes_26_rt")

    _,helpful_message = checker.check_and_compose_instructions(parsed_paper)

    if helpful_message == "":
        print("No problems found with the camera ready version of your paper!")
    else:
        print("Some problems were found with the camera ready version of your paper. Make sure it conforms to the following instructions:\n")
        print(helpful_message)

if __name__ == "__main__":
    main()