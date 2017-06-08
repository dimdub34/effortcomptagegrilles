# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import effortcomptagegrillesParams as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext
import logging

logger = logging.getLogger("le2m")
try:
    localedir = os.path.join(params.getp("PARTSDIR"), "effortcomptagegrilles",
                             "locale")
    trans_ECG = gettext.translation(
      "effortcomptagegrilles", localedir, languages=[params.getp("LANG")]).ugettext
except (AttributeError, IOError):
    logger.critical(u"Translation file not found")
    trans_ECG = lambda x: x  # if there is an error, no translation


def get_text_explanation_grilles():
    text = trans_ECG(u"Please count the number of 1 in each grid.")
    return text


def get_grille_to_html(grille):
    html = "<table style='width: 150px;'>"
    for l in grille:
        html += "<tr>"
        for c in l:
            html += "<td style='width: 15px;'>{}</td>".format(c)
        html += "</tr>"
    html += "</table>"
    return html



