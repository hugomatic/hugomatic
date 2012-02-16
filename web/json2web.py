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
    <script language="javascript" src="hugomatic/web/stylesheets/canvas/gcode2canvas.js"></script>
    
    <script type="text/javascript">
    window.addEventListener('load', function (){
        //debug("on load");
        title_div = document.getElementById('title');
        var s = "" + gcode.title + ""
        var button_str = '<button type="button"  onClick="render();">' + s + '</button>';
        title_div.innerHTML =   button_str;
        
        onResize();
   
        //debug("render image");
        
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
        
    var context = get_canvas_context('top_viz');    
        
    debug('draw stock');
    draw_stock(context, xform, gcode);
    
    var last=gcode.lines.length-1;
    draw_lines(context, gcode, xform , 0, last);    

    debug('render end');
}

function onResize()
{

    var divCanvas = document.getElementById("divCanvas");
    var canvas =  document.getElementById("top_viz");
    var code = document.getElementById("code");
    

    var iWidth = document.body.clientWidth;
    var sWidth = iWidth.toString();    
    canvas.width = iWidth;
    sWidth += "px";
    divCanvas.style.width = sWidth;
    
    code.style.width = sWidth;

    // Height
    var sHeight = new String();
    var iHeight = document.body.clientHeight / 2;
    sHeight = iHeight.toString();
    sHeight += "px";
    canvas.height = iHeight;
    divCanvas.style.height = sHeight;
    code.style.width = sHeight;
    
    render();
  
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

</head>

<body style="margin: 0pt; overflow: hidden;" onresize="onResize()">



<div id="title" style="width: 100%; height: 60px;">
</div>

<div id="divCanvas" style="overflow: auto; width: 804px; height: 600px; background-color:black">
    <canvas id="top_viz">
        Your browser does not have support for Canvas.
    </canvas>
</div>

<div style="overflow: auto;" id="code">
</div>


</body>
</html>
"""
    return s1+gcode_json+s2 