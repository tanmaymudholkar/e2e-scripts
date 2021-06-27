from __future__ import print_function, division

import json

class Settings:
    def __init__(self, source_file_path):
        self.source_file_path_ = source_file_path
        self.values_ = None
        with open(self.source_file_path_, 'r') as source_file_handle_:
            self.values_ = json.load(source_file_handle_)

    def __str__(self):
        return str(self.values_)

    def __repr__(self):
        return "Instance of class Settings"

    def run_tests(self):
        print("Settings read in from file {sfp}:".format(sfp=self.source_file_path_))
        print(self)
        print("All done!")

if __name__ == "__main__":
    settings = Settings("settings.json")
    settings.run_tests()
