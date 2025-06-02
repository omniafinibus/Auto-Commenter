from file_handling import (
    get_files,
    clear_output_directory,
    create_output_directory,
    create_file,
    set_target_directory
)
from comment_parsers import get_code_block, contents_are_equal
from file_extensions import get_file_language
from logger import setup_custom_logger
from ai_client import AiClient
import logging as log
import subprocess
import os
import re

# Some placeholder definitions
BASE_DIRECTORY = "/" + os.path.join(
    "mnt", "extra", "Nextcloud", "Programming", "tools", "Auto-Commenter"
)
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, "temp_files")
TARGET_DIRECTORY = BASE_DIRECTORY
L_EXCLUDE = ["__pycache__"]
R_EXCLUDE = r"\.pyc"
LOG_DIRECTORY = os.path.join(BASE_DIRECTORY, "logs")
MODEL = "deepseek-r1:7b"
HOST = "http://10.0.0.148:11434"
EDITOR = "code"

# Setup logging
gLogger = setup_custom_logger("root", LOG_DIRECTORY, True, log.DEBUG)

# Connect to local AI
client = AiClient(MODEL, HOST)

# Clear local output folder
create_output_directory(OUTPUT_DIRECTORY)
print(f"Do you want to delete all files in {OUTPUT_DIRECTORY}? [y/n]")
if re.findall(r"^[yYe*E*s*S*]$", input()):
    clear_output_directory(OUTPUT_DIRECTORY)

# Scan directory for any files to be commented
set_target_directory(TARGET_DIRECTORY)
sFilesToComment = get_files(TARGET_DIRECTORY, L_EXCLUDE, R_EXCLUDE)

# Loop over each file which can have comments added
for file in sFilesToComment:
    log.debug(f"Starting comment generation for {file}")
    with open(file, "r") as f:
        fileContents = f.read()

    # Start comment generation for a file
    fileLanguage = get_file_language(file)
    response = client.get_response(language=fileLanguage, code=fileContents)
    
    # Parse response to extract new code
    outputText = get_code_block(response.message.content, fileLanguage)

    # Write generated output to local file
    newFile = create_file(OUTPUT_DIRECTORY, TARGET_DIRECTORY, file, outputText)

    # Compare both files to see if functionality has been altered
    contentsAreEqual = contents_are_equal(fileContents, outputText, fileLanguage, re.sub(TARGET_DIRECTORY, "", file))

    # Show the user the updated file
    subprocess.run(f"{EDITOR} \"{file}\"", shell=True)
    subprocess.run(f"{EDITOR} \"{newFile}\"", shell=True)

    # Request for merge
    print(f"Do you want the contents of {newFile} to replace the contents of {file}? [y/n]")
    if re.findall(r"^[yYe*E*s*S*]$", input()):
        log.info(f"\tWriting contents of {newFile} into {file}")
        # Overwrite original file
        with open(file, 'w') as originalFile:
            with open(newFile, 'r') as generatedFile:
                originalFile.write(generatedFile.read())
        log.info(f"\tDeleting {newFile}")
        os.remove(newFile)