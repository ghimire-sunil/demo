from odoo import api, fields, models



class HrEmployee(models.Model):
    _inherit='hr.employee'

    street = fields.Char()
    
    private_country_id = fields.Many2one('res.country',default=lambda self: self._get_default_country())
    province_id = fields.Many2one('res.province', 'Province')
    district_id = fields.Many2one(comodel_name ='res.district', string='Districts')
    municipality_id = fields.Many2one('res.municipality', string = 'Municipality')
    ward = fields.Char()
    ward_id = fields.Many2one('res.ward', string = 'Ward')


# def_country= env['res.country'].search([('name','=','Nepal')]).id
    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('name', '=', 'Nepal')], limit=1)
        return country.id if country else False
  

    @api.onchange('province_id')
    def onchange_province_id(self):
        if self.province_id:
            self.district_id = False
            self.municipality_id = False
            self.ward = False
    
    @api.onchange('district_id')
    def onchange_district_id(self):
        if self.district_id:
            self.municipality_id = False
            self.ward = False


    @api.onchange('municipality_id')
    def onchange_municipality_id(self):
        if self.municipality_id:
            self.ward = False
    

class District(models.Model):
    _name = "res.district"

    name = fields.Char(string='District Name', required=True)
    country_id =  fields.Many2one('res.country',"Country",default=lambda self: self._get_default_country())
    province_id = fields.Many2one('res.province', 'Province')
    municipality_ids = fields.One2many(comodel_name="res.municipality",inverse_name="district_id",string="Municipality")

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('name', '=', 'Nepal')], limit=1)
        return country.id if country else False
    

class Province(models.Model):
    _name = 'res.province'
    
    name = fields.Char(string='Province Name', required=True)
    country_id =  fields.Many2one('res.country',"Country",default=lambda self: self._get_default_country())
    district_ids = fields.One2many(comodel_name="res.district", inverse_name='province_id', string="Districts")

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('name', '=', 'Nepal')], limit=1)
        return country.id if country else False

class Municipality(models.Model):
    _name = 'res.municipality'
    
    name = fields.Char(string='Municipality Name', required=True)
    country_id =  fields.Many2one('res.country',"Country",default=lambda self: self._get_default_country())
    district_id = fields.Many2one('res.district', "District")
    ward_ids = fields.One2many(comodel_name="res.ward", inverse_name="municipality_id",string="Ward")

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('name', '=', 'Nepal')], limit=1)
        return country.id if country else False

class Ward(models.Model):
    _name = 'res.ward'

    name = fields.Char(string='Ward Name', required=True)
    country_id =  fields.Many2one('res.country',"Country",default=lambda self: self._get_default_country())
    municipality_id = fields.Many2one('res.municipality', string = 'Municipality')
    

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('name', '=', 'Nepal')], limit=1)
        return country.id if country else False


class Ward(models.Model):
    _name = 'res.ward'
    
    name = fields.Char(string='Ward No', required=True)
    country_id =  fields.Many2one('res.country',"Country",default=lambda self: self._get_default_country())
    district_id = fields.Many2one('res.district', "District")
    municipality_id = fields.Many2one('res.municipality', "Municipality")

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('name', '=', 'Nepal')], limit=1)
        return country.id if country else False
    

    