from unittest.mock import MagicMock

my_module = MagicMock()
import sys

sys.modules["RPi"] = my_module

from ati_experiment import experiment

experiment()
