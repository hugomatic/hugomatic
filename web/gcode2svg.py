#!/usr/bin/env python


import sys
#import re

import gcode2params

import json as json
class Gcode2Svg(gcode2params.Gcode2Params):
    def __init__(self):
        state = {'svg_scaling':100.0}
        gcode2params.Gcode2Params.__init__(self,state)
            
    def __get_svg_path(self, line_nb, params, state):
    
        #<path d="M600,350 a25,25 -30 0,1 50,-25"
        # http://www.w3.org/TR/SVG/paths.html#PathDataEllipticalArcCommands
        
        g3_path = """  
        <path
           d="M %s,%s L %s, %s"
           id="line_%s"
           style="fill:none;fill-rule:evenodd;stroke:#ffff00;stroke-width:%s;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:0.1" />
       """
        g2_path = """  
        <path
           d="M %s,%s L %s, %s"
           id="line_%s"
           style="fill:none;fill-rule:evenodd;stroke:#008000;stroke-width:%s;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:0.1" />
       """
        
        g1_path = """
        <path
           d="M %s,%s L %s, %s"
           id="line_%s"
           style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:%s;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:0.1" />
    """
        g0_path = """
    <path
           d="M %s,%s L %s, %s"
           id="line_%s"
           style="fill:#ff2a2a;fill-rule:evenodd;stroke:#ff2a2a;stroke-width:1.0;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;opacity:1;stroke-miterlimit:4;stroke-dasharray:none" />
        """    
        
        x0 = None
        y0 = None
        z0 = None        
        if state.has_key('x'):        
            x0 = state['x']
        if state.has_key('y'):     
            y0 = state['y']
        if state.has_key('z'):     
            z0 = state['x']    
            
        x1 = x0
        y1 = y0
        z1 = z0
        if params.has_key('x'):
            x1 = params['x']
        if params.has_key('y'):
            y1 = params['y']
        if params.has_key('z'):
            z1 = params['z']    
        
        if params.has_key('g'):
            scaling = state['svg_scaling']
            x0 *= scaling
            y0 *= scaling
            z0 *= scaling
            x1 *= scaling
            y1 *= scaling
            z1 *= scaling
            
            if params['g'] == 0.:
                path = g0_path % (x0,y0,x1,y1,line_nb)
                return path
            
            if params['g'] == 1.:
                tool_dia = state['tool_dia'] * state['svg_scaling']
                path = g1_path % (x0,y0,x1,y1,line_nb, tool_dia)    
                return path
        
            if params['g'] == 2.:
                tool_dia = state['tool_dia'] * state['svg_scaling']
                path = g1_path % (x0,y0,x1,y1,line_nb, tool_dia)    
                return path
            
            if params['g'] == 3.:
                tool_dia = state['tool_dia'] * state['svg_scaling']
                path = g3_path % (x0,y0,x1,y1,line_nb, tool_dia)    
                return path
            
                

    def _get_svg_header(self):
        
        xmin = self.min_max['x'][0]* self.state['svg_scaling']
        xmax = self.min_max['x'][1]* self.state['svg_scaling']
        ymin = self.min_max['y'][0]* self.state['svg_scaling']
        ymax = self.min_max['y'][1]* self.state['svg_scaling']
      
        dx = xmax - xmin
        dy = ymax - ymin
        
        mid_point = ((xmin + xmax)/2, (ymin + ymax)/2)
        
        dx += 50.
        dy += 50.
    
        translate_x = dx/2 - mid_point[0]
        translate_y = dy/2 - mid_point[1]
        
        #header = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
#    <!-- Created with Hugomatic (http://hugomatic.ca/) -->"""
        header = """
    <svg
       xmlns:svg="http://www.w3.org/2000/svg"
       xmlns="http://www.w3.org/2000/svg"
       version="1.0"
       width="%s"
       height="%s"
       id="svg_code">
    """ % (dx, dy)
    
    
        group = """   
       
      <defs id="defs2460" />
         
       <g
         id="g2771"
         transform="matrix(1,0,0,-1,%s,%s)">  
      
    """ %  (translate_x, translate_y)
    
        # this scaling should be done in the parameter gathering
        # to avoid a rogue g20 or g21 
        w = self.state['stock_w'] * self.state['svg_scaling']
        h = self.state['stock_h'] * self.state['svg_scaling']
        x0 = self.state['stock_x0']* self.state['svg_scaling']
        y0 = self.state['stock_y0']* self.state['svg_scaling']
        stock = """
          <rect
         style="opacity:1;fill:#aaccff;fill-opacity:1;stroke:none"
         id="rect_stock"
         width="%s"
         height="%s"
         x="%s"
         y="%s" />
        """ % (w, h, x0, y0)
        return  header  + group + stock 
    
    def _get_svg_line_from_params(self, params):
        line_nb, text, params, state = params
        lines = []
        text = text.replace("--","- -") # invalid -- inside xml comments
        lines.append( "       <!-- N%03d %s -->" % (line_nb, text))   
        path = self.__get_svg_path(line_nb, params, state)
        if path:
            lines.append(path)     
        return "\n".join(lines)
      
    def get_svg_document(self):
        svg_text = []
        svg_text.append(self._get_svg_header())
        for  g_parameters in self.gcode_params:
            line = self._get_svg_line_from_params(g_parameters)
            svg_text.append(line ) 
        footer = "</g></svg>"
        svg_text.append(footer)
        return "\n".join(svg_text)

if __name__ == "__main__":
    lines = get_lines_from_file(sys.argv[1])
    svg_translator = Gcode2Svg()
    for line in lines:
        svg_translator.add_gcode_line(line)
    print svg_translator.get_svg_document()
 