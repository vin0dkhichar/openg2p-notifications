from odoo import models

from odoo.addons.g2p_programs.models import constants


class G2PProgramMembership(models.Model):
    _inherit = "g2p.program_membership"

    def enroll_eligible_registrants(self):
        res = super(G2PProgramMembership, self).enroll_eligible_registrants()
        if res and res.get("params", {}).get("type", None) == "success":
            for manager in self.program_id.get_managers(constants.MANAGER_NOTIFICATION):
                manager.on_enrolled_in_program(self)
            self.is_enrolled_notification_sent = True
        return res
