from unittest.mock import MagicMock
import sys
from ati_experiment import experiment

my_module = MagicMock()

sys.modules["RPi"] = my_module

experiment()
print("Test finished")
