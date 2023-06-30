
reduction_rules = [
    # ('㇐*', '一'), # ㇐* => 一 simplifies rules
    # ('㇑*', '㇑*'), # ㇐* => 一 simplifies rules
    ('㇐,巾','帀'),
    ('㇒,㇙,㇒,㇏', '𧘇'),
    ('㇑,㇑,㇔,㇒,㇐', '业'),
    ('㇕,㇐,㇐', '彐'),
    ('㇐,㇑,㇑,㇑,㇑', '卌'),
    ('㇐,㇑,㇑,㇑', '卅'),
    ('㇐,㇑,㇑,㇐,㇐', '𠀎'),
    ('㇐,㇑,㇑', '卄'),
    ('㇐,㇐,㇐', '三'),
    ('㇐,㇐', '二'),
    ('㇒,㇑,㇒,㇔', '𧘇'),
    ('㇑,㇕,㇐,㇕,㇐', '㠯'),
    ('㇑,㇕,㇔', '卪'),
    ('㇔,㇒', '丷'),
    ('人,㇐,口,人', '㑒'),
    ('㇑,㇕', '⨅'),
    ('㇒,㇔', '八'),
    ('㇒,㇚', '刂'),
    ('三,㇑', '龶'),
    ('人,人,人,人', '𠈌'),
    ('㇆,㇔,㇀', '习'),
    
    # Questionable rules
    ('丿,丶', '冫'), # Technically correct, could lead to more issues down the line...
    
    # Probably bad rules
    ('㇂,丿,丶', '义'), # Missing hook, not a huge fan of this one.
    ('㇂,㇒,㇔', '义'), # Missing hook, not a huge fan of this one.
    ('㇒,㇏', '人'), 
    # ('艹', '卄'), # They look the same :D
    # ('𠆢', '人'), 
    # ('⺈', '𠂊')   
]


def get_rules():
    return reduction_rules