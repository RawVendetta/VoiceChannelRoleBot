import fileinput
import re

# Display Pretext
print("Welcome, this script is meant to aid users in changing the variables they need for this repository's bot to work.\nSimply enter the information the program asks and it will set the main bot script up.\n\n")

# Specify the filename of the file to modify
filename = "VoiceChannelRoleBot.py"

# Define the variables to change
variables = [
    "BOT_TOKEN",
    "SERVER_NAME",
    "RULES_CHANNEL",
    "ROLE_NAME",
    "DM_CONTENT"
]

# Read the original file to extract the current values of the variables
current_values = {}
with open(filename, 'r') as file:
    content = file.read()
    for variable in variables:
        match = re.search(rf'{variable}\s*=\s*"([^"]*)"', content)
        if match:
            current_values[variable] = match.group(1)
        else:
            current_values[variable] = ""

# Prompt the user for new values and modify the file
for variable in variables:
    current_value = current_values[variable]
    new_value = input(f'Enter new value for {variable} (current value: "{current_value}"): ')
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            if variable in line:
                line = re.sub(rf'{variable}\s*=\s*"[^"]*"', f'{variable} = "{new_value}"', line)
            print(line, end='')
