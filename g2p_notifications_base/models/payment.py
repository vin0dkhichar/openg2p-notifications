import logging

from odoo import models

from odoo.addons.g2p_programs.models import constants

_logger = logging.getLogger(__name__)


class G2PCycle(models.Model):
    _inherit = "g2p.cycle"

    def send_payment(self):
        res = super(G2PCycle, self).send_payment()
        if res and self.payment_batch_ids:
            for manager in self.program_id.get_managers(constants.MANAGER_NOTIFICATION):
                for payment_batch in self.payment_batch_ids:
                    manager.on_payment_send(payment_batch)
        return res
