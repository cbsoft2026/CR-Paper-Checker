"""
Holds the definition of the RuleSetInfo class. 
"""

import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from src.constants import RULESET_FILE, TEST_RULESET_FILE

class RuleSetInfo():
    """
    Encapsulates info pertaining to track specific data and paper 
     checking configuration for a specific track related to the conferece.
    """

    def load_track_by_name(track_name, testing):
        """
        Creates a new TrackInfor instance loading the info from a 
        """

        new_instance = RuleSetInfo()
        info_path = TEST_RULESET_FILE if testing else RULESET_FILE

        loaded_info = None

        with open(info_path) as track_info_file:
            ruleset_info = json.load(track_info_file)
            track_infos = ruleset_info["tracks"]
            for track_info in track_infos:
                if track_info["name"] == track_name:
                    loaded_info = track_info
                    break
            if loaded_info is None:
                print("No track configuration found for",track_name)
                print("Please refer to the README and choose one of the tracks listed in the ruleset file", info_path[1:])
                exit(1)
            
        new_instance.rule_messages = ruleset_info["rules"]

        if "specific_rules" in loaded_info:
            new_instance.rule_messages = new_instance.rule_messages | loaded_info["specific_rules"]
        
        new_instance.track_name = loaded_info["name"]
        new_instance.track_header = loaded_info["conference_header"]
        new_instance.max_paper_pages = loaded_info["total_page_limit"]
        new_instance.max_content_pages = loaded_info["content_page_limit"]   

        return new_instance

    def get_track_header(self):
        """
        Returns the track header associated with a given track, including conference name and dates.
        """

        return self.track_header

    def get_track_total_pages_limit(self):
        """
        Returns the track's maximum paper length, counting pages dedicated exclusively for references.
        """
        return self.max_paper_pages

    def get_track_content_pages_limit(self):
        """
        Returns the track's maximum paper length (in number of pages) for its main contents, excluding
        references.
        """
        return self.max_content_pages
    
    def get_check_message_if_existent(self, check_key) -> None | str:
        """
        If a given check message is included in the conference's ruleset, returns
        the instructive message that advises what the authors should do to conform to 
        the given check. 

        If the check is absent, returns None.
        """

        return self.rule_messages.get(check_key, None)