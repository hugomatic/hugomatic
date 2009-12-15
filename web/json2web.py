def get_html (gcode_json):
    s1 = """


<html><head>

<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">

    <title>CNC IDE</title>

<style>

 .odd{background-color: rgb(255,255,200);}
 .even{background-color:rgba(0,0,128,0.1); }
 .nb{
    font-color:"darkblue";
    background-color:light-gray;
}

div {
    // background-color:black
}

td {
//    border-right: 1px solid #C1DAD7;
//    border-bottom: 1px solid #C1DAD7;
    background: #fff;
    padding: 0px 0px 0px 0px;
    color: #4f6b72;
}





</style>

    <script type="text/javascript"> 
    // $hugomatic$
"""

    s2 = """

    // $$hugomatic$$
    </script> 
    <script language="javascript" src="hugomatic/web/stylesheets/canvas/split_panels.js"></script>
    <script language="javascript" src="hugomatic/web/stylesheets/canvas/gcode2canvas.js"></script>
    
    <script type="text/javascript">
    window.addEventListener('load', function (){
        //debug("on load");
        title_div = document.getElementById('title');
        var s = "" + gcode.title + ""
        title_div.innerHTML = s;
        //debug("render image");
        render();
        //debug("render code");
        code(); 
        //debug("on load... done");       
        
    }, false);

var x_off = 50;
var y_off = 100;
var scale = 100;
xform = new Scale(x_off, y_off, scale);    

function render()
{
    debug('render begin');
    
    debug('fill info');
   // var s = format_gcode_info(gcode);  
   // var info_div = document.getElementById('gcode_info');
   // info_div.innerHTML = s;
   // s = format_hugomatics(gcode);
   // debug('fill params');
   // var params_div = document.getElementById('divLeft');
   // params_div.innerHTML = s;
        
    debug('draw lines');    
    
    var context = get_canvas_context('top_viz');    
        
    debug('draw stock');
    draw_stock(context, xform, gcode);
    
    var last=gcode.lines.length-1;
    draw_lines(context, gcode, xform , 0, last);    

    debug('render end');
}

function code()
{
    debug('render text code');
    var start_line = 0;
    var end_line = gcode.line_count;
    var s = format_code(start_line, end_line,gcode);
    code_div = document.getElementById('code');
    code_div.innerHTML = s;
}

  </script>

    <script language="javascript" src="split_panels.js"></script>
    <script language="javascript" src="gcode2canvas.js"></script>
</head><body style="margin: 0pt; overflow: hidden;" onload="OnLoadIndex()" onresize="OnResizeIndex()" onmouseup="OnMouseUpBar()" onmousemove="return OnMouseMoveBar(event);">

<!-- Header -->
<div id="title" style="width: 100%; height: 60px;">
    <table width="100%" cellpadding="0" cellspacing="0">
        <tbody><tr>
            <td style="width: 100%;"><img src="indexB_files/image003.gif" width="100%" height="24"></td>
        </tr>
        <tr>
            <td style="width: 100%;"><img src="indexB_files/image002.gif" width="100%" height="34"></td>
        </tr>
    </tbody></table>
</div>

<!-- Vertical Bar -->
<div id="divVertBar" onmousedown="return OnMouseDownBar(true, event);" style="cursor: col-resize; font-size: 3pt; position: absolute; width: 5px; background-color: orange; height: 518px; left: 203px;"></div>

<!-- Horizontal Bar -->
<div id="divHorzBar" onmousedown="return OnMouseDownBar(false, event);" style="cursor: row-resize; font-size: 3pt; position: absolute; width: 814px; height: 4px; background-color: orange; left: 203px; top: 371px;"></div>

<!-- divPhantomBar -->
<div id="divPhantomBar" style="display: none; font-size: 3pt; position: absolute; background-color: rgb(51, 102, 153);"></div>

<table style="border: 3px solid orange;" cellpadding="0" cellspacing="0">
    <tbody><tr>
        <td rowspan="2" style="border: 2px solid orange;">

<div id="divLeft" style="overflow: auto;">

<button type="button"  onClick="render();">render</button>

</div></td>

        <td style="border: 2px solid orange;">

<div id="divCanvas" style="overflow: auto; width: 804px; height: 306px; background-color:black">
    <canvas id="top_viz">Your browser does not have support for Canvas.</canvas>
</div>

</td>
    </tr>
    <tr>
        <td style="border: 2px solid orange;">

<div style="overflow: auto;" id="code"></div>

</td>
    </tr>
</tbody></table>
</body></html>
"""
    return s1+gcode_json+s2 