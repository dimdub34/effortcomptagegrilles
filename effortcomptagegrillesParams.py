# -*- coding: utf-8 -*-
"""=============================================================================
This modules contains the variables and the parameters.
Do not change the variables.
Parameters that can be changed without any risk of damages should be changed
by clicking on the configure sub-menu on the server screen.
If you need to change some parameters below please be sure of what you do,
which means that you should ask to the developer ;-)
============================================================================="""

from util import utiltools
from datetime import time


# variables --------------------------------------------------------------------
BASELINE = 0
TREATMENTS_NAMES = {BASELINE: "Baseline"}

# parameters -------------------------------------------------------------------
TREATMENT = BASELINE
TAUX_CONVERSION = 1
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 0
MONNAIE = u"None"

NB_GRILLES = 5
SIZE_GRILLES = 8
NB_GRILLES_PER_LINE = 5
TIME_TO_FILL_GRILLES = time(0, 2, 0)  # hours, minutes, seconds
PAYOFF = 20


def get_grilles():
    return utiltools.get_grids(NB_GRILLES, SIZE_GRILLES)
