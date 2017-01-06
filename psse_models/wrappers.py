"""Module containing useful psse function wrappers."""

import psspy

def one_bus_subsys(sid, bus_id):
    """Function to create a subsys consisting of one bus.
        Input:
            sid: The id of the subsystem
            bus_id: The number of the bus
    """

    psspy.bsys(sid, 0, [0.0, 0.0], 0, [], 1, [bus_id], 0, [], 0, [])


def get_total_bus_load(bus_id):
    """Wraper to get total bus load."""
    one_bus_subsys(1, bus_id)
    return psspy.alodbusreal(sid=1, flag=2, string='O_TOTALACT')[1][0][0]
