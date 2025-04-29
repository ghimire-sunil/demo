from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    def action_employee_branch_transfer(self):
        print("hello")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employee Branch Transfer',
            'res_model': 'employee.batch.transfer.wizard',
            'target': 'new',
            'view_mode': 'form',
            'context': {'default_employee_id': self.id},
        }

  