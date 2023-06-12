import logging

from zeep import Client

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WiservNotificationManager(models.Model):
    _name = "g2p.program.notification.manager.wiserv"
    _description = "Wiserv Notification Manager"
    _inherit = [
        "g2p.base.program.notification.manager",
        "g2p.manager.source.mixin",
        "mail.thread",
        "mail.activity.mixin",
    ]

    notification_types = ("sms", "both")

    api_url = fields.Char("API URL", required=True)
    user_name = fields.Char(required=True)
    wiserv_password = fields.Char("Password", required=True)

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
        # program_memberships = self.env['g2p.program_membership'].sudo().browse(15)
        for mem in program_memberships:
            if (
                mem.partner_id.notification_preference in self.notification_types
                and mem.partner_id.phone
                and send_sms_body_list.get(mem.id, None)
            ):
                if self.api_url and self.user_name and self.wiserv_password:
                    try:
                        client = Client(self.api_url)
                        response = client.service.sendMessage(
                            UserName=self.user_name,
                            PassWord=self.wiserv_password,
                            MobileNo=mem.partner_id.phone,
                            Message=send_sms_body_list[mem.id],
                        )
                        _logger.debug("$$------------Response%s", response)
                        return response
                    except Exception as e:
                        # Handle general exception
                        _logger.exception("Error occurred during sendMessage:%s" % e)
                        error_msg = f"Error occurred during sendMessage to this partner: {mem.partner_id.name} ⟶ {e}"
                        self.message_post(
                            body=error_msg, subject=_("Wirserv Failure Response")
                        )
                        return None
                else:
                    raise UserError(
                        _("Please configure Wiserv SMS configuration correctly.")
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
