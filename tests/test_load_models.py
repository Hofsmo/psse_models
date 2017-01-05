import os
import psspy
import pytest
import numpy as np
from numpy import testing
from psse_models import wrappers
from psse_models import load_models

@pytest.fixture(scope='module')
def network():
    """Set up the PSS/E case"""
    cwd = os.path.dirname(__file__)
    casename = os.path.join(cwd, 'cases/simple.sav')
    psspy.psseinit(10)
    psspy.case(casename)

    return {'load_bus': 1, 'gen': 2, 'load': 100.0}

def test_time_series_step(network):
    """Test the time series load steps"""
    step = 1
    steps = [step, 0]

    load = load_models.TimeSeriesLoad(network['load_bus'], steps)

    for idx, val in enumerate(steps):
        correct = network['load'] + val
        load.step(idx+1)
        value = wrappers.get_total_bus_load(network['load_bus'])
        testing.assert_almost_equal(value, correct)

def test_step(network):
    """Test the load step method."""
    load = load_models.Load(network['load_bus'])
    load.step(10)
    value = wrappers.get_total_bus_load(network['load_bus'])
    testing.assert_almost_equal(value, network['load']+10)

    load.step(-10)

def test_white_noise_load(network):
    """Test the WhiteNoiseLoad class."""
    std_pu = 0.01
    load = load_models.WhiteNoiseLoad(network['load_bus'], 10000, std_pu)

    # Calculate the standard deviation of the generated steps
    std = np.std(load.samples)

    # Calculate what the standard deviation should be 
    corr = network['load']*std_pu

    testing.assert_almost_equal(std, corr, 1)
    
