from odoo import models, fields, api, exceptions

class EsgDepartment(models.Model):
    _name = 'esg.department'
    _description = 'Department Master Data'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    head_id = fields.Many2one('hr.employee')
    parent_id = fields.Many2one('esg.department')
    employee_count = fields.Integer()
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='active')

class EsgCategory(models.Model):
    _name = 'esg.category'
    _description = 'Shared Category'

    name = fields.Char(required=True)
    type = fields.Selection([('csr', 'CSR Activity'), ('challenge', 'Challenge')], required=True)
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='active')

class EsgEmissionFactor(models.Model):
    _name = 'esg.emission.factor'
    _description = 'Emission Factor'

    name = fields.Char(required=True)
    factor_value = fields.Float(required=True)

class EsgProductProfile(models.Model):
    _name = 'esg.product.profile'
    _description = 'Product ESG Profile'

    name = fields.Char(required=True)
    product_id = fields.Many2one('product.product')
    carbon_footprint = fields.Float()

class EsgEnvironmentalGoal(models.Model):
    _name = 'esg.environmental.goal'
    _description = 'Sustainability Targets'

    name = fields.Char(required=True)
    target_value = fields.Float()
    current_value = fields.Float()
    deadline = fields.Date()

class EsgPolicy(models.Model):
    _name = 'esg.policy'
    _description = 'Governance Policies'

    name = fields.Char(required=True)
    content = fields.Text()
    effective_date = fields.Date()

class EsgBadge(models.Model):
    _name = 'esg.badge'
    _description = 'Employee Achievements'

    name = fields.Char(required=True)
    description = fields.Text()
    unlock_rule = fields.Selection([('xp', 'XP Based'), ('challenges', 'Challenge Count Based')], required=True)
    required_value = fields.Integer(required=True)
    icon = fields.Binary()

class EsgReward(models.Model):
    _name = 'esg.reward'
    _description = 'Redeemable Incentives'

    name = fields.Char(required=True)
    description = fields.Text()
    points_required = fields.Integer(required=True)
    stock_status = fields.Selection([('in_stock', 'In Stock'), ('out_of_stock', 'Out of Stock')], default='in_stock')
    stock_qty = fields.Integer(default=10)

class EsgCarbonTransaction(models.Model):
    _name = 'esg.carbon.transaction'
    _description = 'Carbon Transaction'

    name = fields.Char(required=True)
    emission_factor_id = fields.Many2one('esg.emission.factor')
    calculated_emission = fields.Float()
    transaction_date = fields.Date(default=fields.Date.context_today)
    source_type = fields.Selection([('purchase', 'Purchase'), ('manufacturing', 'Manufacturing'), ('expense', 'Expense'), ('fleet', 'Fleet')])
    source_amount = fields.Float()

    @api.onchange('emission_factor_id', 'source_amount')
    def _onchange_calculate_emission(self):
        if self.emission_factor_id and self.source_amount:
            self.calculated_emission = self.source_amount * self.emission_factor_id.factor_value

class EsgCsrActivity(models.Model):
    _name = 'esg.csr.activity'
    _description = 'CSR Activity'

    name = fields.Char(required=True)
    category_id = fields.Many2one('esg.category', domain=[('type', '=', 'csr')])
    description = fields.Text()
    points_awarded = fields.Integer(default=10)

