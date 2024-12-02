# CSV file format:
# Timestamp, Event, Item, ItemType, Sender, Receiver

from ast import Tuple


def preprocessLine(line: str, priorLine:str = None, nextLine:str = None) -> Tuple[str, str]:
    # Parses a single line into a set of CSV values.
    # Also filters out unneccesary lines.

    # Ignore the line if it isn't timestamped (such as commands)
    if not line.startswith("["):
        return None, None
    
    timestamp, lineWithoutStamp = line.split("]:  ", 1)
    # Chop off the leading bracket on time stamp
    timestamp = timestamp[1:]
    return timestamp, lineWithoutStamp

def parseNotice(line:str, timestamp:str, priorLine:str, nextLine:str):
    # Parses a notice line into a set of CSV values.
    pass

def promptForFile():
    # Prompts the user for the log file they would like to parse.
    pass

def parseLog():
    # Takes an Archipelago log file and converts it into a CSV for analysis.
    pass


if __name__ == "__main__":
    promptForFile()