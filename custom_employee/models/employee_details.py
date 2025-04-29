import logging
import calendar
from odoo.exceptions import UserError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
import re
import magic
import base64
import mimetypes
import logging

_logger = logging.getLogger(__name__)
    
class HrEmployeeclass(models.Model):
    _inherit ="hr.employee"
    employment_details_ids = fields.One2many('hr.employment.details', 'employee_id', string='Employment Details')
    family_details_ids = fields.One2many(
        'hr.family.details', 'employee_id', string="Family Details"
    )
    documents_details_ids = fields.One2many('hr.documents.details', 'employee_id', string="Documents Details")
    emp_blood_group = fields.Selection(
        string="Blood Group",
        selection=[
            ('a_positive', 'A+'),
            ('a_negative', 'A-'),
            ('b_positive', 'B+'),
            ('b_negative', 'B-'),
            ('ab_positive', 'AB+'),
            ('ab_negative', 'AB-'),
            ('o_positive', 'O+'),
            ('o_negative', 'O-'),
        ]
    )
    relationship = fields.Char(String="Relationship")
    # temporary_address = fields.Char(String="Temporary Address")
    province = fields.Many2one('res.province', 'Province')
    district = fields.Many2one('res.district', 'District')
    municipality = fields.Many2one('res.municipality', string = 'Municipality')
    ward_no = fields.Many2one('res.ward', string= "Ward No")
    house_no = fields.Char(String="House No")
    contact_no = fields.Char(String="Contact No")
    city_name = fields.Char(String="City Name")
    parmanent_account_number = fields.Char(
        String="Permanent Account Number (PAN)")
    provident_fund_number = fields.Char(string="Provident Fund Number")
    ssf_no = fields.Char(String="SSF Number")
    cit_number = fields.Char(String="CIT Number")
    gratuity_number = fields.Char(String="Gratuity Number")
    national_card_id_no = fields.Char(String="National Card ID NO")
    religion = fields.Selection([
        ('christianity', 'Christianity'),
        ('islam', 'Islam'),
        ('hinduism', 'Hinduism'),
        ('buddhism', 'Buddhism'),
        ('judaism', 'Judaism'),
        ('baháí_faith', 'Baháí Faith'),
        ('sikhism', 'Sikhism')
    ], string="Religion")
    current_age = fields.Char(string="Current Age", readonly=True)
    
    num_sons = fields.Integer(string="Number of Sons", default=0)
    num_daughters = fields.Integer(string="Number of Daughters", default=0)
    children = fields.Integer(
        string="Number of Dependent Children",
        compute='_compute_children',
        store=True
    )

    @api.depends('num_sons', 'num_daughters')
    def _compute_children(self):
        for record in self:
            record.children = record.num_sons + record.num_daughters
    @api.onchange('birthday')
    def _onchange_birthday(self):
        for record in self:
            if record.birthday:
                today = date.today()
                # Calculate the age in full years
                age = today.year - record.birthday.year - \
                    ((today.month, today.day) < (record.birthday.month, record.birthday.day))
                record.current_age = str(age)
            else:
                record.current_age = ''


class ConstructionEmployeeFamilyMembers(models.Model):
    _name = "hr.family.details"
    _description = "Family Details"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    sno = fields.Char(string='S.NO', compute='_compute_sno', store=True, readonly=True)
    relationship = fields.Selection([
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('spouse', 'Spouse'),
        ('sibling', 'Sibling'),
        ('children', 'Children')],
        string="Relationship"
    )
    name = fields.Char(string="Name")
    nationality = fields.Many2one(
        "res.country",
        string="Nationality",
        default=lambda self: self.env['res.country'].search([('code', '=', 'NP')], limit=1)
    )
    age = fields.Integer(string="Age")
    occupation = fields.Char(string="Occupation")
    organization = fields.Char(string="Organization")
    phone_number = fields.Char(string="Phone No")

    @api.depends('employee_id.family_details_ids')
    def _compute_sno(self):
        """Compute serial numbers based on the line sequence."""
        for employee in self.mapped('employee_id'):
            for index, line in enumerate(employee.family_details_ids, start=1):
                line.sno = str(index) 
                
