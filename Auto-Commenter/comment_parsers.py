from copy import deepcopy
import logging as log
import re

# Define patterns for different programming languages' comment syntaxes
RAW_COMMENT_DATA = {
    "Arduino": {r"//": r"\n", r"/\*": r"\*/"},
    "APL": {r"⍝": r"\n", r"⟃": r"⟄", r"\'": r"\' ⊢", r"⊣ \'": r"\'"},
    "Ada": {r"--": r"\n"},
    "AppleScript": {r"--": r"\n", r"#": r"\n", r"\(\*": r"\*\)"},
    "BASIC": {r"\'": r"\n"},
    "Bash": {r"#": r"\n", r"<< \'MULTILINE-COMMENT\'": r"MULTILINE-COMMENT"},
    "C": {r"//": r"\n", r"/\*": r"\*/"},
    "C#": {r"//": r"\n", r"/\*": r"\*/"},
    "C++": {r"//": r"\n", r"/\*": r"\*/"},
    "D": {r"//": r"\n", r"/\*": r"\*/", r"/+": r"+"},
    "Delphi": {r"//": r"\n", r"{r": r"}", r"\(\*": r"\*\)", r"{\*": r"\*}"},
    "Eiffel": {r"--": r"\n"},
    "Fortran": {r"!": r"\n"},
    "Go": {r"//": r"\n", r"/\*": r"\*/"},
    "HTML": {r"<!--": r"-->"},
    "Haskell": {r"--": r"\n"},
    "Java": {r"//": r"\n", r"/\*": r"\*/", r"/\*\*": r"\*/"},
    "JavaScript": {r"//": r"\n", r"/\*": r"\*/"},
    "Julia": {r"#": r"\n", r"#=": r"=#"},
    "Kotlin": {r"//": r"\n", r"/\*": r"\*/"},
    "Lua": {
        r"--": r"\n",
        r"--\[\[": r"\]\]",
        r"--\[=\[": r"--\]=\]",
        r"--\[==\[": r"--\]==\]",
        r"--\[\[": r"--\]\]",
        r"--\[\[": r"--\]\]",
        r"--\[=\[\]\]": r"--\]=\]",
        r"--\[\[": r"--\[=\[\]\]}",
    },
    "MATLAB": {r"%": r"\n", r"%{r": r"%}", r"...": r"..."},
    "Modula-2": {r"\(\*": r"\*\)"},
    "Nim": {r"#": r"\n", r"#\[": r"\]#"},
    "OCaml": {
        r"\(\*": r"\*\)",
        r"\(\*\*": r"\*\)",
        r"\(\*\*/": r"\*\*\)",
        r"\(\*": r"\*\)#",
    },
    "Oberon": {r"\(\*": r"\*\)"},
    "PHP": {r"//": r"\n", r"#": r"\n", r"/\*": r"\*/"},
    "Pascal": {r"\(\*": r"\*\)"},
    "Perl": {r"#": r"\n", r"=": r"=cut"},
    "PowerShell": {r"#": r"\n", r"<#": r"#>"},
    "Python": {r"#": r"\n", r"\"\"\"": r"\"\"\""},
    "R": {r"#", r"\n"},
    "Raku": {
        r"#": r"\n",
        r"#`\(": r"\)",
        r"#`\[": r"\[",
        r"=begincomment": r"=endcomment",
    },
    "Ruby": {r"#": r"\n", r"\"\"\"": r"\"\"\"", r"=begin": r"=end"},
    "Rust": {
        r"//!": r"\n",
        r"/\*!": r"\*/",
        r"//": r"\n",
        r"/\*": r"\*/",
        r"/\*\*": r"\*/",
    },
    "SGML": {r"<!--": r"-->", r"---*": r"--"},
    "SQL": {r"--": r"\n", r"/\*": r"\*/"},
    "Scala": {r"//": r"\n", r"/\*": r"\*/", r"/\*\*": r"\*/"},
    "Swift": {r"//": r"\n", r"/\*": r"\*/"},
    "TypeScript": {r"//": r"\n", r"/\*": r"\*/", r"/\*\*": r"\*/"},
    "VHDL": {r"--": r"\n"},
    "Verilog": {r"//": r"\n", r"/\*": r"\*/"},
    "XML": {r"<!--": r"-->"},
}

