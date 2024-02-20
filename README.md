# Prototype python library

This library is implemented for educational purposes

Library modules:
 - Calculations 
 - Forecasts 
 - Optimizers 
 - Utilities

**Calculations**  
This module is designed to perform calculations with always deterministic results in accordance with the formulas

**Forecasts**  
This module is designed to perform forecasts using data science technologies (linear models, gradient boosting, 
neural networks, time series, etc.)

**Optimizers**  
This module is designed to solve mixed-integer programming problems

**Utilities**  
This section introduces helper classes and functions

To update the library you need:
1. Refactor code
2. Update requirements if it needs
3. Update the library version number
4. In the terminal, run the following commands sequentially:
 - python setup.py sdist bdist_wheel
 - twine upload --repository pypi dist/*