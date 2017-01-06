# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 12:14:50 2016

@author: sigurdja
"""


import psspy
from psse_models import wrappers
import numpy as np
_i = psspy.getdefaultint()


class Load(object):
    """Base class for load models."""
    def __init__(self, bus_id):
        """
            Constructor for the vbase load class.
            Input:
                bus_id: The bus number to add to the load model
        """

        self.bus_id = bus_id

    def step(self, value):
        """
            Wrapper around psspy scal_2 to step the load.
            Input:
                value: the load increase or decrease
        """
        wrappers.one_bus_subsys(1, self.bus_id)
        psspy.scal_2(1, 0, 1, [0, 0, 0, 0, 0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        psspy.scal_2(0, 1, 2, [_i, 3, 1, 1, 0], [value, 0, 0.0, -.0, 0.0, -.0, 0.0])


class TimeSeriesLoad(Load):
    """Load that steps through a time series."""
    def __init__(self, bus_id, load_steps):
        """Constructor
            Input:
                bus_id: The number of the bus to model
                steps: The number of
        """
        super(TimeSeriesLoad, self).__init__(bus_id)
        self.samples = load_steps
        self.prev = 0.0

    def step(self, step):
        """ Perform load step
            Input:
                step: The current time step
        """
        self.prev = self.samples[step-1] - self.prev
        super(TimeSeriesLoad, self).step(self.prev)


class WhiteNoiseLoad(TimeSeriesLoad):
    """Load that behaves as white noise."""
    def __init__(self, bus_id, steps, std):
        """Constructor
            Input:
                bus_id: The number of the bus to model
                steps: The number of the load steps in p.u.
                std: The standard deviation
        """
        base = wrappers.get_total_bus_load(bus_id)
        std = std*abs(base)
        if std > 0:
            steps = np.random.normal(0, std, size=steps)
        else:
            steps = [0.0] * steps

        super(WhiteNoiseLoad, self).__init__(bus_id, steps)
        self.std = std


class WienerProcessLoad(WhiteNoiseLoad):
    """Load that behaves like a Wiener process."""
    def __init__(self, bus_id, steps, std, td):
        """Constructor
            Input:
                bus_id: The bus number of the load to model
                steps: The number of load steps
                std: The standard deviation of the load
                td: The time step
        """
        super(WienerProcessLoad, self).__init__(bus_id, steps, std)
        self.sqrt_td = np.sqrt(td)

    def step(self, step):
        Load.step(self, self.samples[step-1]*self.sqrt_td)
