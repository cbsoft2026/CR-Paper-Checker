"""
Holds the definition of the TrackInfo class. 
"""

import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from src.constants import TRACKS_INFO_FILE

class TrackInfo():
    """
    Encapsulates info pertaining to track specific data for a specific 
    track related to the conferece.
    """

    def load_track_by_name(track_name):
        """
        Creates a new TrackInfor instance loading the info from a 
        """

        new_instance = TrackInfo()
        loaded_info = None

        with open(TRACKS_INFO_FILE) as track_info_file:
            track_infos = json.load(track_info_file)
            for track_info in track_infos:
                if track_info["name"] == track_name:
                    loaded_info = track_info
                    break
            if loaded_info is None:
                loaded_info = track_infos[0]
        
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

    def get_total_pages_limit(self):
        """
        Returns the track's maximum paper length, counting pages dedicated exclusively for references.
        """
        return self.max_paper_pages

    def get_content_pages_limit(self):
        """
        Returns the track's maximum paper length (in number of pages) for its main contents, excluding
        references.
        """
        return self.max_content_pages