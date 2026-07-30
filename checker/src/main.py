import os
import pandas as pd
from parsed_paper import ParsedPaper
from acmlike.acmlike_checker import ACMLikeChecker

def main():
    track = os.environ["TRACK"]

    single_paper = os.environ.get("CHECK_PAPER_AT")
    paper_batch = os.environ.get("CHECK_PAPERS_AT")
    debug_paper = os.environ.get("DEBUG_PAPER_AT")
    
    checker = ACMLikeChecker(track)

    if single_paper is not None:
        check_single_paper(checker,single_paper)
    elif paper_batch is not None:
        check_paper_batch(checker,paper_batch)
    elif debug_paper is not None:
        debug_paper_checking(checker,debug_paper)
    else:
        print("Please refer to the README file for instructions on how to invoke the checker script.")
    

def check_single_paper(checker, paper_path):
    """
    Checks whether a single paper conforms to the restrictions of a track.
    """
    parsed_paper = ParsedPaper.from_pdf("/data/" + paper_path)

    _,helpful_message = checker.check_and_compose_instructions(parsed_paper)

    if helpful_message == "":
        print("No problems found with the camera ready version of your paper!")
    else:
        print("Some problems were found with the camera ready version of your paper. Make sure it conforms to the following instructions:\n")
        print(helpful_message)

def check_paper_batch(checker, batch_path):
    """
    Checks whether a batch of papers at a given directory conform to the restricitons of a track.
    """

    if batch_path[-1] == "/":
        batch_path = batch_path[:-1]

    all_papers = os.listdir("/data/"+batch_path)
    all_results = []

    for paper_path in  all_papers:
        try:
            parsed_paper = ParsedPaper.from_pdf("/data/" + batch_path + "/" + paper_path)
        except:
            print("Ignoring file", paper_path)
            continue
        print("Checking paper", paper_path)
        
        binary_results, helpful_message = checker.check_and_compose_instructions(parsed_paper)
        composite_results = {"paper": paper_path} | binary_results | {"_message": helpful_message, "_author_emails": parsed_paper.get_author_emails_as_str()}
        all_results.append(composite_results)

    save_batch_results("/data/"+batch_path+"_results.xlsx",all_results)

def save_batch_results(output_path, all_results):
    """
    Saves the results of a given batch of papers checked to a csv file.
    """

    results_df = pd.DataFrame(all_results)
    results_df.to_excel(output_path, index=False, engine='openpyxl')

def debug_paper_checking(checker, paper_path):
    """
    Run the checker on 'debug mode' with the paper in a given path.
    """

    checker.activate_debug_logs()

    parsed_paper = ParsedPaper.from_pdf("/data/" + paper_path)
    
    print(checker.check_paper(parsed_paper))

if __name__ == "__main__":
    main()