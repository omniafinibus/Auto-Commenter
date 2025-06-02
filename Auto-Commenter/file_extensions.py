# Import necessary modules
import logging as log  # Log messages for debugging purposes
import re  # Regular expressions for file extension matching

# Define mappings of file extensions to programming languages
D_FILE_EXTENSIONS = {
    "ino": "Arduino",
    "c": "C",        # Maps C and C++ extensions
    "h": "C",        
    "cpp": "C++",
    "cc": "C++",
    "cxx": "C++",
    "C++": "C++",
    "hpp": "C++",
    "hh": "C++",
    "hxx": "C++",
    "h++": "C++",
    "cs": "C#",       # Maps C# extensions
    "d": "D",        # Delphi and Dart extensions
    "java": "Java",
    "js": "JavaScript",  # Maps JavaScript and Js extensions
    "jsx": "JavaScript",
    "swift": "Swift",
    "sh": "Bash",     # Shell scripting extensions
    "raku": "Raku",
    "rb": "Ruby",     # Ruby and Rails extensions
    "pl": "Perl",     # Perl and PDL extensions
    "pm": " Perl",    # Perl Monads extensions
    "ps1": "PowerShell",
    "psm1": "PowerShell",  # PowerShell extensions
    "py": "Python",    # Python and PyPy extensions
    "pyw": "Python",
    "R": "R",         # R and S-PLUS extensions
    "r": "R",        
    "html": "HTML",   # HTML/CSS extensions
    "htm": "HTML",
    "xml": "XML",     # XML/SVG extensions
    "sgml": "SGML",
    "ada": "Ada",      # Ada programming language extension
    "e": "Eiffel",     # Eiffel programming language extension
    "hs": "Haskell",   # Haskell programming language extension
    "lua": "Lua",      # Lua scripting language extension
    "sql": "SQL",      # SQL database querying extensions
    "vhd": "VHDL",    # VHDL hardware description extensions
    "vhdl": "VHDL",
    "v": "Verilog",   # Verilog hardware description extension
    "vh": "Verilog",
    "sql": "SQL",      # SQL database querying extensions
    "apl": "APL",      # APL programming language extension
    "applescript": "AppleScript",  # Apple scripting language extension
    "bas": "BASIC",    # BASIC programming language extension
    "f": "Fortran",   # Fortran programming language extension
    "for": "Fortran",
    "f90": "Fortran",
    "f95": "Fortran",
    "m": "MATLAB",    # MATLAB technical computing extension
    "nim": "Nim",     # Nim programming language extension
    "ml": "OCaml",    # OCaml and Objective Caml extensions
    "mli": "OCaml",
    "pas": "Pascal",   # Pascal programming language extension
    "dpr": "Delphi",  # Delphi development system extension
    "dfm": "Delphi",
    "mod": "Modula-2", # Modula-2 programming language extension
    "oberon": "Oberon",# Oberon programming language extension
    "php": "PHP",      # PHP scripting language extension
    "php3": "PHP",
    "phtml": "PHP",
    "kt": "Kotlin",   # Kotlin programming language extension
    "go": "Go",       # Go programming language extension
    "ts": "TypeScript",# TypeScript programming language extension
    "rs": "Rust",     # Rust programming language extension
    "jl": "Julia",    # Julia programming language extension
    "scala": "Scala",  # Scala programming language extension
}

# Set of known file extensions that correspond to valid programming languages

def get_file_extension(fileName):
    """Get the file extension from a given filename"""
    lSplitDirectory = re.split(r"\.", fileName)
    if not lSplitDirectory:
        log.info(f"No extension found for {fileName}")
        return None
    else:
        extension = lSplitDirectory[-1].lower()

    if extension not in D_FILE_EXTENSIONS.keys():
        log.debug(f"Extension {extension} not recognized")
        return None
    return extension

def supports_comments(fileName):
    """Check if a file has recognized comments based on its extension"""
    extension = get_file_extension(fileName)
    return extension and extension in D_FILE_EXTENSIONS.keys()

def get_file_language(fileName):
    """Determine the programming language of a file based on its extension"""
    extension = get_file_extension(fileName)
    return D_FILE_EXTENSIONS[extension]  # Return None if unknown extension
