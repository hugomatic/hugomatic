
function Scale(x_off, y_off, scale) {
	this.x_off = x_off;
	this.y_off = y_off;
	this.scale = scale;

	this.position = function(x,y,z) 
    {
        return [x_off + (x * this.scale), y_off + (y * this.scale), z * this.scale];
	}

    this.distance = function(dist)
    {
        return dist * this.scale
    }
} 

function debug_clear()
{
    var elem = document.getElementById('debug');
    elem.innerHTML = "Cleared!"
    
}

function debug(msg)
{
    var elem = document.getElementById('debug');
    elem.innerHTML += "<p>" + msg + "</p>";
}    

function get_canvas_context(canvas_id)
{
  var elem = document.getElementById(canvas_id);
  if (!elem || !elem.getContext) {
    return;
  }

  // Get the canvas 2d context.
  var context = elem.getContext('2d');
  if (!context) {
    return;
  }
  return context;
}

function format_hugomatics(gcode)
{
    var s = "<ul>";
    for(x in gcode.hugomatics) 
        s+= "<li>" + x + ": " + gcode.hugomatics[ x ] + "</li>";
    s += "</ul>";
    return s;
}

function format_gcode_info(gcode)
{  
    var s = "<ul>"
    s += "<li>Nb of lines = ";
    s += gcode.line_count + "</li>";
    var dx = gcode.gcode_min_max.x[1] - gcode.gcode_min_max.x[0];
    var dy = gcode.gcode_min_max.y[1] - gcode.gcode_min_max.y[0];
    var dz = gcode.gcode_min_max.z[0] - gcode.gcode_min_max.z[1];
    s += "<li>dX = "+dx+ " [" + gcode.gcode_min_max.x[0] + "," + gcode.gcode_min_max.x[1] + "]</li>";
    s += "<li>dY = "+dy+ " [" + gcode.gcode_min_max.y[0] + "," + gcode.gcode_min_max.y[1] + "]</li>";
    s += "<li>dZ = "+dz+ " [" + gcode.gcode_min_max.z[1] + "," + gcode.gcode_min_max.z[0] + "]</li>";
    s+= "</ul>";    
    return s;
}

function draw_stock(context, scale, gcode)
{
    var x = gcode.hugomatics.x0_stock;
    var y = gcode.hugomatics.y0_stock;
    var w = gcode.hugomatics.dx_stock;
    var h = gcode.hugomatics.dy_stock;
    var z = gcode.hugomatics.z0_stock;
    var dz = gcode.hugomatics.dz_stock;
    
    if( x === undefined)
    {
    	end_state = gcode.lines[gcode.line_count-1][3];
    	x =  end_state['stock_x0'];
    	y =  end_state['stock_y0'];
    	w =  end_state['stock_w'];
    	h =  end_state['stock_h'];
    	z =  end_state['stock_z0'];
    	dz =  end_state['stock_dz'];
    }

                                                 
    if( x === undefined)
    {
    	x =  end_state['']
    	debug("stock origin (x0_stock) undefined");
    	return;
	}
    if( y === undefined)
    {
    	debug("stock origin (y0_stock) undefined");
    	return;
    }
    if( w === undefined)
    {
    	debug("stock origin (dx_stock) undefined");
    	return;
    }
    if( h === undefined)
    {
    	debug("stock origin (dy_stock) undefined");
    	return;
    }
    if( z === undefined)
    {
    	debug("stock origin (z0_stock) undefined");
    	return;
    }
    if( dz === undefined)
    {
    	debug("stock origin (dz_stock) undefined");
    	return;
    }
    p = scale.position(x,y,z);
    context.strokeStyle = "rgba(0,0,128,0.1)"; 
    context.fillStyle   = "rgba(0,0,128,0.1)"; 
    context.fillRect(p[0], p[1], scale.distance(w), scale.distance(h))
}

function format_comment(comment)
{
    return '<font color="darkgreen"><i>' + comment + "</i></font>";
}

function pad(number,length) {
    var str = '' + number;
    while (str.length < length)
        str = '0' + str;
    return str;
}


function format_line_nb(nb)
{ 
  var nb_s  = pad(nb+1, 4);
  return '<font color="darkblue"><a class="nb" onclick="gsel('+ nb + ')">'+ nb_s + '  </a></font>';
}

function format_gcode(text)
{
    var s = "<font color='darkorange'><b>" + text + "</b>";;
    return s;
}

function format_text(line)
{
    var toks = line.split('(');
    // debug(line + " : " +toks.length)    
    var s = format_gcode(toks[0]);
    if (toks.length > 1) 
    {
        s += '<font color="darkgreen"><i>(' + toks[1] +  "</b></font>";
    }
    return s;
}


