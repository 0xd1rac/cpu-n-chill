from instruction import *
import regex as re
class Parser:
    """Parses assembly lines into instructions or label definitions."""
    label_pattern = re.compile(r'^(\w+):')
    instruction_pattern = re.compile(r'^\s*(\w+)(.*)$')

    @classmethod
    def parse_line(cls, line, line_num):
        # Remove comments (anything after ';') and strip whitespace.
        line = line.split(';')[0].strip()
        if not line:
            return None