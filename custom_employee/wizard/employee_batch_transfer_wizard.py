from odoo import fields, models, api



class EmployeeBatchTransferWizard(models.TransientModel):
    _name = 'employee.batch.transfer.wizard'
    
    
    employee_id = fields.Many2one('hr.employee', string="Employee")
    designation = fields.Many2one('hr.job', 'Designation', related="employee_id.job_id")
    date_of_transfer = fields.Date('Date Of Transfer')
    department = fields.Many2one('hr.department', 'Department', related="employee_id.department_id")
    contact_no = fields.Char('Contact No', related='employee_id.mobile_phone')
    reason_for_tranfer = fields.Text('Reason For Transfer', required=True)
    transferred_site = fields.Many2one('hr.department', string="Transferred Site", required=True)
    reporting_officer_of_site = fields.Many2one('hr.job', string="Reporting Officer Of Site", required=True)
    released_by = fields.Many2one('res.users', string="Released By", required=True, default=lambda self: self.env.user)
    phone_number = fields.Char('Phone Number', required=True)
    effective_date_ton_the_transferred_site = fields.Date('Effective Date To Join The Transferred Site',required=True)
    
    @api.model
    def create(self, vals):
        """ Automatically send email after saving transfer details. """
        record = super(EmployeeBatchTransferWizard, self).create(vals)

        # Assign the employee to the new department/site
        if record.employee_id and record.transferred_site:
            record.employee_id.department_id = record.transferred_site.id

        # Send email notification
        template = self.env.ref('custom_employee.email_template_employee_transfer', raise_if_not_found=False)
        if template:
            template.send_mail(record.employee_id.id, force_send=True)
    
        return record
    