import csv
import json
from xml.etree.ElementTree import iterparse

from sortedcollections import OrderedSet
from src.kanji import get_joyo_kanji
from src.radicals import get_radicals
from src.tree import Tree

from src.unicode import to_homoglyph
from itertools import chain,zip_longest


def set_char_meanings(char_dict):
    ''' Set the meanings of each character in char_dict. 
    Goals:
        1. No two char should have the same primary meaning to avoid confusion.
        2. Only kanji should have meanings. (radical meanings  will inevitably  overlap with kanji meanings)
        3. The meaning should be concise, ideally one word.
        4. Secondary meanings should be saved as well
        5. For overlapping meanings (including secondary meanings), save that data in similar_meaning
        6. Primarily take most common kanji representations into account while finding synonyms. (old usage not very important)
        
    '''
    
    # Manually confirmed or changed meanings
    override_meanings = {
        '用': "utilize",
        '成': "become",
        '候': "climate",
        '理': "logic",
        '絶': "discontinue",
        '首': "neck",
        '⾴': "page",
        '光': "visible light", # light has double meaning
        '軽': "not heavy", # light has double meaning
        '右': "right side",
        '正': "correct",
        '権': "authority",
        '老' : "old person",
        # --- Separation ----
        '分' : "part",
        '割' : "fraction",
        '離' : "detach",
        '別' : "separate",
        # ------------
        '台' : "pedestal",
        '立' : "stand up",
        '系' : "lineage",
        '面' : "mask",
        '太' : "chubby", # fat has double meaning
        '研' : "sharpen",
        # --- Temperature ---
        '熱' : "burning hot",
        '温' : "pleasantly warm",
        '冷' : "freezing cold",
        '涼' : "refreshingly cool",
        '暑' : "hot climate",
        '暖' : "mild climate",
        '寒' : "cold climate",
        # ------------
        '座' : "sit",
        '較' : "contrast",
        '抗' : "confront",
        '焼' : "roast",
        '閣' : "political cabinet",
        '濃' : "undiluted",
        '討' : "chastise",
        '貿' : "exchange",
        '便' : "convenience",
        '⾱' : "n/a", # hyougai,
        '几' : "n/a", # radical
        '⼹' : "n/a", # radical
        '⺔' : "n/a", # radical
        '⻖' : "n/a", # radical
        '⺅' : "n/a", # radical
        '⺌' : "n/a", # radical
        '㇠' : "n/a", # radical,
        '㇟' : "n/a", # radical,
        '将' : "officer",
        '概' : "approximate",
        '頃' : "proximate time",
        '当' : "hit",
        '今' : "now",
        '提' : "propose",
        '漁' : "fishing",
        '河' : "large foreign river",
        '屋' : "roof",
        '鳴' : "make sound",
        '支' : "support",
        '歳' : "annual",
        '世' : "generation",
        '印' : "stamp",
        '暴' : "outburst",
        '我' : "selfish",
        '自' : "oneself",
        '童' : "juvenile",
        '児' : "newborn",
        '善' : "virtue",
        '銭' : "coin",
        '貨' : "cargo",
        '乾' : "drought",
        '盟' : "oath",
        '肌' : "texture",
        '皮' : "animal pelt",
        '眼' : "eyeball",
        '数' : "several",
        '恋' : "romance",
        '泉' : "fountain",
        '僕' : "servant",
        '画' : "brush-stroke",
        '舞' : "whirling dance",
        # --- Creation ---
        '工' : "construct",
        '造' : "create",
        '作' : "make",
        '製' : "manufacture",
        '構' : "structure",
        '築' : "fabricate" ,
        '創' : "genesis",
        # ------------
        '著' : "publish",
        '端' : "edge",
        '課' : "lesson",
        '護' : "safeguard",
        '共' : "together",
        '業' : "business",
        '勢' : "force",
        '力' : "strength",
        '身' : "somebody",
        '場' : "location",
        '置' : "placement",
        '育' : "nurture",
        '募' : "recruit",
        '密' : "secrecy",
        '望' : "ambition",
        '命' : "command",
        '換' : "interchange",
        '著' : "renowned", 
        '品' : "goods",
        '野' : "plains",
        '徳' : "benevolence",
        '汽' : "vapour",
        '判' : "judgement",
        '態' : "attitude",
        '述' : "verbal",
        '法' : "method",
        '役' : "role",
        '己' : "self",
        '帰' : "homecoming",
        '戻' : "revert",
        '途' : "route",
        '道' : "road-way",
        '令' : "decree",
        '志' : "intention",
        '仁' : "humanity",
        '群' : "herd",
        '妬' : "envy",
        '懐' : "pocket",
        # --- Time of Day ---
        '暁' : "dawn",
        '旦' : "daybreak",
        '晩' : "nightfall",
        '夕' : "evening",
        '夜' : "night",
        # --- Darkness ---
        '暮' : "get dark",
        '闇' : "darkness",
        '暗' : "dark",
        '冥' : "gloom",
        # --- Sadness ---
        '憂' : "melancholy",
        '鬱' : "depression",
        '悲' : "sad",
        '哀' : "pathetic",
        '嘆' : "grief",
        '悼' : "lament",
        '忌' : "mourning",
         # --- Fear ---
        '慄' : "shiver",
        '惧' : "threatened",
        '恐' : "fear",
        # ---- Containers ----
        '丼' : "bowl",
        '鉢' : "pot",
        '鍋' : "pan",
        '蓋' : "lid",
        # --- Hide ---
        '蔽' : "conceal",
        '隠' : "hide",
        '匿' : "shelter",
        # -------------
        '咽' : "choked",
        '没' : "death",
        # ----------------
        '存' : "aware of",
        '稽' : "practice",
        # ---------
        '替' : "replace",
        '挫' : "sprain",
        '呉' : "kingdom of wu",
        '脊' : "spine",
        '背' : "back (body)",
        '嘲' : "insult",
        '慢' : "laziness", # Can be improved
        '璧' : "annulus", 
        '萎' : "shrivel",
        '歌' : "sing",
        '唄' : "ballad",
        '呂' : "bath",
        '将' : "admiral",
        '箋' : "label", # slip of paper alt. meaning
        '湧' : "seethe",
        '賄' : "supply",
        '終' : "finish",
        '酒' : "alcohol",
        '戚' : "relatives",
        '挟' : "between",
        '奥' : "interior",
        '串' : "skewer",
        '玩' : "plaything",
        '挙' : "project",
        '点' : "point",
        '阜' : "mound",
        '湧' : "well up",
        '奔' : "rush",
        '配' : "hand out",
        '弊' : "malice",
        '没' : "fall into",
        '容' : "content",
        '穂' : "ear of grain",
        # -------- thinking ------
        '稽' : "thought",
        '考' : "consider",
        '虞' : "expectation",
        '畏' : "reverence",
        '和' : "japanese",
        '岳' : "peak",
        '昧' : "state of thought",
        '曖' : "ambiguous",
        '恣' : "arbitrary",
        '陣' : "battle-array",
        # ---- Group ---- (avoid party)
        '派' : "faction",
        '閥' : "clique",
        '団' : "group",
        '党' : "alliance",
        '隊' : "troop",
        '班' : "team", # squad
        # --------------
        '営' : "occupation",
        '凡' : "commonplace",
        '庸' : "mediocre",
        '競' : "contest",
        '畿' : "suburbs of capital",
        '未' : "not yet",
        '非' : "not",
        '捉' : "capture",
        '宅' : "home",
        '載' : "placed on",
        #------- sand --------
        '砂' : "sand",
        '沙' : "grit",
    }

    joyo = get_joyo_kanji()

    # Read KanjiDic2.xml - 13,108 kanji
    with open("data/kanjidic2.xml", "r", encoding="utf8") as file:
        kd2 = Tree()
        curr_char = None
        for _, elem in iterparse(file):
            if elem.tag == 'literal':
                curr_char = elem.text
                kd2[curr_char]['kd2_meanings'] =  []
            elif elem.tag == 'meaning' and 'm_lang' not in elem.attrib:
                kd2[curr_char]['kd2_meanings'] +=  [elem.text]
            elif elem.tag == 'cp_value' and elem.attrib['cp_type'] == 'ucs':
                kd2[curr_char]['cp'] = elem.text
            elif elem.tag == 'grade':
                kd2[curr_char]['grade'] = elem.text
            elif elem.tag == 'jlpt':
                kd2[curr_char]['jlpt'] = elem.text

    # Read KanjiAlive.csv - 1235 kanji
    with open("data/kanjialive/ka_data.csv", "r", encoding="utf8") as file:
        ka = Tree()
        reader = csv.reader(file, delimiter=",", )
        next(reader) # skip header
        for row in reader:
            if '#' in row[0]: continue # Skip comments
            (char,name,stroke,meaning,*_) = row
            ka[char] = {
                'meanings': list(
                    filter(
                        lambda y : y != "", map(
                            lambda x : x.strip('" '), 
                                meaning.split(',')
                        )
                    )
                )
            }

    # Read Wanikani kanji - 1235 kanji
    with open("data/davidluzgouveia-kanji-data/kanji.json", "r", encoding="utf8") as file:
        wk = json.load(file)

    meaning_to_char = Tree()
    primary_to_char = Tree()
    resulting_dict = Tree()

    # Select primary meaning, Ensure unique, merge dicts, find kanji with overlapping meanings
    for char in joyo:

        # Get meanings from sources
        kd2_meanings = kd2[char]['kd2_meanings'] if char in kd2 else []

        ka_meanings = ka[char]['meanings'] if char in ka else []
        wk_meanings = wk[char]['wk_meanings'] if char in wk and wk[char]['wk_meanings']  else []
        wk_meanings = [s.replace("^", "") for s in wk_meanings]

        if (char == "鉢"):
            print()
        # Weave the two lists together
        weave = chain.from_iterable(zip_longest(kd2_meanings, ka_meanings, wk_meanings))
        meanings = list(filter(lambda x : x, weave))
        if char in override_meanings:
            meanings.insert(0, override_meanings[char])

        # Filter out radical meanings and lower case
        meanings = [s.lower() for s in meanings if  "(no. " not  in s]

        # Remove duplicates
        meanings = [*dict.fromkeys(meanings)]

        # Set primary and secondary meanings
        primary = meanings[0] if meanings else ""
        secondary = meanings[1:] if len(meanings) > 1 else []

        # Save a reverse dict to later check for duplicate meanings
        primary_to_char.add_or_append(primary, char)
        for meaning in meanings:
            meaning_to_char.add_or_append(meaning, char)

        resulting_dict[char] = {
            'meaning': primary,
            'meaning_sec': secondary,
        } | kd2[char]
        del resulting_dict[char]['kd2_meanings']

    if duplicate_primaries := {
        c for c in primary_to_char 
        if len(primary_to_char[c]) > 1
    }:
        print(f"Duplicate primary meanings: {len(duplicate_primaries)}")
        for meaning in duplicate_primaries:
            if len(primary_to_char[meaning]) > 1:
                print(f"Duplicate PRIMARY: {meaning}")
                for char in primary_to_char[meaning]:
                    print(f"char: {char} meaning: {[resulting_dict[char]['meaning']] + resulting_dict[char]['meaning_sec']}")

    # Check for overlapping  meanings
    # for meaning in meaning_to_char:
    #     if len(meaning_to_char[meaning]) > 1:
    #         print(f"Duplicate meaning: {meaning}")
    #         for char in meaning_to_char[meaning]:
    #             print(f"char: {char} meaning: {resulting_dict[char]['meaning']}")

    print()
    print(f"Total kanji: {len(resulting_dict)}")