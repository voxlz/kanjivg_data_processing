## An attempt to create a dependency tree including all JoYo kanji based on their parts.
from typing import List
from my_code.kanji import get_jinmeiyo_kanji, get_joyo_kanji, get_valid_kanji
from my_code.kanjivg_utils import get_comp_list, get_components, load_kanji, reduce_tree
from my_code.radicals import get_radicals, get_strokes
from my_code.tree import Tree
from my_code.unicode import to_homoglyph

# Program limits
max_comps = 5 # how many kanji parts to allow in UI for a single kanji

# List of radicals to accept to reduce the number of components a kanji can have. Let's say... 8 components max.
radicals_8 = []

# Clear the cache of python 
import importlib
clear_cache = importlib.invalidate_caches()

def remove_duplicates(char_set, name):
    ''' Remove homoglyph duplicates from a set of
    characters with to_homoglyph. '''
    
    old_len = len(char_set)
    pref_chars = set(map(to_homoglyph, char_set))
    char_set = pref_chars.intersection(char_set)
    # removed = pref_chars.difference(char_set)
    print(f"{name}: {old_len} -> {len(char_set)} (-{old_len - len(char_set)})")
    return char_set

# Load all characters - Circular bullshit
joyo        = get_joyo_kanji()
strokes     = remove_duplicates(get_strokes(), 'strokes')
radicals    = remove_duplicates(get_radicals(), 'radicals')
jinmeiyo    = remove_duplicates(get_jinmeiyo_kanji(), 'jinmeiyo')

# Ensure no overlapping characters
assert radicals.isdisjoint(joyo)
assert joyo.isdisjoint(jinmeiyo)
assert radicals.isdisjoint(jinmeiyo)



    
def reduce_parts(strokes: List[str]):
    # '醸' = ['酉', '六', '一', '㇑*', '㇑*', '一', '一', '㇒*', '㇙*', '㇒*', '㇏*'] => ['酉', '六', '一', '㇑*', '㇑*', '二', '𧘇']
    strokes_str = ','.join(strokes)
    for (match, result) in reduction_rules:
        
        if match in strokes_str:
            # if match not in ['㇐*','㇑*']: 
            #     print(f"Reducing {strokes_str} to {result} in {kanji}")
            strokes_str = strokes_str.replace(match, result)
    
    # Split and remove empty strings
    return list(filter(lambda c: c, strokes_str.split(',')))

# Look up all joyo kanji in the kanji-svg database
kanji_parts = {}
kanji_dict = {}
joyo_tree = {}


for kanji in ['臣', '形' ]:
    kanji_obj = load_kanji(kanji)
    kanji = kanji_obj.element
    
    comps = get_components(kanji_obj, joyo = False)
    comp_tree = get_comp_list(kanji_obj)
    comp_with_radicals = reduce_parts(comps)

    # if random.randint(0, 100) == 0:
    #     print()
    joyo_tree[kanji] = comp_tree
    kanji_parts[kanji] = comp_with_radicals
    kanji_dict[kanji] = {
        'comp_kanji': [k for k in comp_with_radicals if k in get_valid_kanji()],
        'comp_kanji&radicals': comp_with_radicals, # Kanji, radicals and strokes
        'comp_kanji&strokes': comp_with_radicals, # Only kanji and strokes
        'comp_preferred': comp_with_radicals,
    }
    # print(comp_elems)

reduce_tree([joyo_tree])

print()

# Calculate a dependency tree for each kanji
for kanji in kanji_parts:
    # if kanji == "楼":
    #     print(f"{kanji} has {len(parts)} parts")

    kanji_dict[kanji] = {
        'part_of': [parent for parent, p_parts in kanji_parts.items() if kanji in p_parts],
    } | kanji_dict[kanji]

    print(f"{kanji} part of {kanji_dict[kanji]['part_of']}, contains {kanji_dict[kanji]['comp_preferred']}")

print()
print()
print()
print()
# How many have more than 'max_comps' components?
radical_comps = [
    (
        kanji,
        kanji_dict[kanji]['comp_preferred'],
        len(kanji_dict[kanji]['comp_preferred']),
    )
    for kanji in joyo
]
above_x_comps = list(filter(lambda x: x[2] > max_comps, radical_comps))
print(f"More than {max_comps} components: {len(above_x_comps)}")
for kanji, comps, num_comps in above_x_comps:
    print(f"{kanji} has {num_comps} components: {comps}")


# # Goal: Minimize components. Going through joyo tree, note down all encountered characters, and save their most reduced form.
# def find_most_reduced_form(list_of_chars):
#     ''' Recursively find the most reduced form of a tree of components. Input [{}]. '''
    
#     most_reduced = Tree()
    
#     for chars in list_of_chars:
#         for (char, comps) in chars.items():
#             print()
    
#     return most_reduced

# find_most_reduced_form([joyo_tree])


# Ideally we want to minimize the amount of radicals the user will have to learn, since they are not kanji themselves.
# given 'max_comps', how many radicals will the user encounter?
seen_strokes = set()
seen_radicals = set()
seen_other = set()
seen_name_kanji = set()
seen_components = 0
for kanji in joyo:
    seen_components += len(kanji_dict[kanji]['comp_preferred'])
    for part in kanji_dict[kanji]['comp_preferred']:
        if part not in joyo:
            if '*' in part: 
                seen_strokes.add(part[:-1])
            elif part in radicals:
                seen_radicals.add(part)
            elif part in jinmeiyo:
                seen_name_kanji.add(part)
            else:
                seen_other.add(part)

print(f"User will encounter {len(seen_strokes)} strokes")
print(seen_strokes)
print(f"User will encounter {len(seen_radicals)} radicals")
print(seen_radicals)
print(f"User will encounter {len(seen_name_kanji)} name kanji")
print(seen_name_kanji)
print(f"User will encounter {len(seen_other)} extra kanji")
print(seen_other)
print(f"User will encounter {seen_components} components")
print(len(joyo))

# Most repeated component in a kanji? 
# 傘 has 6 components: ['人', '人', '人', '人', '人', '十']