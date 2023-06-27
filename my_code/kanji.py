# Create list of all joyo-kanji
import csv


joyo_kanji_list = set()
def get_joyo_kanji():
    '''Returns a list of all joyo-kanji'''
    
    # If already in memory, use that.
    if joyo_kanji_list != set(): 
        return joyo_kanji_list
        
    with open("my_files/joyo2010.tsv", "r", encoding="utf8") as kanji_file:
        reader = csv.reader(kanji_file, delimiter="\t")

        # Skip the first row, which is just the source link
        next(reader)

        for row in reader:
            (kanji, old_kanji, radical_comps, school_grade, added, reading) = row
            joyo_kanji_list.add(kanji)
    return joyo_kanji_list

jinmeiyo_kanji_list = set()
def get_jinmeiyo_kanji():
    '''Returns a list of all jinmeiyo-kanji'''
    
    # If already in memory, use that.
    if jinmeiyo_kanji_list != set(): 
        return jinmeiyo_kanji_list
    
    with open("my_files/jinmeiyo.csv", "r", encoding="utf8") as kanji_file:
        tsv_reader = csv.reader(kanji_file, delimiter=",")

        # Skip the first row, which is just the source link
        next(tsv_reader)

        for row in tsv_reader:
            (kanji, *variant) = row
            jinmeiyo_kanji_list.add(kanji)
            if variant != []: jinmeiyo_kanji_list.add(variant[0])
    return jinmeiyo_kanji_list