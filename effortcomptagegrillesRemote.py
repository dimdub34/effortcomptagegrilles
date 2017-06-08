# -*- coding: utf-8 -*-

import logging
import random

from twisted.internet import defer
from client.cltremote import IRemote
import effortcomptagegrillesParams as pms
from effortcomptagegrillesGui import DEffort


logger = logging.getLogger("le2m")


class RemoteECG(IRemote):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)

    def remote_configure(self, params):
        """
        Set the same parameters as in the server side
        :param params:
        :return:
        """
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, period):
        """
        Set the current period and delete the history
        :param period: the current period
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period

    def remote_display_decision(self, grilles):
        logger.debug(u"{} display_effort".format(self.le2mclt.uid))
        if self.le2mclt.simulation:
            answers = 0
            for i in range(len(grilles)):
                answers += random.randint(0, 1)  # 1 if success, 0 otherwise
            logger.info(u"{} send back {}".format(self.le2mclt.uid, answers))
            return answers
        else:
            defered = defer.Deferred()
            screen_effort = DEffort(
                defered, self.le2mclt.automatique, self.le2mclt.screen, grilles)
            screen_effort.show()
            return defered

