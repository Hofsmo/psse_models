# psse_models
Place where I gather my PSSE Python models.
At the moment I only have some load models and wrapper functions and some examples demonstrating how to use the load models

## load_models
The load models I have created to be used in dynamic simulations

### Load
This is the base class. It can perform a load step of a specified size

### TimeSeriesLoad
This class is derived from the Load class. It takes in an array of load values and sets the load value to one of these at every time step

### WhiteNoiseLoad
This class is derived from the TimeSeriesLoad class it takes in the mean and standard deviation and generates a white noise time series.

### WienerProcessLoad
This class is derived from the WhiteNoiseLoad class it takes in the mean and standard deviation and generates a winer process |time series.

## examples
Here examples on how to use loads are gathered

### one_load_step
An example demonstrating how to use the code to run a dynamic simulation with a load step and plot the results.

### wiener_loads
This example shows how to make all the loads in a system behave as wiener processes. It also shows how to run the dynamic simulation in a loop.

## tests
All the load models are tested. The tests are compatible with pytest.

## Installation
It should be possible to install the module using setuptools

# Tips for setting up psspy 
I normally follow the second highest rated answer to this thread https://psspy.org/psse-help-forum/question/122/how-do-i-import-the-psspy-module-in-a-python-script/ . The highest rated answer requires one to add some boilerplate code to each script, the second highest has a solution which avoids this.
