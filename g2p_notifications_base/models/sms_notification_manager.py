from odoo import models


class SMSNotificationManager(models.Model):
    _inherit = "g2p.program.notification.manager.sms"

    notification_types = ("sms", "both")

    # TODO: To be Implemented.
