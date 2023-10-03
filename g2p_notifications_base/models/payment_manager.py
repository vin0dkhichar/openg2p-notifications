import logging

from odoo import models

from odoo.addons.g2p_programs.models import constants

_logger = logging.getLogger(__name__)


class DefaultPaymentManager(models.Model):
    _inherit = "g2p.program.payment.manager.default"

    def send_payments(self, batches):
        res = super(DefaultPaymentManager, self).send_payments(batches)
        if res and batches:
            for manager in self.program_id.get_managers(constants.MANAGER_NOTIFICATION):
                for batch in batches:
                    manager.on_payment_send(batch)
        return res
