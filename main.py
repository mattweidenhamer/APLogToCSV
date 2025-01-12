# Item Send CSV file format:
# Timestamp: When the item was sent
# Team: The team that sent the item
# Item: The actual name of the item sent
# Location: Where the item was found.
# ItemType: Progression, useful, filler, or trap. Will need to be cross-referenced based on the item name in the files.
# Sender: Who sent the item
# Receiver: Who received the item
# example input line: [2024-11-29 06:00:06,786]: (Team #1) Nillsanity sent Gunther <3 to Tair (Level 1 Mining)

from functions import parse_log

def prompt_for_file() -> None:
    # Prompts the user for the log file they would like to parse.
    while(True):
        file_location = input("Please enter the location of the log file you would like to parse: ")
        try:
            with open(file_location, "r") as f:
                break
        except FileNotFoundError:
            print("File path not found. Please try again.")

    while(True):
        file_output = input("Please enter the name of the file to output the CSV to: ")
        if not file_output.endswith(".csv"):
            file_output += ".csv"
        try:
            with open(file_output, "w", newline="") as f:
                break
        except FileNotFoundError:
            print("File path not found. Please try again.")
        except PermissionError:
            print("Permission denied. Please try again.")

    while(True):
        file_type = input("Parse item sends or player actions? (item/player/both):")
        if file_type.lower() in ["item", "player", "both"]:
            break
        else:
            print("Invalid input. Please try again.")

    parse_log(file_location, file_output, file_type.lower())

if __name__ == "__main__":
    prompt_for_file()