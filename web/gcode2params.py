#!/usr/bin/env python
import unittest


import sys
import re
      
class Gcode2Params(object):
    
    def __init__(self, title, params, state = {}, ):
        self.line_nb = 0
        self.title = title
        self.params = params
        self.state = {'x':0.,
                    'y':0., 
                    'z':0., 
                    'f':0., 
                    'tool_dia':1, 
                    'units':'default',
                     }
        
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
        # "3 x[2*0.5] 
        if( len(toks[0].strip()) > 0):
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
            v = self.state[k] 
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
                self.state['units'] = 'mm'
            if params['g'] == 21.:
                unit_change = True
                self.state['units'] = 'inches'
        if not unit_change:
            self.state.update(params)
            self.__min_max_updates()



if __name__ == "__main__":
    p1 = 0
    p2 = 69
    params = Gcode2Params('title', locals())
    params.add_gcode_line("g3 x0.5175 y0.0000 i[-1.0 * 0.1250] j0 z0.000")
    
    code_dict =  params.gcode_params[0][2]
    print code_dict
    assert(code_dict['g'] == 3.0)
    assert(code_dict['x'] == 0.5175)
    assert(code_dict['i'] == -0.125)
    assert(code_dict['z'] == 0.)
    
    assert(params.params['p2'] == 69)