#!/usr/bin/env python


import sys
import re

class Gcode2Svg(object):
    
    def __init__(self, state = {'x':0.,
                                'y':0., 
                                'z':0., 
                                'f':0., 
                                'tool_dia':1, 
                                'svg_scaling':100.,
                                'stock_w':1., 
                                'stock_h':1., 
                                'stock_x0':0.,
                                'stock_y0':0.,
                                'stock_dz':-1.
                                 
                                }):
        self.line_nb = 0
        self.state = {}
        self.state.update(state)
        self.floating_point_regex = re.compile('[-+]?[0-9]*\.?[0-9]+')
        self.gcode_params = []
        self.min_max = {'x':[self.state['x'],self.state['x']],
                        'y':[self.state['y'],self.state['y']],
                        'z':[self.state['z'],self.state['z']], }
    
    
    def __collect_extra_params(self, line, params):
        # put them in the state
        toks = line.split('hugomatic')
        if len(toks) > 1:
            for hu in toks[1:]:
                toks = hu.split('[')
                if len(toks) > 1:
                    s = toks[1]
                    toks = s.split(']')
                    if len(toks) >1:
                        param = toks[0]
                        param = param.replace('"','')
                        param = param.replace("'",'')
                        toks = toks[1].split('=')
                        if len(toks) > 1:
                            value_str = toks[1].strip()
                            f = self.__get_float_from_expression(value_str)
                            params[param] = f
                
    
    def __get_float_from_string(self,str):
        try:
            m = self.floating_point_regex.match(str)
            float_string =  m.group()
        except:
            print "Error matching '%s' to float" % str
            raise 
        f = float(float_string)
        return f
                
    def __get_float_from_expression(self, expression):
        
        toks = expression.split('[')
        if len(toks) == 1:
            f = self.__get_float_from_string(expression)
            return f
        s = toks[1]
        str = s.split(']')[0]
        return eval(str)
        #print "******* %s *****" % str

    
    def __collect_float_param(self, param_names, line, params):    
        
        for param in param_names:
            try:
                toks = line.split(param)
                if len(toks)>1:
                    number_str = toks[1].strip()
                    f = self.__get_float_from_expression(number_str)
                    params[param] = f
            except:
                print "Get_param error param = '%s', line = '%s'" % (param, line)
                raise     
            
    def __min_max_updates(self):
        for k in ('x','y','z'):
            v = self.state[k] * self.state['svg_scaling']
            if v < self.min_max[k][0]:
                self.min_max[k][0] =  v
            if v > self.min_max[k][1]:
                self.min_max[k][1] =  v
    
                   
    def add_gcode_line(self, line):
        text = line
        self.line_nb += 1
        params = {}
        self.__collect_extra_params(line, params)
        line = line.split('(')[0] # remove comments
        line = line.lower()
        line = line.strip()
        self.__collect_float_param( ('g','x','y','z','f', 'i', 'j', 'p', 'r', 'm', 'q' ), line, params)
        current_state = dict(self.state)
        self.gcode_params.append( (self.line_nb, text.strip(), params, current_state)  )
#        del params['r']
#        del params['m']
#        del params['q']
#        del params['i']
#        del params['j']
        
        unit_change = False
        if params.has_key('g'):
            if params['g'] == 20.:
                unit_change = True
                self.state['svg_scaling'] = 100.0
            if params['g'] == 21.:
                unit_change = True
                self.state['svg_scaling'] = 2.54
        if not unit_change:
            self.state.update(params)
            self.__min_max_updates()

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
        
        xmin = self.min_max['x'][0]
        xmax = self.min_max['x'][1]
        ymin = self.min_max['y'][0]
        ymax = self.min_max['y'][1]
      
        dx = xmax - xmin
        dy = ymax - ymin
        
        mid_point = ((xmin + xmax)/2, (ymin + ymax)/2)
        
        dx += 50.
        dy += 50.
    
        translate_x = dx/2 - mid_point[0]
        translate_y = dy/2 - mid_point[1]
        
        header = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!-- Created with Hugomatic (http://hugomatic.ca/) -->
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
    translator = Gcode2Svg()
    for line in lines:
        translator.add_gcode_line(line)
    print translator.get_svg_document()
