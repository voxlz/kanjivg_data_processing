from kanjivg_utils import get_comp_list_recursive, reduce_comps, simplify_comp_list


def get_comps_info(char_info):
    comps = get_comp_list_recursive(char_info)
    comps = reduce_comps(comps, char)
    comps = simplify_comp_list(comps)
