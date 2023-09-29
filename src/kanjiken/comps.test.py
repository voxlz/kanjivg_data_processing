import unittest
from comps import get_comps_info

from kanjivg_utils import load_kanji

class TestCompTree(unittest.TestCase):

    def test_simple(self):
        char = '亜'
        char_dict = {}
        char_info = load_kanji(char)
        char_dict[char]['comps'] = get_comps_info(char_info)
        self.assertDictEqual(char_dict[char]['comps'], {
            'simple': ['㇐', '口', '\u2fda'], # max 6, stroke order
            'complete': {
                'group': 'vertical', # vertical, horizontal, literal
                'components': [  # 1-3 components per group,  stroke order
                    {
                        'group': 'literal',
                        'components': ['㇐']
                    },
                    {
                        'group': 'literal',
                        'components': ['口']
                    },
                    {
                        'group': 'literal',
                        'components': ['\u2fda']
                    }
                ]
            }
        }
)
        
if __name__ == '__main__':
    unittest.main()