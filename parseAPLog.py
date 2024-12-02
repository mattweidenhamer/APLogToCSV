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


def preprocess_line(line: str) -> str:
    # Filters unneccesary lines from the log file.

    # Ignore the line if it isn't timestamped (such as commands)
    if not line.startswith("["):
        return None

def split_timestamp(line:str) -> Tuple[str, str]:
    # Splits the timestamp from the rest of the line.
    timestamp, lineWithoutStamp = line.split("]:  ", 1)

    # Chop off the leading bracket on time stamp
    timestamp = timestamp[1:]
    return timestamp, lineWithoutStamp

def parse_notice(notice: str):
    # Parses a notice line into a set of CSV values.

    # Notice CSV file format:
    # Timestamp: When the notice was sent
    # Event: Join, leave, or view.
    # Sender: Who sent the notice
    # Team: The team that the notice is about
    # Example input line: [2024-11-29 05:34:12,250]: Notice (all): surger1 (Team #1) playing Stardew Valley has joined. Client(0.5.0), ['AP'].

    # If the notice is not a join or leave notice, ignore it.
    if "has joined" not in notice and "has left" not in notice:
        return None
    
    

def parse_item_line(item_line: str):
    # Parses an item send line into a set of CSV values.
    # Example input line:
    # (Team #1) Nillsanity sent Gunther <3 to Tair (Level 1 Mining)
    team, item = item_line.split(")", 1)
    team = team[1:]

    # The sender is anything before the "sent" keyword.
    sender, item = item.split(" sent ", 1)

    # The parenthesis at the end contains the location.
    # TODO: Is there a way to have this not break for locations with parenthesis?
    item, location = item.rsplit("(", 1)
    location = location[:-1]

    # The receiver is anything after the "to" keyword.
    item, receiver = item.rsplit(" to ", 1)

    # The item should be the only thing left.
    item = item.strip()
    return {
        "team": team,
        "item": item,
        "location": location,
        "sender": sender,
        "receiver": receiver
    }




def parse_log(input_location: str, output_location:str) -> None:
    # Takes an Archipelago log file and converts it into a CSV for analysis.
    pass


def prompt_for_file() -> None:
    # Prompts the user for the log file they would like to parse.
    file_location = input("Please enter the location of the log file you would like to parse: ")
    file_output = input("Please enter the name of the file to output the CSV to: ")
    parse_log(file_location, file_output)

if __name__ == "__main__":
    prompt_for_file()