class EsgEmployeeParticipation(models.Model):
    _name = 'esg.employee.participation'
    _description = 'Employee Participation'

    employee_id = fields.Many2one('hr.employee', required=True)
    activity_id = fields.Many2one('esg.csr.activity', required=True)
    proof = fields.Binary()
    approval_status = fields.Selection([('draft', 'Draft'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='draft')
    points_earned = fields.Integer()
    completion_date = fields.Date()

    def action_approve(self):
        param = self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.evidence_requirement')
        for record in self:
            if param and not record.proof:
                raise exceptions.UserError('Approval requires an attached proof file.')
            record.approval_status = 'approved'
            record.points_earned = record.activity_id.points_awarded
            record.employee_id.esg_xp_balance += record.points_earned
            record.employee_id._check_badge_auto_award()

class EsgChallenge(models.Model):
    _name = 'esg.challenge'
    _description = 'Sustainability Challenge'

    title = fields.Char(required=True)
    category_id = fields.Many2one('esg.category', domain=[('type', '=', 'challenge')])
    description = fields.Text()
    xp = fields.Integer(default=20)
    difficulty = fields.Selection([('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    evidence_required = fields.Boolean()
    deadline = fields.Date()
    status = fields.Selection([
        ('draft', 'Draft'), 
        ('active', 'Active'), 
        ('under_review', 'Under Review'), 
        ('completed', 'Completed'), 
        ('archived', 'Archived')
    ], default='draft')

class EsgChallengeParticipation(models.Model):
    _name = 'esg.challenge.participation'
    _description = 'Challenge Participation'

    challenge_id = fields.Many2one('esg.challenge', required=True)
    employee_id = fields.Many2one('hr.employee', required=True)
    progress = fields.Float()
    proof = fields.Binary()
    approval = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='draft')
    xp_awarded = fields.Integer()

    def action_approve(self):
        for record in self:
            record.approval = 'approved'
            record.xp_awarded = record.challenge_id.xp
            record.employee_id.esg_xp_balance += record.xp_awarded
            record.employee_id.completed_challenges_count += 1
            record.employee_id._check_badge_auto_award()

class EsgPolicyAcknowledgement(models.Model):
    _name = 'esg.policy.acknowledgement'
    _description = 'Policy Acknowledgement'

    policy_id = fields.Many2one('esg.policy', required=True)
    employee_id = fields.Many2one('hr.employee', required=True)
    acknowledged = fields.Boolean(default=False)
    acknowledgement_date = fields.Date()

class EsgAudit(models.Model):
    _name = 'esg.audit'
    _description = 'Governance Audits'

    name = fields.Char(required=True)
    audit_date = fields.Date()
    auditor = fields.Char()
    result = fields.Text()

class EsgComplianceIssue(models.Model):
    _name = 'esg.compliance.issue'
    _description = 'Compliance Issue'

    name = fields.Char(required=True)
    audit_id = fields.Many2one('esg.audit')
    severity = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    description = fields.Text()
    owner_id = fields.Many2one('hr.employee', required=True)
    due_date = fields.Date(required=True)
    status = fields.Selection([('open', 'Open'), ('closed', 'Closed')], default='open')
    is_overdue = fields.Boolean(compute='_compute_is_overdue', store=True)

    @api.depends('due_date', 'status')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.status == 'open' and record.due_date and record.due_date < today:
                record.is_overdue = True
            else:
                record.is_overdue = False

class EsgDepartmentScore(models.Model):
    _name = 'esg.department.score'
    _description = 'Department Score'

    department_id = fields.Many2one('esg.department', required=True)
    environmental_score = fields.Float()
    social_score = fields.Float()
    governance_score = fields.Float()
    total_score = fields.Float(compute='_compute_total_score', store=True)

    @api.depends('environmental_score', 'social_score', 'governance_score')
    def _compute_total_score(self):
        for record in self:
            record.total_score = (
                (record.environmental_score * 0.40) + 
                (record.social_score * 0.30) + 
                (record.governance_score * 0.30)
            )

class EsgRewardRedemption(models.Model):
    _name = 'esg.reward.redemption'
    _description = 'Reward Redemption'

    employee_id = fields.Many2one('hr.employee', required=True)
    reward_id = fields.Many2one('esg.reward', required=True)
    redemption_date = fields.Date(default=fields.Date.context_today)

    @api.model
    def create(self, vals):
        reward = self.env['esg.reward'].browse(vals['reward_id'])
        employee = self.env['hr.employee'].browse(vals['employee_id'])
        if reward.stock_status == 'out_of_stock' or reward.stock_qty <= 0:
            raise exceptions.UserError('This reward is out of stock.')
        if employee.esg_xp_balance < reward.points_required:
            raise exceptions.UserError('Insufficient XP/Points balance to redeem this reward.')
        employee.esg_xp_balance -= reward.points_required
        reward.stock_qty -= 1
        if reward.stock_qty == 0:
            reward.stock_status = 'out_of_stock'
        return super(EsgRewardRedemption, self).create(vals)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    esg_xp_balance = fields.Integer(default=0)
    completed_challenges_count = fields.Integer(default=0)
    badge_ids = fields.Many2many('esg.badge', string='Badges')

    def _check_badge_auto_award(self):
        param = self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.badge_auto_award')
        if not param:
            return
        badges = self.env['esg.badge'].search([])
        for employee in self:
            for badge in badges:
                if badge in employee.badge_ids:
                    continue
                if badge.unlock_rule == 'xp' and employee.esg_xp_balance >= badge.required_value:
                    employee.badge_ids = [(4, badge.id)]
                elif badge.unlock_rule == 'challenges' and employee.completed_challenges_count >= badge.required_value:
                    employee.badge_ids = [(4, badge.id)]