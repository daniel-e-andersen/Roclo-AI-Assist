# Tables used to construct Knowledge graph from SQL database.

related_tables = [
    ["companies", "id"], # Main table of Company Node.
    ["company_details", "company_id"], # Connected to companies table.
    ["company_details_company_subtypes", "companydetails_id"], # Connected to company_details table. Grouping required.
    ["company_details_sectors", "companydetails_id"], # Connected to company_details table. Grouping required.
    ["company_details_sub_sectors", "companydetails_id"], # Connected to company_details table. Grouping required.
    ["company_financials", "company_id"], # Connected to companies table. Grouping by company_id is required.
    ["company_shareholders", "id"], # Main table of Shareholder node. 
    ["company_subtypes", "id"], # Referenced by company_details table.
    ["company_types", "id"], # Referenced by company_details table.
    ["contacts", "id"], # Main table of Employee node.
    ["contacts_users", "id"], # Used for HAS_RELATIONSHIP relation. 
    ["corporate_statuses", "id"], # Referenced by company_details table.
    ["crm_lost_reasons", "id"], # Referenced by crm_opportuntiny_lost_reasons table.
    ["crm_opportunities", "id"], # Main table of Opportunity node.
    ["crm_opportunities_contacts", "id"], # Used for HAS_CONTACT relation.
    ["crm_opportunities_internal_introducers", "id"], # Used for INTRODUCES relation.
    ["crm_opportunities_team_members", "id"], # Used for HAS_TEAM_MEMBER relation.
    ["crm_opportunity_notes", "id"], # Used for WRITE_NOTE relation. 
    ["crm_opportunity_schedules", "id"], # Used for ACTIVITY relation.
    ["crm_opportunity_status", "id"], # Referenced by crm_oppotunities table.
    ["crm_opportuntiny_lost_reasons", "opportunity_id"], # Connected to crm_opportunities table. Delete Uniques are crucial.
    ["crm_pipeline_stages", "id"], # Referenced by crm_opportunities table.
    ["crm_pipelines", "id"], # Referenced by crm_opportunities table.
    ["descriptions", "company_id"], # Connected to companies table. Grouping after extract vector due to chunk for each section.
    ["office_addresses", "id"], # Main table of the Office node.
    ["ownerships","id"], # Referenced by companies table.
    ["project_buyer_categories", "id"], # Referenced by project_buyers table.
    ["project_buyer_comments", "id"], # Connected to project_buyers table.
    ["project_buyer_stages", "id"], # Referenced by project_buyers table.
    ["project_buyer_ranks", "id"], # Referenced by project_buyers table.
    ["project_buyers", "id"], # Main table for BUY_PROJECT relation.
    ["project_stages", "id"], # Referenced by projects table.
    ["project_status", "id"], # Referenced by projects table.
    ["projects", "id"], # Main table for Project node.
    ["projects_introducers", "id"], # Main table for INTRODUCES relation.
    ["projects_team_members", "id"], # Main table for HAS_TEAM_MEMBER relation.
    ["sectors", "id"], # Referenced by company_details table.
    ["source_types", "id"], # Referenced by company_details table.
    ["sub_sectors", "id"], # Referenced by company_details table.
    ["trading_statuses", "id"], # Referenced by company_details table.
    ["transaction_types", "id"], # Referenced by projects table.
    ["user", "id"], # Main table of User node.
    ["user_title", "id"], # Referenced by contacts table.
    ["user_profile", "user_id"] # Referenced by user table.
]