class EmploymentDetails(models.Model):
    _name = 'hr.employment.details'
    _description = 'Employment Details'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade')
    sno = fields.Char(string='S.NO', compute='_compute_sno', store=True, readonly=True)
    organization = fields.Char(string='Organization', required=True)
    designation = fields.Char(string='Designation', required=True)
    from_date = fields.Date(string='From', required=True)
    to_date = fields.Date(string='To', required=True)

    @api.depends('employee_id.employment_details_ids')
    def _compute_sno(self):
        """Compute serial numbers for employment details lines."""
        for employee in self.mapped('employee_id'):
            for index, line in enumerate(employee.employment_details_ids, start=1):
                line.sno = str(index)


class DocumentsDetails(models.Model):
    _name = 'hr.documents.details'
    _description = 'Documents Details'
    
    document = fields.Binary(string="Documents", attachment=True)
    document_type = fields.Selection(
        selection=[
            ('academic_certificates', "Academic Certificates"),
            ('character_certificates', "Character Certificates"),
            ('copy_of_appointment_letter_from_pervious_employeer', "Copy Of Appointment Letter From Previous Employer"),
            ('copy_of_experience_letter_from_pervious_employeer', "Copy Of Experience Letter From Previous Employer"),
            ('copy_of_payslip_form_pervious_employeer', "Copy Of Payslip From Previous Employer"),
            ('copy_of_citizenship', "Copy Of Citizenship"),
            ('copy_of_pan_card', "Copy Of PAN Card"),
            ('copy_of_driving_licence', "Copy Of Driving Licence"),
            ('non_objectives_certificates', "Non Objection Certificate"),
            ('self_declaration_form', "Self Declaration Form"),
            ('passport_size_photograph', "Passport Size Photograph"),
            ('police_report', "Police Report")
        ], required=True
    )    
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade')
    documents_document_id = fields.Many2one('documents.document', string="Linked Document", ondelete='cascade')

    @api.model
    def create(self, vals):
        """ Create a document and link it with hr.documents.details """
        record = super(DocumentsDetails, self).create(vals)
        # print("----------------------------emplyoyee ID create",record.employee_id.name)
        employee_name_folder = record.employee_id.name
        emp_id = record.employee_id.id
        if 'document' in vals and vals['document']:
            file_name = 'Employee_Document.pdf'  # Default name if missing
            mimetype = mimetypes.guess_type(file_name)[0] or 'application/pdf'
            # mimetype = 'pdf'

            # to create a folder search if exist
            folder = self.env['documents.document'].search([('name', '=', employee_name_folder),('type', '=', 'folder')], limit=1)
            if not folder:
                folder = self.env['documents.document'].create({'name':employee_name_folder,'type':'folder'})
                # print('===========================create folder if not exist',folder)

            
            doc_vals = {
                'datas': vals['document'],
                # 'datas_fname': file_name,  # Only pass 'datas_fname' here
                'name': file_name,
                'mimetype': mimetype,
                'res_model':'hr.employee',
                'res_id':record.employee_id.id,
                'folder_id': folder.id,
            }

            document = self.env['documents.document'].create(doc_vals)
            record.documents_document_id = document.id

        return record

    def write(self, vals):
        """ Update document details when editing """
        res = super(DocumentsDetails, self).write(vals)
        # 
        for rec in self:
            # print("----------------------------emplyoyee ID write",rec.employee_id.id)
            if 'document' in vals and vals['document']:
                file_name = 'Updated_Document.pdf'
                mimetype = mimetypes.guess_type(file_name)[0] or 'application/pdf'

                if rec.documents_document_id:
                    rec.documents_document_id.write({
                        'datas': vals['document'],
                        # 'datas_fname': file_name,
                        'name': file_name,
                        'mimetype': mimetype,
                        'res_model':'hr.employee',
                        'res_id':rec.employee_id.id,
                    })
                else:
                    doc_vals = {
                        'datas': vals['document'],
                        # 'datas_fname': file_name,  # Only pass 'datas_fname' for documents.document
                        'name': file_name,
                        'mimetype': mimetype,
                        'res_model':'hr.employee',
                        'res_id':rec.employee_id.id,
                    }
                    document = self.env['documents.document'].create(doc_vals)
                    rec.documents_document_id = document.id

        return res
        
    @api.model
    def unlink(self):
        for rec in self:
            delete_file = rec.documents_document_id.unlink()

        return delete_file



