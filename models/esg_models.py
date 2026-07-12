from odoo import models, fields, api
from datetime import date

class EsgDepartment(models.Model):
    _name = 'esg.department'
    _description = 'ESG Department'
   
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    head_id = fields.Many2one('hr.employee', string='Head')
    parent_id = fields.Many2one('esg.department', string='Parent Department')
    employee_count = fields.Integer(string='Employee Count')
    status = fields.Selection([
        ('active', 'Active'), 
        ('inactive', 'Inactive')
    ], string='Status', default='active')

class EsgCategory(models.Model):
    _name = 'esg.category'
    _description = 'ESG Category'

    name = fields.Char(string='Name', required=True)
    type = fields.Selection([
        ('csr', 'CSR Activity'), 
        ('challenge', 'Challenge')
    ], string='Type', required=True)
    status = fields.Selection([
        ('active', 'Active'), 
        ('inactive', 'Inactive')
    ], string='Status', default='active')

class EsgEmissionFactor(models.Model):
    _name = 'esg.emission.factor'
    _description = 'Emission Factor'

    name = fields.Char(string='Name', required=True)
    value = fields.Float(string='Carbon Value')

class EsgProductProfile(models.Model):
    _name = 'esg.product.profile'
    _description = 'Product ESG Profile'

    name = fields.Char(string='Name', required=True)
    esg_score = fields.Float(string='ESG Score')

class EsgGoal(models.Model):
    _name = 'esg.goal'
    _description = 'Environmental Goal'

    name = fields.Char(string='Name', required=True)
    department_id = fields.Many2one('esg.department', string='Department')
    target_co2 = fields.Float(string='Target CO2')
    current_co2 = fields.Float(string='Current CO2')
    progress = fields.Float(string='Progress', compute='_compute_progress')
    deadline = fields.Date(string='Deadline')
    status = fields.Selection([
        ('active', 'Active'), 
        ('on_track', 'On Track'), 
        ('completed', 'Completed')
    ], string='Status')

    @api.depends('target_co2', 'current_co2')
    def _compute_progress(self):
        for record in self:
            if record.target_co2 > 0:
                record.progress = (record.current_co2 / record.target_co2) * 100
            else:
                record.progress = 0

class EsgPolicy(models.Model):
    _name = 'esg.policy'
    _description = 'ESG Policy'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

class EsgBadge(models.Model):
    _name = 'esg.badge'
    _description = 'ESG Badge'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    unlock_rule = fields.Char(string='Unlock Rule')
    icon = fields.Binary(string='Icon')

class EsgReward(models.Model):
    _name = 'esg.reward'
    _description = 'ESG Reward Catalog'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    points_required = fields.Integer(string='Points Required')
    stock = fields.Integer(string='Stock')
    status = fields.Selection([
        ('available', 'Available'), 
        ('out_of_stock', 'Out of Stock')
    ], string='Status', default='available')

class EsgCarbonTransaction(models.Model):
    _name = 'esg.carbon.transaction'
    _description = 'Carbon Transaction'

    name = fields.Char(string='Reference', required=True)
    department_id = fields.Many2one('esg.department', string='Department')
    source_type = fields.Char(string='Source Type')
    calculated_emission = fields.Float(string='Calculated Emission')
    transaction_date = fields.Date(string='Transaction Date', default=fields.Date.context_today)

class EsgCsrActivity(models.Model):
    _name = 'esg.csr.activity'
    _description = 'CSR Activity'

    name = fields.Char(string='Activity Name', required=True)
    category_id = fields.Many2one('esg.category', string='Category')
    description = fields.Text(string='Description')
    status = fields.Selection([
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed')
    ], string='Status', default='planned')

