# Item Send CSV file format:
# Timestamp: When the item was sent
# Team: The team that sent the item
# Item: The actual name of the item sent
# Location: Where the item was found.
# ItemType: Progression, useful, filler, or trap. Will need to be cross-referenced based on the item name in the files.
# Sender: Who sent the item
# Receiver: Who received the item
# example input line: [2024-11-29 06:00:06,786]: (Team #1) Nillsanity sent Gunther <3 to Tair (Level 1 Mining)

import csv
from ast import Tuple, parse
from functions import process_line, parse_notice, split_timestamp

def prompt_for_file() -> None:
    # Prompts the user for the log file they would like to parse.
    while(True):
        file_location = input("Please enter the location of the log file you would like to parse: ")
        try:
            with open(file_location, "r") as f:
                break
        except FileNotFoundError:
            print("File path not found. Please try again.")

    file_output = input("Please enter the name of the file to output the CSV to: ")
    if not file_output.endswith(".csv"):
        file_output += ".csv"
    parse_log(file_location, file_output)

if __name__ == "__main__":
    prompt_for_file()