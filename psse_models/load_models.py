# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 12:14:50 2016

@author: sigurdja
"""

import psspy
import numpy as np
_i=psspy.getdefaultint()

class Load(object):
    def __init__(self, bus_id, steps):
        self.bus_id = bus_id
        self.steps = steps
        
    def step(self, value):
        psspy.bsys(1,0,[0.0,0.0],0,[],1,[self.bus_id],0,[],0,[])
        psspy.scal_2(1,0,1,[0,0,0,0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        psspy.scal_2(0,1,2,[_i,3,1,1,0],[value, 0,0.0,-.0,0.0,-.0, 0.0])
        
class TimeSeriesLoad (Load):
    def __init__(self, bus_id, steps, load_steps):
        super(TimeSeriesLoad, self).__init__(bus_id, steps)
        self.samples = load_steps
        self.prev = 0.0
        
    def step(self, step):
        self.prev = self.samples[step-1] - self.prev
        super(TimeSeriesLoad, self).step(self.prev)
        
        
class WhiteNoiseLoad(TimeSeriesLoad):
    def __init__(self, bus_id, steps, std):
        super(WhiteNoiseLoad, self).__init__(bus_id, steps,
                                         np.random.normal(0, std, size=steps))
        self.std = std

class WienerProcessLoad(WhiteNoiseLoad):
    def __init__(self, bus_id, steps, std, td):
        super(WienerProcessLoad, self).__init__(bus_id, steps, std)
        self.sqrt_td = np.sqrt(td)
                
    def step(self, step):
        super(TimeSeriesLoad, self).step(self.samples[step]*self.sqrt_td)