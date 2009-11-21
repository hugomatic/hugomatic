#!/usr/bin/env python


import sys
import re

import gcode2params
import json as json

class Gcode2json(gcode2params.Gcode2Params):
     
     def get_json(self):
        text = []
        header = self._get_info()
        text.append(header)
        text.append("var gcode = " + json.write(self.gcode_params))
        footer = "\n// footer\n\n"
        text.append(footer)
        return "\n".join(text)

     def _get_info(self):
        count  = len(self.gcode_params)
        s = "var line_count = " + str(count) +";\n" 
        s += "var gcode_min_max = " + json.write(self.min_max) + ";\n"
        return s

def get_lines_from_file(name):
    f = None
    lines = None
    try:    
        f = open(name) 
        lines = f.readlines()
    finally:
        f.close()
    return lines

if __name__ == "__main__":
    lines = get_lines_from_file(sys.argv[1])
    json_translator = Gcode2json()
    for line in lines:
        json_translator.add_gcode_line(line)
    json_str = json_translator.get_json()
    print json_str
    print "// done"
