import logging

import requests

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Fast2SMSNotificationManager(models.Model):
    _name = "g2p.program.notification.manager.fast2sms"
    _description = "Fast2SMS Notification Manager"
    _inherit = ["g2p.base.program.notification.manager", "g2p.manager.source.mixin"]

    notification_types = ("sms", "both")

    send_api_endpoint = fields.Char("Send API Endpoint", required=True)
    access_token = fields.Char(required=True)
    sms_language = fields.Char("SMS Language", default="english")
    sms_route = fields.Char("SMS Route", default="q")

    on_enrolled_in_program_template = fields.Many2one("sms.template")
    on_cycle_started_template = fields.Many2one("sms.template")
    on_cycle_ended_template = fields.Many2one("sms.template")

    def on_enrolled_in_program(self, program_memberships):
        if not self.on_enrolled_in_program_template:
            return
        # TODO: Make the following asynchrous and in bulk
        send_sms_body_list = self.on_enrolled_in_program_template._render_template(
            self.on_enrolled_in_program_template.body,
            "g2p.program_membership",
            [mem.id for mem in program_memberships],
        )
        for mem in program_memberships:
            if (
                mem.partner_id.notification_preference in self.notification_types
                and mem.partner_id.phone
                and send_sms_body_list.get(mem.id, None)
            ):
                requests.post(
                    self.send_api_endpoint,
                    data={
                        "message": send_sms_body_list[mem.id],
                        "language": self.sms_language,
                        "route": self.sms_route,
                        "numbers": mem.partner_id.phone,
                    },
                    headers={
                        "authorization": self.access_token,
                    },
                )

    def on_cycle_started(self, program_memberships, cycle_id):
        if not self.on_cycle_started_template:
            return
        # TODO: to be implemented
        return

    def on_cycle_ended(self, program_memberships, cycle_id):
        if not self.on_cycle_ended_template:
            return
        # TODO: to be implemented
        return
