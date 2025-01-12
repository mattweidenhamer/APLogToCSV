import csv
from ast import Tuple, parse

def process_line(line: str) -> str:
    # Filters unneccesary lines from the log file.

    # Ignore the line if it isn't timestamped (such as commands)
    if not line.startswith("["):
        return None
    
    if "Notice" in line:
        return parse_notice(line)
    
    # This might be too broad, but it should catch all item send lines.
    if "sent" in line:
        return parse_item_line(line)
    
    print(f"Unhandled line: {line}")
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
    # Event: Join or leave.
    # Player: Who sent the notice
    # Player Team: The team that the sender is on
    # Example input line: [2024-11-29 05:34:12,250]: Notice (all): surger1 (Team #1) playing Stardew Valley has joined. Client(0.5.0), ['AP'].

    # If the notice is not a join or leave notice, ignore it.
    if "has joined" not in notice and "has left" not in notice:
        return None
    
    # By default, ignore the notice if it for a viewer instead of a player.
    if "'TextOnly'" in notice:
        return None
    
    # Split the timestamp from the rest of the line.
    timestamp, notice = split_timestamp(notice)

    # Remove the notice from the line.
    notice = notice.split(":", 1)[1]

    # Divide the playing half and the notice half, to avoid accidental misinterpretation.
    player, game = notice.split(" playing ", 1)

    player, team = player.split(" (Team ", 1)
    player.strip()
    team = team[:-1]
    team.strip()

    # The event is either join or leave.
    event = "join" if "has joined" in game else "leave"
    
    return {
        "timestamp": timestamp,
        "event": event,
        "player": player,
        "player_team": team,
    }

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