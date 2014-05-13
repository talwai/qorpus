"""
Utility functions
"""

def clean_text(txt):
    try:
        raw_lines = txt.split('\n')
        for line in list(raw_lines):
            if line.strip() == '' or line.isspace() or line.strip() == '[Chorus]':
                raw_lines.remove(line)
        return ' '.join(raw_lines) + ' '
    except IOError:
        return ' '
