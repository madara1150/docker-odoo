from odoo import _, api, fields, models


class SearchAppointmentWizard(models.TransientModel):
    _name = "search.appointment.wizard"
    _description = "search Appointment Wizard"

    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)

    def action_search_appointment_m1(self):
        action = self.env.ref("om_hospital.action_hospital_appointment").read()[0]
        action["domain"] = [("patient_id", "=", self.patient_id.id)]

    def action_search_appointment_m2(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "om_hospital.action_hospital_appointment"
        )
        action["domain"] = [("patient_id", "=", self.patient_id.id)]
        return action

    def action_search_appointment_m3(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Appointments",
            "res_model": "hospital.appointment",
            "view_type": "form",
            "domain": [("patient_id", "=", self.patient_id.id)],
            "view_mode": "tree,form",
            "target": "current",
        }
        return action
