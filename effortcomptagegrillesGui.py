# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""

import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import effortcomptagegrillesParams as pms
from effortcomptagegrillesTexts import trans_ECG
import effortcomptagegrillesTexts as texts_ECG
from client.cltgui.cltguiwidgets import WExplication, WCompterebours, WGrid


logger = logging.getLogger("le2m")


class DEffort(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, grilles):
        QtGui.QDialog.__init__(self, parent)

        self._defered = defered
        self._automatique = automatique
        self._grilles = grilles

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        explanation = WExplication(
            parent=self, text=texts_ECG.get_text_explanation_grilles(),
            size=(600, 100))
        layout.addWidget(explanation)

        self._countdown = WCompterebours(
            self, temps=pms.TIME_TO_FILL_GRILLES, actionfin=self._accept)
        layout.addWidget(self._countdown)

        grid_layout = QtGui.QGridLayout()
        layout.addLayout(grid_layout)

        self._widgets_grilles = list()
        current_line = 0
        for i, g in enumerate(self._grilles):
            self._widgets_grilles.append(WGrid(g, self._automatique))
            grid_layout.addWidget(
                self._widgets_grilles[-1], current_line,
                i - current_line * pms.NB_GRILLES_PER_LINE)
            if i > 0 and (i+1) % pms.NB_GRILLES_PER_LINE == 0:
                current_line += 1

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.adjustSize()
        self.setFixedSize(self.size())
        self.setWindowTitle(trans_ECG(u"Tasks"))

    def reject(self):
        pass

    def _accept(self):
        if self._countdown.is_running():
            confirmation = QtGui.QMessageBox.question(
                self, "Confirmation",
                trans_ECG(u"Do you want to quit before the end of the timer?"),
                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes:
                return
            else:
                self._countdown.stop()
        answers = sum([int(g.is_ok()) for g in self._widgets_grilles])
        if not self._automatique:
            QtGui.QMessageBox.information(
                self, "Information",
                trans_ECG(u"You've found {} grids.").format(answers))
        logger.info("send back {}".format(answers))
        self.accept()
        self._defered.callback(answers)


class DConfig(QtGui.QDialog):
    def __init__(self, ecran_serveur):
        QtGui.QDialog.__init__(self, ecran_serveur)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        form_layout = QtGui.QFormLayout()
        layout.addLayout(form_layout)
        
        # nb grids
        self._spinbox_nb_grids = QtGui.QSpinBox()
        self._spinbox_nb_grids.setMinimum(0)
        self._spinbox_nb_grids.setMaximum(30)
        self._spinbox_nb_grids.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self._spinbox_nb_grids.setFixedWidth(30)
        self._spinbox_nb_grids.setValue(pms.NB_GRILLES)
        form_layout.addRow(QtGui.QLabel(trans_ECG(u"Number of grids")),
                           self._spinbox_nb_grids)
        
        # grid size
        self._spinbox_grid_size = QtGui.QSpinBox()
        self._spinbox_grid_size.setMinimum(0)
        self._spinbox_grid_size.setMaximum(30)
        self._spinbox_grid_size.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self._spinbox_grid_size.setFixedWidth(30)
        self._spinbox_grid_size.setValue(pms.SIZE_GRILLES)
        form_layout.addRow(QtGui.QLabel(trans_ECG(u"Grids' size")),
                           self._spinbox_grid_size)
        
        # nb grids per line
        self._spinbox_nb_grids_perline = QtGui.QSpinBox()
        self._spinbox_nb_grids_perline.setMinimum(0)
        self._spinbox_nb_grids_perline.setMaximum(30)
        self._spinbox_nb_grids_perline.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self._spinbox_nb_grids_perline.setFixedWidth(30)
        self._spinbox_nb_grids_perline.setValue(pms.NB_GRILLES_PER_LINE)
        form_layout.addRow(QtGui.QLabel(trans_ECG(u"Number of grids per line")),
                           self._spinbox_nb_grids_perline)

        # time
        self._timeEdit = QtGui.QTimeEdit()
        self._timeEdit.setTime(QtCore.QTime(pms.TIME_TO_FILL_GRILLES.hour,
                                            pms.TIME_TO_FILL_GRILLES.minute,
                                            pms.TIME_TO_FILL_GRILLES.second))
        form_layout.addRow(QtGui.QLabel(trans_ECG(u"Time to fill the form")),
                           self._timeEdit)

        # payoff
        self._spinbox_payoff = QtGui.QSpinBox()
        self._spinbox_payoff.setMinimum(0)
        self._spinbox_payoff.setSingleStep(1)
        self._spinbox_payoff.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self._spinbox_payoff.setValue(pms.PAYOFF)
        form_layout.addRow(QtGui.QLabel(trans_ECG(u"Payoff")), self._spinbox_payoff)

        button = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        button.accepted.connect(self._accept)
        layout.addWidget(button)

        self.setWindowTitle(le2mtrans(u"Parameters"))
        self.adjustSize()

    def _accept(self):
        nb_grids = self._spinbox_nb_grids.value()
        grid_size = self._spinbox_grid_size.value()
        nb_grids_perline = self._spinbox_nb_grids_perline.value()
        time_to_fill = self._timeEdit.time().toPyTime()
        payoff = self._spinbox_payoff.value()
        txt_confirm = trans_ECG(u"Do you confirm?") + u'\n' + \
                      trans_ECG(u"Number of grids") + u": {}\n".format(nb_grids) + \
                      trans_ECG(u"Grids' size") + u": {}\n".format(grid_size) + \
                      trans_ECG(u"Number of grids per line") + u": {}\n".format(nb_grids_perline) + \
                      trans_ECG(u"Time to fill the form") + u": {}\n".format(
            str(time_to_fill)) + trans_ECG(u"Payoff") + u": {}".format(payoff)
        confirm = QtGui.QMessageBox.question(
            self, le2mtrans(u"Confirmation"), txt_confirm,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if confirm != QtGui.QMessageBox.Yes:
            return
        pms.NB_GRILLES = nb_grids
        pms.SIZE_GRILLES = grid_size
        pms.NB_GRILLES_PER_LINE = nb_grids_perline
        pms.TIME_TO_FILL_GRILLES = time_to_fill
        pms.PAYOFF = payoff
        self.accept()
