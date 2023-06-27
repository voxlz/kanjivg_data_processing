# Convert string unicode to char
from ast import literal_eval
import csv

from my_code.kanji import get_jinmeiyo_kanji, get_joyo_kanji
from my_code.radicals import get_radicals

# Convert string unicode to char
str_unicode = "0x" + "2ED0"
convert_str = literal_eval(str_unicode)
non_standard = chr(convert_str)

# Convert string unicode to char
str_unicode = "0x" + "2ED0"
convert_str = literal_eval(str_unicode)
non_standard = chr(convert_str)

# Convert string unicode to char
str_unicode = "2ED0"
convert_str = int(str_unicode, 16)
non_standard = chr(convert_str)

def to_chr(unicode_codepoint):
    ''' Convert string unicode to char: 2ED0 -> ⻐'''
    return chr(int(unicode_codepoint, 16))

homo_dict = {} 
def to_homoglyph(char):
    ''' Convert characters to the preferred default homoglyph unicode representation. This is needed as some radicals have multiple unicode representations. 
    
    The preferred order goes like this:
    1. Joyo Kanji
    2. Radicals
    3. Jinmeiyo Kanji '''
    
    # Create mapping
    if homo_dict == {}:
        with open("my_files/homoglyphs.csv", "r", encoding="utf8") as mapping:
            reader = csv.reader(mapping, delimiter=",")

            joyo = get_joyo_kanji()
            radicals = get_radicals()
            jinmeiyo = get_jinmeiyo_kanji()

            for row in reader:
                if '#' in row[0]: continue # Skip if comment
                row = list(map(to_chr, row))

                prefer = None # Preferred representation

                # Check for joyo chars
                if prefer is None:
                    for homoglyph in row:
                        if homoglyph in joyo:
                            if prefer is None:
                                prefer = homoglyph
                            else:
                                raise LookupError("Multiple joyo kanji considered homoglyphs")

                # Check for radicals chars
                if prefer is None:
                    for homoglyph in row:
                        if homoglyph in radicals:
                            if prefer is None:
                                prefer = homoglyph
                            else:
                                raise LookupError(f"Multiple radicals considered homoglyphs: {prefer}")

                # Check for jinmeiyo chars
                if prefer is None:
                    for homoglyph in row:
                        if homoglyph in jinmeiyo:
                            if prefer is None:
                                prefer = homoglyph
                            else:
                                raise LookupError("Multiple jinmeiyo considered homoglyphs")

                if prefer is None:
                    continue
                for alt_char in [c for c in row if c != prefer]:
                    homo_dict[alt_char] = prefer
    # Lookup the character
    return homo_dict[char] if char in homo_dict else char