""" D_COMMENT_CHARACTERS = {
    "Arduino":      r"//.*$ | /\*(.|\n)*\*/",
    "APL":          r"⍝.*$ | ⟃.*⟄ | ^\'.*\'\s*⊢ | ⊣\'.*\'$",
    "Ada":          r"--.*$",
    "AppleScript":  r"--.*$ | #.*$ | \(\*(.|\n)*\*\)",
    "BASIC":        r"\'.*$",
    "Bash":         r"#.*$ | <<\s*\'MULTILINE-COMMENT\'(.|\n)*MULTILINE-COMMENT",
    "C":            r"//.*$ | /\*(.|\n)*\*/",
    "C#":           r"//.*$ | /\*(.|\n)*\*/",
    "C++":          r"//.*$ | /\*(.|\n)*\*/",
    "D":            r"//.*$ | /\*(.|\n)*\*/ | /\+(.|\n)*\+",
    "Delphi":       r"//.*$ | \{(.|\n)*\} | \(\*(.|\n)*\*\) | \{\*(.|\n)*\*\}",
    "Eiffel":       r"--.*$",
    "Fortran":      r"!.*$",
    "Go":           r"//.*$ | /\*(.|\n)*\*/",
    "HTML":         r"<!--(.|\n)*--\>",
    "Haskell":      r"--.*$",
    "Java":         r"//.*$ | /\*(.|\n)*\*/ | /\*\*(.|\n)*\*\/",
    "JavaScript":   r"//.*$ | /\*(.|\n)*\*/",
    "Julia":        r"#.*$ | #=(.|\n)*=#",
    "Kotlin":       r"//.*$ | /\*(.|\n)*\*/",
    "Lua":          r"--.*$ | --\[=*\[\]*(.|\n)*-*[\]\[=]*",
    "MATLAB":       r"%.*$ | %\{(.|\n)*%\} | \.\.\..*\.\.\.",
    "Modula-2":     r"\(\*(.|\n)*\*\)",
    "Nim":          r"#.*$ | #\[(.|\n)*\]#",
    "OCaml":        r"\(\*.*\*\)$ | \(\*\*.*\*\)$ | \(\*\*/\*\*\)$ | \(\*(.|\n)*\*\)#",
    "Oberon":       r"\(\*.*\*\)",
    "PHP":          r"//.*$ | #.*$ | /\*(.|\n)*\*/",
    "Pascal":       r"\(\*.*\*\)$ | \(\*(.|\n)*\*\)",
    "Perl":         r"#.*$ | =(.|\n)*=cut",
    "PowerShell":   r"#.*$ | <#(.|\n)*#>",
    "Python":       r"#.*$ | \"\"\"(.|\n)*\"\"\"",
    "R":            r"#.*$",
    "Raku":         r"#.*$ | #`\(.*\) | #`\[(.|\n)*\] | =begincomment(.|\n)*=endcomment",
    "Ruby":         r"#.*$s | \"\"\"(.|\n)*\"\"\" | =begin\(.|\n)*\n=end",
    "Rust":         r"//!.*$ | /\*!.\*\*/ | //.*$ | ///.*$ | /\*.*\*/ | /\*\*.*\*/",
    "SGML":         r"<!--(.|\n)*--> | --(.|\n)*--",
    "SQL":          r"--.*$ | /\*(.|\n)*\*/",
    "Scala":        r"//.*$ | /\*(.|\n)*\*/,/\*\*(.|\n)*\*/",
    "Swift":        r"//.*$ | /\*(.|\n)*\*/",
    "TypeScript":   r"//.*$ | /\*(.|\n)*\*/,/\*\*(.|\n)*\*/",
    "VHDL":         r"--.*$",
    "Verilog":      r"//.*$ | /\*(.|\n)*\*/",
    "XML":          r"<!--(.|\n)*-->"
}
"""


