from odoo import fields, models


class G2PRegistrant(models.Model):
    _inherit = "res.partner"

    def _default_notification_preference(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("g2p_notifications_base.default_notification_preference", "none")
        )

    notification_preference = fields.Selection(
        [
            ("none", "None"),
            ("email", "Email"),
            ("sms", "SMS"),
            ("both", "Both Email & SMS"),
        ],
        default=_default_notification_preference,
    )


class G2PProgramMembership(models.Model):
    _inherit = "g2p.program_membership"

    is_enrolled_notification_sent = fields.Boolean(default=False)


class G2PPayment(models.Model):
    _inherit = "g2p.payment"

    is_payment_notification_sent = fields.Boolean(default=False)