class EsgCsrParticipation(models.Model):
    _name = 'esg.csr.participation'
    _description = 'CSR Employee Participation'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    activity_id = fields.Many2one('esg.csr.activity', string='Activity', required=True)
    proof = fields.Binary(string='Proof of Participation')
    points_earned = fields.Integer(string='Points Earned')
    completion_date = fields.Date(string='Completion Date')
    approval_status = fields.Selection([
        ('pending', 'Pending'), 
        ('approved', 'Approved'), 
        ('rejected', 'Rejected')
    ], string='Approval Status', default='pending')

class EsgChallenge(models.Model):
    _name = 'esg.challenge'
    _description = 'ESG Challenge'

    name = fields.Char(string='Title', required=True)
    category_id = fields.Many2one('esg.category', string='Category')
    description = fields.Text(string='Description')
    xp = fields.Integer(string='XP Awarded')
    difficulty = fields.Selection([
        ('easy', 'Easy'), 
        ('medium', 'Medium'), 
        ('hard', 'Hard')
    ], string='Difficulty')
    evidence_required = fields.Boolean(string='Evidence Required')
    deadline = fields.Date(string='Deadline')
    status = fields.Selection([
        ('draft', 'Draft'), 
        ('active', 'Active'), 
        ('under_review', 'Under Review'),
        ('completed', 'Completed'),
        ('archived', 'Archived')
    ], string='Status', default='draft')

class EsgChallengeParticipation(models.Model):
    _name = 'esg.challenge.participation'
    _description = 'Challenge Participation'

    challenge_id = fields.Many2one('esg.challenge', string='Challenge', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    progress = fields.Float(string='Progress')
    proof = fields.Binary(string='Proof')
    approval = fields.Selection([
        ('pending', 'Pending'), 
        ('approved', 'Approved'), 
        ('rejected', 'Rejected')
    ], string='Approval', default='pending')
    xp_awarded = fields.Integer(string='XP Awarded')

class EsgPolicyAck(models.Model):
    _name = 'esg.policy.ack'
    _description = 'Policy Acknowledgement'

    policy_id = fields.Many2one('esg.policy', string='Policy', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)

class EsgAudit(models.Model):
    _name = 'esg.audit'
    _description = 'Governance Audit'

    name = fields.Char(string='Title', required=True)
    department_id = fields.Many2one('esg.department', string='Department')
    auditor_id = fields.Many2one('res.users', string='Auditor')
    date = fields.Date(string='Date')
    findings = fields.Text(string='Findings')
    status = fields.Selection([
        ('open', 'Open'), 
        ('under_review', 'Under Review'),
        ('completed', 'Completed')
    ], string='Status', default='open')

class EsgComplianceIssue(models.Model):
    _name = 'esg.compliance.issue'
    _description = 'Compliance Issue'

    name = fields.Char(string='Issue', required=True)
    audit_id = fields.Many2one('esg.audit', string='Audit')
    severity = fields.Selection([
        ('low', 'Low'), 
        ('medium', 'Medium'), 
        ('high', 'High')
    ], string='Severity')
    description = fields.Text(string='Description')
    owner_id = fields.Many2one('res.users', string='Owner')
    due_date = fields.Date(string='Due Date')
    status = fields.Selection([
        ('open', 'Open'), 
        ('resolved', 'Resolved')
    ], string='Status', default='open')
    
    is_overdue = fields.Boolean(string='Is Overdue', compute='_compute_is_overdue')

    @api.depends('due_date', 'status')
    def _compute_is_overdue(self):
        for record in self:
            if record.due_date and record.status == 'open' and record.due_date < date.today():
                record.is_overdue = True
            else:
                record.is_overdue = False

class EsgDepartmentScore(models.Model):
    _name = 'esg.department.score'
    _description = 'Department ESG Score'

    department_id = fields.Many2one('esg.department', string='Department', required=True)
    env_score = fields.Float(string='Environmental Score')
    social_score = fields.Float(string='Social Score')
    gov_score = fields.Float(string='Governance Score')
    total_score = fields.Float(string='Total Score')
