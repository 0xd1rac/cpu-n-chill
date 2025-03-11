from instruction import *
import regex as re
class Parser:
    """Parses assembly lines into instructions or label definitions."""
    label_pattern = re.compile(r'^(\w+):')
    instruction_pattern = re.compile(r'^\s*(\w+)(.*)$')