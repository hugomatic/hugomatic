#!/usr/bin/env python


import sys
import re

import gcode2params
import json2web
import json as json

class Gcode2json(gcode2params.Gcode2Params):

    def __init__(self, title, params):
        state = {}
        gcode2params.Gcode2Params.__init__(self, title, params, state )
 
    def _add_jscode(self, lines):
        text = lines
        text.append ("var gcode = {")
        text.append('    title : "%s",' % self.title)
        text.append("    line_count : %s,\n" % len(self.gcode_params) )
        text.append("    gcode_min_max : " + json.write(self.min_max) + ",\n")
        text.append("    hugomatics:{")
        for k,v in self.params.iteritems():
            str_value = v
            if type(v) == str:
                str_value = '"%s"' % v
            if type(v) == bool:
                str_value =  str(v).lower()
                    
            text.append('%s:%s,' % (k, str_value) )
        text.append("},")
        text.append("    lines : [ ")
        for line in self.gcode_params:
            text.append(json.write(line) +"," )
        text.append(" \n],\n}") 
        #text.append("var gcode = [" + json.write(self.gcode_params))
        
    
    def _add_htmlheader(self, lines):    
        s1 =""""""
        lines.append(s1)

    def _add_html_footer(self, lines):
        s = """
        """
        lines.append(s)   
        
    def get_document(self):
        text = []
        self._add_jscode(text)
        s =  json2web.get_html("\n".join(text))
        return s
    

if __name__ == "__main__":

    f = None
    lines = None
    try:    
        f = open(sys.argv[1]) 
        lines = f.readlines()
    finally:
        f.close()

    json_translator = Gcode2json(sys.argv[1], {})
    for line in lines:
        json_translator.add_gcode_line(line)
    json_str = json_translator.get_document()
    print json_str
    print "// done"
