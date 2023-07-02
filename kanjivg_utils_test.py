

import unittest
from kanjivg import Stroke

from my_code.kanjivg_utils import check_for_stroke, comps_from_tree, get_comp_list_recursive, load_kanji, reduce_comps_recursive

class TestUtils(unittest.TestCase):

    def test_isStroke(self):
        kanji_obj = Stroke({})
        kanji_obj.stype = '㇔'
        kanji_obj.svg = 'M17.71,16.59c2.46,2.07,6.36,8.49,6.98,11.71'        

        isStroke, stroke = check_for_stroke(kanji_obj)
        self.assertEqual(isStroke, True)
        self.assertEqual(stroke, '㇔')
        
        


if __name__ == '__main__':
    unittest.main()
    