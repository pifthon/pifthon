
#################################
# STATEMENT STRUCTURE
#################################

KEYWORDS = r'(if|else|while|def)'
# ^[\t]*[if|else|while|def][ \w(\+|-|\*|\/|=|>|<|>=|<=|&|\||%|!|\^|\(|\))]+:[ \t]*(#[ \w\S]*)?$
# ^[\t]* -- a string may start with zero or more number of tabs
# [if|else|while|def] -- followed by any of the keywords from if/else/while/def
# [ \w(\+|-|\*|\/|=|>|<|>=|<=|&|\||%|!|\^|\(|\))]+ -- then string comprise one or more number of
# variables (\w) and operators
# : --  strictly followed by a colon
# [ \t]* -- then zero or more number of space of tabs
# (#[ \w\S]*)? -- zero or one comment may go starting with a # and zero or more number of characters
BLOCK_SYNTAX = r'^[\t]*[if|else|while][ \w(\+|-|\*|\/|=|>|<|>=|<=|&|\||%|!|\^|\(|\))]+:[ \t]*(#[ \w\S]*)?$'

ASSIGNMENT = r'^[\t]*[a-zA-Z]+[0-9]*[ \t]*=[ \t]*(\+\+|\-\-)*\w+[ \t]*([ \t]*(\+|-|\*|\/|==|>|<|>=|<=|&|and|or|not|\||%|!|\^|\(|\))[ \t]*\w+[ \t]*)*[ \t]*(#[ \w\S]*)?$'

PASS = r'^[\t]*pass[ \t]*(#[ \w\S]*)?$'

RETURN = r'^[\t]*return[ \t]+(\+\+|\-\-)*\w+[ \t]*([ \t]*(\+|-|\*|\/|==|>|<|>=|<=|&|and|or|not|\||%|!|\^|\(|\))[ \t]*\w+[ \t]*)*[ \t]*(#[ \w\S]*)?$'

METHOD_CALL = r'^[\t]*([a-zA-Z]+[0-9]*[ \t]*=)?[ \t]*\w+\((\w*[ \t]*([ \t]*,[ \t]*\w+)*)?\)[ \t]*(#[ \w\S]*)?$'

METHOD_DEF = r'^[\t]*def[ \t]+\w+\(([a-zA-Z]+[0-9]*[ \t]*([ \t]*,[ \t]*[a-zA-Z]+[0-9]*)*)?\):[ \t]*(#[ \w\S]*)?$'

THREAD = r'^[\t]*[a-zA-Z]+[0-9]*[ \t]*=[ \t]*Thread\(\w+[ \t]*(,\[\w*[ \t]*([ \t]*,[ \t]*\w+)*\])?\)[ \t]*(#[ \w\S]*)?$'

COMMENT = r'[ \t]*#[^\n]+'


syntax = [
    BLOCK_SYNTAX, 
    THREAD, 
    ASSIGNMENT, 
    PASS, 
    RETURN, 
    METHOD_CALL, 
    METHOD_DEF, 
    COMMENT
    ]