import csv
from ast import Tuple

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

def split_timestamp(line:str) -> Tuple:
    # Splits the timestamp from the rest of the line.
    timestamp, lineWithoutStamp = line.split("]: ", 1)

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

def parse_log(input_location: str, output_location:str, file_type:str) -> None:
    # Takes an Archipelago log file and converts it into a CSV for analysis.
    with open(input_location, "r") as f:
        lines = f.readlines()
    item_csv = []
    player_csv = []

    for line in lines:
        parsed_line = process_line(line)
        if parsed_line is None:
            continue
        if "event" in parsed_line:
            player_csv.append(parsed_line)
        else:
            item_csv.append(parsed_line)

    if file_type == "both":
        output_location_item = output_location.replace(".csv", "_item.csv")
        output_location_player = output_location.replace(".csv", "_player.csv")
        write_output(output_location_item, item_csv, ["timestamp", "team", "item", "location", "sender", "receiver"])
        write_output(output_location_player, player_csv, ["timestamp", "event", "player", "player_team"])
    elif file_type == "item":
        write_output(output_location, item_csv, ["timestamp", "team", "item", "location", "sender", "receiver"])
    elif file_type == "player":
        write_output(output_location, player_csv, ["timestamp", "event", "player", "player_team"])

def write_output(output_location: str, data: list, fieldnames: list) -> None:
    with open(output_location, "w", newline="", encoding="UTF-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for line in data:
            writer.writerow(line)

    
