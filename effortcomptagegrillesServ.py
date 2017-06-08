# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
from util.utili18n import le2mtrans
import effortcomptagegrillesParams as pms
from effortcomptagegrillesGui import DConfig
from effortcomptagegrillesTexts import trans_ECG


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen)
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self._configure
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[le2mtrans(u"Start")] = lambda _: self._demarrer()
        actions[le2mtrans(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("effortcomptagegrilles")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Effort comptage grilles", actions)

    def _configure(self):
        # self._le2mserv.gestionnaire_graphique.display_information(
        #     le2mtrans(u"There is no parameter to configure"))
        # return
        screen_conf = DConfig(self._le2mserv.gestionnaire_graphique.screen)
        if screen_conf.exec_():
            to_display = [u"Nb grids: {}".format(pms.NB_GRILLES),
                          u"Grids' size: {}".format(pms.SIZE_GRILLES),
                          u"Time: {}".format(str(pms.TIME_TO_FILL_GRILLES)),
                          u"Payoff: {}".format(pms.PAYOFF)]
            self._le2mserv.gestionnaire_graphique.infoserv(to_display)

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        # check conditions =====================================================
        if not self._le2mserv.gestionnaire_graphique.question(
                        le2mtrans(u"Start") + u" effortcomptagegrilles?"):
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "effortcomptagegrilles", "PartieECG",
            "RemoteECG", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'effortcomptagegrilles')

        # set parameters on remotes
        yield (self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Configure"), self._tous, "configure"))
        
        # Start part ===========================================================
        # init period
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "newperiod", 0))

        # decision
        yield(self._le2mserv.gestionnaire_experience.run_step(
            trans_ECG(u"Grids"), self._tous, "display_decision"))

        # period payoffs
        self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
            "effortcomptagegrilles")

        # End of part ==========================================================
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "effortcomptagegrilles"))
