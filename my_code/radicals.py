import csv


kangxi_radicals = set()
def get_radicals():
    '''Returns a list of all radicals'''
    
    # If already in memory, use that.
    if kangxi_radicals != set(): 
        return kangxi_radicals
    
    with open("my_files/radicals_kangxi.csv", "r", encoding="utf8") as radical_file:
        reader = csv.reader(radical_file)

        for row in reader:
            if "#" in row[0]: continue # Skip if comment
            radical = row[0]
            kangxi_radicals.add(radical)
            
    return kangxi_radicals