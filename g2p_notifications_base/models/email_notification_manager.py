import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class EmailNotificationManager(models.Model):
    _name = "g2p.program.notification.manager.email"
    _description = "Email Notification Manager"
    _inherit = ["g2p.base.program.notification.manager", "g2p.manager.source.mixin"]

    notification_types = ("email", "both")

    send_immediately = fields.Boolean(default=False)

    on_enrolled_in_program_template = fields.Many2one("mail.template")
    on_cycle_started_template = fields.Many2one("mail.template")
    on_cycle_ended_template = fields.Many2one("mail.template")

    def on_enrolled_in_program(self, program_memberships):
        if not self.on_enrolled_in_program_template:
            return
        # TODO: Make the following asynchrous and in bulk
        for mem in program_memberships:
            if (
                mem.partner_id.notification_preference in self.notification_types
                and mem.partner_id.email
            ):
                self.on_enrolled_in_program_template.send_mail(
                    mem.id, force_send=self.send_immediately
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
