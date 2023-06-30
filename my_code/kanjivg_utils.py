from kanjivg import Stroke
from my_code.kanji import get_joyo_kanji, get_valid_kanji
from my_code.radicals import get_radicals, get_strokes
from my_code.reduction import get_rules
from my_code.tree import Tree
from my_code.unicode import to_homoglyph
from utils import canonicalId, listSvgFiles

svg_file_list = listSvgFiles("./kanji/")

def load_kanji(kanji):
    ''' Load the kanji from the kanji-svg database. '''
    kanji_id = canonicalId(kanji)
    kanji_info = [f.read() for f in svg_file_list if f"{kanji_id}.svg" in f.path][0]
        
    return kanji_info.strokes

def get_comp_list(kanji_obj):
    ''' Recursively creates a tree of components for a kanji. Returns an 
    list of components. '''

    result = []
    for child in kanji_obj.childs:
        child_comps = Tree()
        
        # Stroke is the innermost element, return it as is
        if type(child) is Stroke:
            result.append(f"{child.stype[0]}")
            continue
        elif (element := to_homoglyph(child.element)) in get_strokes():
            result.append(f"{element}")
            continue
        
        comp_tree    = get_comp_list(child)
        
        # Some things must be true for the element to be valid
        isExistent   = element is not None
        isComplete   = child.part is None
        isPartial    = child.partial == "true"
        isCOMPLETE   = isExistent and isComplete and not isPartial 
        
        # Then, if the element is a radical or joyo kanji, it is valid
        isRadical    = element in get_radicals()
        isKanji      = element in get_valid_kanji()
        isKANJI      = isRadical or isKanji
        
        # Else, if not curriculum, check for red flags 
        # isVariant    = child.variant == "true" # This is inconsistent.
        # isOriginal   = child.original is None
        # isRadical    = child.radical is not None
        # isUNICODE    = not (isVariant and isOriginal) 
        
        if not (isCOMPLETE and isKANJI) and element is not None and kanji_obj.element is not None and isComplete:
            print(f"Skipping {element} from {kanji_obj.element}")
        
        if isCOMPLETE and (isKANJI):
            child_comps[element] = comp_tree
            result.append(child_comps)
        # If not a valid character, skip and go down the tree
        else:
            result.extend(comp_tree)
    return result

def comps_from_tree(comp_tree):
    ''' Get the direct components of this kanji-comp tree. 
    [{'开': [...]}, {'⼺': [...]}] -> ['开', '⼺']'''
    
    return list(map(lambda x: x if type(x) is str else list(x.keys())[0], comp_tree))

reduced_tree      = Tree() # Reduced tree
reduced_chars     = Tree() # Most reduced {kanji: {comp: [components], from: 'char'}}

def get_lvl_str(comp_tree):
    ''' Get the top most string representation of a component tree. '''
    rtn = []
    # Either recursive tree or a stroke string
    for char in comp_tree:
        if type(char) is str:
            rtn.append(char)
        else:
            rtn.append(list(char.keys())[0])
    return ",".join(rtn)

def reduce_tree(tree_list, depth = 0, from_char = None):
    ''' Recursively reduce a tree of components. '''
    
    org_char = from_char

    # Assuming list with single component tree
    for char, comp_tree in tree_list[0].items():

        # Set current character
        if org_char is None:
            from_char = char

        # Apply applicable reduction rules on char
        for rule, result in get_rules():

            # Skip if rule is not a reduction
            if (result == char): continue 

            # Replace if rule is a reduction
            lvl_comps_str = get_lvl_str(comp_tree)
            while (str_index := lvl_comps_str.find(rule)) != -1:
                itm_index = lvl_comps_str.count(',', 0, str_index)
                rule_len = rule.count(',') + 1
                sliced = slice(itm_index,itm_index+rule_len)
                comp_tree[sliced] = [{result: comp_tree[sliced]}]
                lvl_comps_str = get_lvl_str(comp_tree)

        # Recursively reduce the tree
        reduced_comps = []
        for comp in comp_tree:
            if type(comp) is str:
                reduced_comps.append(comp)
            else:
                char_key = list(comp.keys())[0]
                reduced_comps.append({char_key: reduce_tree([comp], depth + 1, from_char if from_char is not None else char_key)})

        # Save the tree
        if depth == 0:
            reduced_tree[char] = reduced_comps

        # Save most reduced form of a character
        if char in reduced_chars:
            if len(reduced_chars[char]['comps']) > len(reduced_comps):
                reduced_chars[char] = {'comps': reduced_comps, 'from': from_char}
        else:
            reduced_chars[char] = {'comps': reduced_comps, 'from': from_char}

    return (reduced_tree, reduced_chars) if depth == 0 else reduced_comps

def get_components(kanji_obj, depth = 0, joyo = True):
    ''' Recursively move down the tree until you find a joyo kanji, radical or stroke. Returns a list of components.
    '''
    
    # If we have reached a stroke without hitting a kanji, return the stroke
    if type(kanji_obj) is Stroke:
        return [f"{kanji_obj.stype[0]}*"] # stroke typically (type, connection)

    # Unless we are at the top level, we want to add the current kanji to the list of parts
    isComplete = kanji_obj.part is None
    # isPartial =  kanji_obj.partial == "true"

    if (depth != 0 and isComplete):
        elem = to_homoglyph(kanji_obj.element)
        isRadical   = elem in get_radicals()
        isKanji     = elem in get_valid_kanji()
        
        if isKanji or (isRadical and not joyo):
            return [elem]
        
        # NOTE: kanji_obj.original
        # Using the kanji_obj.original might reduce the number 
        # of radicals to learn, however:
        # - Original character is not necessary a joyo kanji.
        # - May have different stroke order / strokes amount, confusing learners.
    
    result = []
    for child in kanji_obj.childs:
        result.extend(get_components(child, depth + 1, joyo))
    return result