def remove_comments(text, language):
    """
    Removes comments from a given text based on the specified programming language.

    Args:
        text (str): The input text containing comments to be removed
        language (str): The programming language whose comment syntax is being used

    Returns:
        str: Text with comments removed for the specified language
    """
    text = deepcopy(text)
    if language not in RAW_COMMENT_DATA.keys():
        log.warning(f'language "{language}" is not supported')
        return text

    # Get all possible comment starts and their corresponding syntaxes
    lStartIndex = get_comment_indices(text, language)

    # Sort indices to handle nested comments properly
    lStartIndex.sort(key=lambda x: x[0], reverse=True)
    log.info(
        f"The comment parser has found {len(lStartIndex)} comment" + "s"
        if len(lStartIndex) != 1
        else ""
    )
    log.info(f"Starting clearing process")

    for i, start in enumerate(lStartIndex, 1):
        startIndex, startSyntax = start
        log.info(f"\tRemoving comment {i}/{len(lStartIndex)}")
        text = remove_comment(startIndex, startSyntax, text, language)

    return text


def remove_comment(startIndex, startSyntax, text, language):
    """
    Removes a single comment from the given text based on its starting index and syntax.

    Args:
        startIndex (int): The starting index of the comment
        startSyntax (str): The regex pattern that identifies the comment start
        text (str): The input text containing the comment to be removed
        language (str): The programming language whose comment syntax is being used

    Returns:
        str: Text with the specified comment removed
    """
    stopSyntax = RAW_COMMENT_DATA[language][startSyntax]
    iFoundMatches = list(re.finditer(stopSyntax, text))
    if not iFoundMatches:
        log.warning(
            f"\tDid not find match for start syntax: {startSyntax} at position {startIndex}"
        )
        return text
    stopIndex = iFoundMatches[-1].end()
    # Skip the next line character to avoid layout issues
    if re.findall(r"\n$", stopSyntax):
        stopIndex -= 1
    return remove_string(startIndex, stopIndex, text)


def get_comment_indices(text, language):
    """
    Finds all comment starts in the given text for a specified programming language.

    Args:
        text (str): The input text to search for comments
        language (str): The programming language whose comment syntax is being used

    Returns:
        list: List of tuples containing start index and syntax for each comment found
    """
    # Get sorted list of possible comment starts based on length
    lStartSyntax = sorted(
        RAW_COMMENT_DATA[language].keys(), key=lambda start: len(start)
    )

    # Find all matches of the comment syntaxes
    dStartIndex = {
        i.start(): syntax for syntax in lStartSyntax for i in re.finditer(syntax, text)
    }

    # Return list of indices sorted by position (descending to handle nested comments)
    return [(index, syntax) for index, syntax in dStartIndex.items()]


def remove_string(start, stop, string):
    """
    Removes the substring from start to stop (exclusive) from the given string.

    Args:
        start (int): The starting index of the substring to remove
        stop (int): The ending index of the substring to remove
        string (str): The input string from which to remove the substring

    Returns:
        str: String with specified substring removed
    """
    return string[:start] + string[stop + 1 :]


def get_code_block(responseMessage: str, language: str):
    """
    Extracts and returns a code block from a response message.

    Args:
        responseMessage (str): The input response message containing code blocks
        language (str): The programming language of the extracted code

    Returns:
        str: Cleaned-up code block without surrounding
    """
    outputText = re.sub(r"<think>(.|\n)*</think>", "", responseMessage)

    # Parse response to extract new code
    outputText = re.split(r"```", outputText)[1]

    return re.sub(f"{language.lower()}\n", "", outputText, 1)


def contents_are_equal(oldFileContents, newFileContents, fileLanguage, directory):
    """
    Check if 2 file contents are the same

    Args:
        oldFileContents (str): Contents from the original file
        newFileContents (str): Contents from the new file
        fileLanguage (str): Language of the file
        directory (str): Directory of the original file

    Returns:
        bool: If the contents are equal or not
    """
    newText = remove_comments(newFileContents, fileLanguage)
    newFormattedText = re.sub(r"\s*", "", newText)
    oldText = remove_comments(oldFileContents, fileLanguage)
    oldFormattedText = re.sub(r"\s*", "", oldText)

    if not newFormattedText == oldFormattedText:
        log.critical(f"File {directory} has different semantics")
        return False
    else:
        log.info(f"File {directory} has the same semantics as the original")
        return True
