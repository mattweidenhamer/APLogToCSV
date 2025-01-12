import csv
from ast import Tuple

ITEM_FIELDNAMES = ["timestamp", "team", "item", "location", "sender", "receiver"]
PLAYER_FIELDNAMES = ["timestamp", "event", "player", "player_team"]

unhandled_lines = []

def process_line(line: str) -> str:
    # Filters unneccesary lines from the log file.

    # Ignore the line if it isn't timestamped (such as commands)
    if not line.startswith("["):
        return None
    
    if "Notice" in line:
        return parse_notice(line)
    
    # This might be too broad, but it should catch all item send lines.
    if "(Team " in line:
        return parse_item_line(line)
    
    unhandled_lines.append(line)    
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
    if " playing " in notice:
        player, game = notice.split(" playing ", 1)
    elif " has left " in notice:
        player, game = notice.split(" has left ", 1)
    else: 
        print(f"Unhandled line in notice phase: {notice}")
        unhandled_lines.append(notice)
        return None

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
    timestamp, item_line = split_timestamp(item_line)
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

    player_output_writer = None
    item_output_writer = None
    player_output_file = None
    item_output_file = None

    if file_type in ["both", "player"]:
        output_location_player = output_location
        if file_type == "both":
            output_location_player = output_location.replace(".csv", "_player.csv")
        player_output_file = open(output_location_player, "w", newline='', encoding="UTF-8")
        player_output_writer = csv.DictWriter(player_output_file, fieldnames=PLAYER_FIELDNAMES)
        player_output_writer.writeheader()
    if file_type in ["both", "item"]:
        output_location_item = output_location
        if file_type == "both":
            output_location_item = output_location.replace(".csv", "_item.csv")
        item_output_file = open(output_location_item, "w", newline='', encoding="UTF-8")
        item_output_writer = csv.DictWriter(item_output_file, fieldnames=ITEM_FIELDNAMES)
        item_output_writer.writeheader()

    output_counter = 0
   
    with open(input_location, "r") as f:
        for line in f:
            parsed_line = process_line(line)
            if parsed_line is None:
                continue
            if "event" in parsed_line:
                player_output_writer.writerow(parsed_line)
                output_counter += 1
            elif "item" in parsed_line:
                item_output_writer.writerow(parsed_line)
                output_counter += 1
            else:
                print(f"Unhandled line in parsing phase: {parsed_line}")
                unhandled_lines.append(parsed_line)

    if player_output_file is not None:
        player_output_file.close()
    if item_output_file is not None:
        item_output_file.close()

    print(f"Successfully wrote {output_counter} lines to associated file(s).")
    if len(unhandled_lines) > 0:
        print("Some lines were unhandled. Unhandled lines:")
        for line in unhandled_lines:
            print(line)