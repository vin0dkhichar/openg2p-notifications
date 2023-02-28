from odoo import fields, models


class G2PRegistrant(models.Model):
    _inherit = "res.partner"

    notification_preference = fields.Selection(
        [("none", "None"), ("email", "Email"), ("sms", "SMS"), ("both", "Both")],
        default="none",
    )


class G2PProgramMembership(models.Model):
    _inherit = "g2p.program_membership"

    is_enrolled_notification_sent = fields.Boolean(default=False)
