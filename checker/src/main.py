import os
from parsed_paper import ParsedPaper
from acmlike.acmlike_checker import ACMLikeChecker

def main():
    track = os.environ["TRACK"]

    single_paper = os.environ.get("CHECK_PAPER_AT")
    paper_batch = os.environ.get("CHECK_PAPERS_AT")
    
    
    checker = ACMLikeChecker(track)

    if single_paper is not None:
        check_single_paper(checker,single_paper)
    

def check_single_paper(checker, paper_path):
    parsed_paper = ParsedPaper.from_pdf("/data/" + paper_path)

    _,helpful_message = checker.check_and_compose_instructions(parsed_paper)

    if helpful_message == "":
        print("No problems found with the camera ready version of your paper!")
    else:
        print("Some problems were found with the camera ready version of your paper. Make sure it conforms to the following instructions:\n")
        print(helpful_message)

if __name__ == "__main__":
    main()