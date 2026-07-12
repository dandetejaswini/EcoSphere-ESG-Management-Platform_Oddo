# EcoSphere: ESG Management Platform

EcoSphere is a comprehensive Odoo ERP module designed to integrate Environmental, Social, and Governance (ESG) metrics directly into day-to-day business operations. It transforms manual sustainability tracking into an automated, gamified, and highly visible workflow.

## Business Value
Modern organizations require actionable insights, not just raw data. EcoSphere bridges the gap between operational execution and corporate sustainability goals by automating carbon accounting, enforcing compliance, and driving employee engagement.

## Core Capabilities
* Automates carbon footprint tracking directly from purchasing and manufacturing operations.
* Manages Corporate Social Responsibility (CSR) activities with mandatory evidence workflows.
* Drives employee engagement through gamified sustainability challenges and reward redemptions.
* Tracks governance policies, compliance issues, and overdue audits in real-time.
* Calculates dynamic, weighted ESG scores across organizational departments.

## Technical Architecture
Built as a modular Odoo application, EcoSphere utilizes a dual data model structure:
* **Master Data:** Departments, Emission Factors, Goals, Policies, Categories, Badges, and Rewards.
* **Transactional Data:** Carbon Transactions, CSR Activity, Challenge Participations, and Compliance Audits.

## Installation Instructions
1. Download or clone this repository into your Odoo `addons` directory.
2. Restart the Odoo server service to load the new file paths.
3. Access your Odoo instance and enable **Developer Mode** in Settings.
4. Navigate to the **Apps** menu and click **Update Apps List**.
5. Clear the default search filter, search for `EcoSphere`, and click **Activate**.

## Operational Workflows
* **Carbon Automation:** When enabled, linking an emission factor to an operational transaction automatically calculates the resulting carbon output.
* **Gamification Engine:** Employees earn XP by participating in approved CSR activities and sustainability challenges.
* **Badge Auto-Awarding:** The system continuously monitors employee XP and challenge completion metrics, automatically distributing milestone badges.
* **Compliance Enforcement:** Governance issues are tracked by owner and due date, with overdue items automatically flagged for review. 

## Contributors
* Dande Tejaswini (Team Lead)
* Parvez Sharief (Team Member)