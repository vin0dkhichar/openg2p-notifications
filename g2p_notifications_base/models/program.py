import logging

from odoo import _, models
from odoo.exceptions import UserError

from odoo.addons.g2p_programs.models import constants

_logger = logging.getLogger(__name__)


class G2PProgram(models.Model):
    _inherit = "g2p.program"

    def notify_eligible_beneficiaries(self):
        # TODO: Convert async
        partners_to_notify = [
            mem
            for mem in self.program_membership_ids
            if mem.state in ("enrolled",) and not mem.is_enrolled_notification_sent
        ]
        notification_managers = self.get_managers(constants.MANAGER_NOTIFICATION)
        if notification_managers:
            for manager in notification_managers:
                if manager:
                    manager.manager_ref_id.on_enrolled_in_program(partners_to_notify)
            for mem in partners_to_notify:
                mem.is_enrolled_notification_sent = True
        else:
            raise UserError(_("No Notification Manager defined."))
