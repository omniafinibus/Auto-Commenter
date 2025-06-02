import os
import re
from file_extensions import supports_comments
import logging as log

gOutputDirectory = ""
gTargetDirectory = ""

# Function to create an output directory if it doesn't exist
def create_output_directory(outputDirectory):
    global gOutputDirectory
    # Update the global variable that holds the output directory path
    gOutputDirectory = outputDirectory
    
    # Check if the specified output directory exists
    if not os.path.isdir(outputDirectory):
        log.info(f"Creating directory {outputDirectory}")
        os.makedirs(outputDirectory)

# Function to clear and delete all files in an output directory
def clear_output_directory(outputDirectory):
    global gOutputDirectory
    # Log that we're clearing the output directory
    log.debug(f"Clearing output directory: {outputDirectory}")
    
    # Get a list of all items (files + directories) in the target directory
    for file in os.listdir(outputDirectory):
        log.debug(f"Processing file: {file}")
        
        # Build the full path to the current item
        filePath = os.path.join(outputDirectory, file)
        
        # If it's a directory that contains other files
        if os.path.isdir(filePath):
            # Check if there are any files inside this directory
            if os.listdir(filePath):
                log.debug(f"Recursively clearing subdirectory: {filePath}")
                clear_output_directory(filePath)
                log.info(f"Removing file " + file.replace(gOutputDirectory, ""))
        if os.path.isdir(file):
            log.info(f"\tDeleting: {file}")
            os.removedirs(file)
        elif os.path.isfile(file):
            log.info(f"\tDeleting: {file}")
            os.remove(file)        
        

# Function to set the target directory for processing
def set_target_directory(targetDirectory):
    global gTargetDirectory
    # Log that we're setting a new target directory
    log.debug(f"Setting target directory to: {targetDirectory}")
    
    # Update the global variable with the new target directory path
    gTargetDirectory = targetDirectory

# Function to get all files matching exclusion criteria from a source directory
def get_files(sourceDirectory, lExclude, rExclude):
    excludeRe = rf'({"|".join(lExclude + [rExclude])})'
    sFiles = set()
    
    # Calculate the local directory by removing the target directory prefix
    localDirectory = sourceDirectory.replace(gTargetDirectory, "")
    if re.findall(excludeRe, localDirectory):
        return sFiles
    
    for file in os.listdir(sourceDirectory):
        filePath = os.path.join(sourceDirectory, file)
        
        # Skip directories
        if os.path.isdir(filePath):
            log.debug(f"Skipping directory: {filePath}")
            
            # Recursively process subdirectories only if they don't match exclusions
            if not re.findall(excludeRe, localDirectory):
                sFiles = sFiles.union(get_files(filePath, lExclude, rExclude))
        elif os.path.isfile(filePath) and supports_comments(filePath):
                if not re.findall(excludeRe, localDirectory):
                    sFiles.add(filePath)
    
    return sFiles

# Function to create a new file in an output directory
def create_file(outputDirectory, sourceDirectory, targetFile, content=""):
    # Replace the source directory prefix from the target path
    targetFile = targetFile.replace(sourceDirectory, "")
    
    # Split the target file path into components for constructing temporary paths
    lFileTree = re.split(r'\\|/', targetFile)
    
    log.debug(f"Temporary file tree: {lFileTree}")
    
    if len(lFileTree) > 1:
        # Create temporary folder(s) at the beginning of the target path
        tempDir = os.path.join(outputDirectory, *lFileTree[:-1])
        log.debug(f"Creating temporary directory: {tempDir}")
        
        # Create the directories if they don't exist
        if not os.path.isdir(tempDir):
            log.debug(f"Creating temporary directory: {tempDir}")
            os.makedirs(tempDir)
            
    # Construct the full path for the new file
    finalPath = os.path.join(outputDirectory, *lFileTree)
    
    log.debug(f"Final target path to create: {finalPath}")
    
    # Create and write content to the new file
    with open(finalPath, "w") as file:
        log.debug(f"Writing content to file: {finalPath}")
        file.write(content)
        
    return finalPath
