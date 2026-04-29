from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HotelGuestRegistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'Guest Registration'

    state = fields.Selection([
        ('DRAFT', 'Draft'),
        ('RESERVED', 'Reserved'),
        ('CHECKEDIN', 'Checked In'),
        ('CHECKEDOUT', 'Checked Out'),
        ('CANCELLED', 'Cancelled'),
    ], string='Status', default='DRAFT')

    actualpax = fields.Integer('Actual PAX')
    details = fields.Text('Details')

    room_id = fields.Many2one('hotel.rooms', string='Room', index=True)
    roomtypename = fields.Char('Room Type', related='room_id.roomtype_id.name', store=False)
    guest_id = fields.Many2one('hotel.guests', string='Guest', index=True)
    datefromsched = fields.Datetime(string='Check In Date')
    datetosched = fields.Datetime(string='Check Out Date')
    grc_id = fields.Integer(string='GRC #')

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )

    name = fields.Char('Guest Registration', compute='_compute_name', store=False)

    @api.depends('room_id', 'guest_id')
    def _compute_name(self):
        for rec in self:
            room_name = rec.room_id.name if rec.room_id else ''
            guest_name = rec.guest_id.name if rec.guest_id else ''
            rec.name = f'{room_name}, {guest_name}'

    create_date_ampm = fields.Char(
        string='Created ON',
        compute='_compute_create_date_ampm',
        store=False,
    )

    def _format_user_datetime(self, value):
        if not value:
            return ''
        dt_local = fields.Datetime.context_timestamp(self, value)
        return dt_local.strftime('%m-%d-%Y %I:%M %p')

    @api.depends('create_date')
    def _compute_create_date_ampm(self):
        for rec in self:
            rec.create_date_ampm = rec._format_user_datetime(rec.create_date)

    datefromsched_ampm = fields.Char(
        string='Check In Date',
        compute='_compute_datefromsched_ampm',
        store=False,
    )

    @api.depends('datefromsched')
    def _compute_datefromsched_ampm(self):
        for rec in self:
            rec.datefromsched_ampm = rec._format_user_datetime(rec.datefromsched)

    datetosched_ampm = fields.Char(
        string='Check Out Date',
        compute='_compute_datetosched_ampm',
        store=False,
    )

    @api.depends('datetosched')
    def _compute_datetosched_ampm(self):
        for rec in self:
            rec.datetosched_ampm = rec._format_user_datetime(rec.datetosched)

    grc_id_display = fields.Char(
        string='GRC #',
        compute='_compute_grc_id_display',
        store=False,
    )

    @api.depends('grc_id')
    def _compute_grc_id_display(self):
        for rec in self:
            rec.grc_id_display = str(rec.grc_id) if rec.grc_id else ''

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('grc_id'):
                doctype = 'GRC'
                cmp_id = self.env.company.id
                self.env.cr.execute(
                    'SELECT * FROM public.hotel_fnGetDocno(%s,%s)',
                    (cmp_id, doctype),
                )
                result = self.env.cr.fetchone()
                vals['grc_id'] = result[0] if result else 1

        return super().create(vals_list)

        
    def action_reserve(self):
        for rec in self:
            if not rec.guest_id:
                raise ValidationError('Please supply a valid Guest Name.')
            elif not rec.room_id:
                raise ValidationError('Please supply a valid Room Number.')
            elif not rec.datefromsched:
                raise ValidationError('Please supply a valid Date from Schedule.')
            elif not rec.datetosched:
                raise ValidationError('Please supply a valid Date To Schedule.')
            elif rec.datetosched <=rec.datefromsched:
                raise ValidationError('Invalid Date Range.')
            else:
                rec.state = "RESERVED"
        

    def action_checkin(self):
        for rec in self:
            if not rec.guest_id:
                raise ValidationError('Please supply a valid Guest Name.')
            elif not rec.room_id:
                raise ValidationError('Please supply a valid Room Number.')
            elif not rec.datefromsched:
                raise ValidationError('Please supply a valid Date from Schedule.')
            elif not rec.datetosched:
                raise ValidationError('Please supply a valid Date To Schedule.')
            elif rec.datetosched <=rec.datefromsched:
                raise ValidationError('Invalid Date Range.')
            else:

                rec.state = "CHECKEDIN"

    def action_checkout(self):
        for rec in self:
            if(rec.state == "CHECKEDIN"):
                rec.state = "CHECKEDOUT"
            else:
                raise ValidationError('Guest is not CHECKED IN.')

    def action_cancel(self):
        for rec in self:
            if(rec.state == "CHECKEDIN"):
                raise ValidationError('Guest has already CHECKED IN.')
            else:
                rec.state = "CANCELLED"

    def action_mark_draft(self):
        for rec in self:
            rec.state = "DRAFT"       
                    