function format_line(line_nb, class_name, gcode)
{
    var s = "<tr><td>";
    s += format_line_nb(line_nb);
    s += "</td><td class='" +  class_name+ "'>";
    var text= gcode.lines[line_nb][1]; 
    s += format_text(text) + "</td></tr>";
    return s;
}

function format_code(start_line, end_line,gcode)
{
    var s = '<table><tr>' // '<table border="0" cellspacing="0" cellpadding="5"><tr>';
    
    for ( var i=start_line; i< end_line; i++ )
    {   
        var odd_even = i%2 == 0?  "odd":"even"        
        var nb = gcode.lines[i][0];
    
        s += format_line(i, odd_even, gcode);          
    }
    s += "</table>";
    return s;
}


function draw_line(context, line_nb, scale, gcode)
{
    params, state        
    var params = gcode.lines[line_nb][2];
    var state = gcode.lines[line_nb][3];
        
    // context.fillStyle   = "rgba(0,0,0,1)";
    context.strokeStyle = "rgba(255,165,0,0.1)"; 
    context.lineCap = 'round';
    var tool_dia = state.tool_dia;

    var units = state.units;    

    var g = params.g
    var x = params.x;
    var y = params.y;
    var z = params.z;
    var m = params.m 

    var sx = state.x;
    var sy = state.y;
    var sz = state.z;



    if(g === undefined)
    {
        if (m == 2)
        {
            // done
            return;
        }
        return;
    }

    if(x===undefined)
    {
        x = sx
    }    
    if(y===undefined)
    {
        y = sy
    }
    if(z===undefined)
    {
        z = sz
    }

    if (tool_dia === undefined)
    {
        tool_dia = 0.25
    }
    
    var p1 = scale.position(x,y,z);
    var p0 = scale.position(sx,sy,sz)    

    tool_dia = scale.distance(tool_dia);
    
    if (g == 0)
    {
        g0(context,p0[0],p0[1],p0[2],p1[0], p1[1], p1[2]);
    }
    else if (g == 1)
    {
        g1(context,tool_dia, p0[0],p0[1],p0[2],p1[0], p1[1], p1[2]);
    }
    else if (g == 2)
    {
        var i = scale.distance(params.i);
        var j = scale.distance(params.j);
        g2_3(context,g,tool_dia,p0[0],p0[1],p0[2],p1[0], p1[1], p1[2],i,j);
        
    }
    else if (g == 3)
    {
        var i = scale.distance(params.i);
        var j = scale.distance(params.j);
        g2_3(context,g,tool_dia,p0[0],p0[1],p0[2],p1[0], p1[1], p1[2],i,j);
    }
    
    else if (g == 20)
    {
        units = 'inches';       
    }
    else if (g == 21)
    {
        units = 'mm';
    }

}


function g0(context, x0,y0,z0, x1,y1,z1)
{

    context.lineWidth   = 1;

    context.beginPath();
    // scale.transform(x0,y0);
    
    context.moveTo(x0, y0);
    context.lineTo(x1, y1);
    context.stroke();
    context.closePath();
    // return "<p><b>g0 ["+x0+","+y0+ ","+z0+"] -> "+"["+x1+","+y1+ ","+z1+"]" + "</b></p>"
}

function g1(context, tool_dia,  x0,y0,z0, x1,y1,z1)
{
    context.lineWidth   = tool_dia;
    context.beginPath();
    context.moveTo(x0, y0);
    context.lineTo(x1, y1);
    context.stroke();
    context.closePath();

}

function format_point(x,y,z)
{
    return "[" + x + ", " +  y + ", " + z +"]";
}

function g2_3(ctx, g, tool_dia, x0, y0, z0, x1,y1,z1, i,j,k)
{
    var cx = x0 + i;
    var cy = y0 + j;
    var radius = Math.sqrt(i*i + j*j);
    var s_angle = 0;
    var e_angle = 0;
    // full circle?
    if( (x1 == x0) && (y1 == y0) )
    {
        s_angle = 0;
        e_angle = Math.PI * 2;
    }
    else
    {
        s_angle = Math.atan2(y0 - cy, x0 - cx);
        e_angle = Math.atan2(y1 - cy, x1 - cx);
    }
    var anticlock = (g == 2);
    
    // draw using arc (x, y, radius, start angle rad, end angle, anticlockwise) 
    ctx.lineWidth   = tool_dia;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, s_angle, e_angle, anticlock);
    ctx.stroke();
    ctx.closePath();
}


