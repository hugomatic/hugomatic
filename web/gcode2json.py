#!/usr/bin/env python


import sys
import re

import gcode2params
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
        s1 ="""
<!DOCTYPE html>
<html lang="en">
  <head>

    <meta charset="utf-8">
    <title>GCODE canvas</title>

<style>
 .odd{background-color: rgb(255,255,200);}
 .even{background-color:rgba(0,0,128,0.1); }
table, td
{
  //  border-color: #600;
  //  border-style: solid;
}

table
{
    border-width: 0 0 1px 1px;
    border-spacing: 0;
    border-collapse: collapse;
}

td
{
    margin: 0;
    padding: 4px;
    border-width: 0 0 0 0;
    background-color: lightgray; //#FFC;
}

</style>

<script type="text/javascript">
    """
        lines.append(s1)

    def _add_html_footer(self, lines):
        s = """
    </script> 
    <script src="./hugomatic/web/stylesheets/canvas/gcode2canvas.js" type="text/javascript"></script>
    <script type="text/javascript">
    window.addEventListener('load', function (){
        debug("on load");
        title_div = document.getElementById('title');
        var s = "<h2>" + gcode.title + "</h2>"
        title_div.innerHTML = s;
        debug("render image");
        render();
        debug("render code");
        code(); 
        debug("on load... done");       
        
    }, false);


    
function render()
{
    debug('render begin');
    
    debug('fill info');
    var s = format_gcode_info(gcode);  
    var info_div = document.getElementById('gcode_info');
    info_div.innerHTML = s;
        
    debug('fill params');
    var params_div = document.getElementById('hugomatics');
    s = format_hugomatics(gcode);
    params_div.innerHTML = s;
        
    debug('draw lines');    
    var context = get_canvas_context('top_viz');    
    
    
    
    var x_off = 50;
    var y_off = 100;
    var scale = 100;
    xform = new Scale(x_off, y_off, scale);
   
    draw_stock(context, xform, gcode);
    
    var arLen=gcode.lines.length;
    for ( var i=0, len=arLen; i<len; ++i )
    {   
        var nb = gcode.lines[i][0];
        var text= gcode.lines[i][1];    
        try       
        {
            draw_line(context, i, xform, gcode);
        }
        catch(err)
        {
            debug('ERROR: render_line: ' + nb + ":" + text + " ERR: " + err.description );
        }
    }
    debug('render end');
}

function code()
{
    debug('render text code');
    var start_line = 0;
    var end_line = gcode.line_count-1;
    var s = format_code(start_line, end_line,gcode)
    code_div = document.getElementById('code');
    code_div.innerHTML = s;
}

  </script>

</head>
<body>

<div id="title">
</div>

<!-- button type="button"  onClick="render();">render</button -->
<br>
<canvas id="top_viz" width="800" height="300">Your browser does not have 
support for Canvas.
</canvas>
<h2>G-Code</h2>
<!--button type="button"  onClick="code();">code</button-->
<div id='code'></div>
<h2>Document info</h2>
<div id='gcode_info'></div>
<h2>Params info</h2>
<div id='hugomatics'>
</div>    


<button type="button"  onClick="debug_clear();">clear debug</button>
    <div id='debug'>
Debug log:
    </div>
  </body>
</html>
        
        """
        lines.append(s)   
        
    def get_document(self):
        text = []
        self._add_htmlheader(text)
        self._add_jscode(text)
        self._add_html_footer(text)
        return "\n".join(text)
    
    

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
