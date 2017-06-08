# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes
import effortcomptagegrillesParams as pms


logger = logging.getLogger("le2m")


class PartieECG(Partie):
    __tablename__ = "partie_effortcomptagegrilles"
    __mapper_args__ = {'polymorphic_identity': 'effortcomptagegrilles'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsECG')

    def __init__(self, le2mserv, joueur):
        super(PartieECG, self).__init__(
            nom="effortcomptagegrilles", nom_court="ECG",
            joueur=joueur, le2mserv=le2mserv)
        self.ECG_gain_ecus = 0
        self.ECG_gain_euros = 0

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the historic
        :param periode:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsECG(period)
        self.le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Display the decision screen on the remote
        Get back the decision
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        self.currentperiod.ECG_grids = yield(self.remote.callRemote(
            "display_decision", pms.get_grilles()))
        self.currentperiod.ECG_decisiontime = (datetime.now() - debut).seconds
        self.joueur.info(u"{}".format(self.currentperiod.ECG_grids))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        if self.currentperiod.ECG_grids == pms.NB_GRILLES:
            self.currentperiod.ECG_periodpayoff = pms.PAYOFF
        else:
            self.currentperiod.ECG_periodpayoff = 0

        self.currentperiod.ECG_cumulativepayoff = self.currentperiod.ECG_periodpayoff
        logger.debug(u"{} Period Payoff {}".format(
            self.joueur,
            self.currentperiod.ECG_periodpayoff))

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        """
        Compute the payoff for the part and set it on the remote.
        The remote stores it and creates the corresponding text for display
        (if asked)
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))

        self.ECG_gain_ecus = self.currentperiod.ECG_cumulativepayoff
        self.ECG_gain_euros = float(self.ECG_gain_ecus) * float(pms.TAUX_CONVERSION)
        yield (self.remote.callRemote(
            "set_payoffs", self.ECG_gain_euros, self.ECG_gain_ecus))

        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.ECG_gain_ecus, self.ECG_gain_euros))


class RepetitionsECG(Base):
    __tablename__ = 'partie_effortcomptagegrilles_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_effortcomptagegrilles.partie_id"))

    ECG_period = Column(Integer)
    ECG_treatment = Column(Integer)
    ECG_group = Column(Integer)
    ECG_grids = Column(Integer)
    ECG_decisiontime = Column(Integer)
    ECG_periodpayoff = Column(Float)
    ECG_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.ECG_treatment = pms.TREATMENT
        self.ECG_period = period
        self.ECG_grids = 0
        self.ECG_decisiontime = 0
        self.ECG_periodpayoff = 0
        self.ECG_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns
                if "ECG" in c.name}
        if joueur:
            temp["joueur"] = joueur
        return temp

