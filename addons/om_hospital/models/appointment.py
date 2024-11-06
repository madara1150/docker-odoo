from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    _order = "name desc"

    name = fields.Char(
        string="Order Reference",
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: _("New"),
    )
    note = fields.Text(string="Description")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )

    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    patient_name_id = fields.Many2one(
        "hospital.patient", string="Patient Name", required=True
    )
    age = fields.Integer(string="Age", related="patient_id.age", tracking=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")], string="gender"
    )

    date_appointment = fields.Date(string="date")
    date_checkup = fields.Datetime(string="Check up Time")
    prescription = fields.Text(string="Prescription")
    prescription_line_ids = fields.One2many(
        "appointment.prescription.lines", "appointment_id", string="Prescription Lines"
    )

    def action_confirm(self):
        self.state = "confirm"

    def action_done(self):
        self.state = "done"

    def action_draft(self):
        self.state = "draft"

    def action_cancel(self):
        self.state = "cancel"

    @api.model
    def create(self, vals):
        if not vals.get("note"):
            vals["note"] = "New Patient"
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "hospital.appointment"
            ) or _("New")
        res = super(HospitalAppointment, self).create(vals)
        return res

    @api.onchange("patient_id")
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
        else:
            self.gender = ""

    def unlink(self):
        if self.state == "done":
            raise ValidationError(
                "You Cannot Delete %s as it is in Done state" % self.name
            )
        return super(HospitalAppointment, self).unlink()

    def action_url(self):
        return {
            "type": "ir.actions.act_url",
            "target": "new",
            "url": "https://www.google.%s" % self.prescription,
        }


class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine")
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")
