from typing import List, Dict, Any, Tuple
import datetime

# Mapping of description types to human-readable labels
description_sections = {
    "os":"Overview and Strategy", 
    "bd_pp":"Business Description (PP Report)", 
    "as_pp":"Acquisition Strategy(PP Report)",
    "so_pb":"Short Overview(Pitchboot)", 
    "lo_pb":"Long Overview(Pitchbook)"
}

# Okalins key types
oaklins_keys_types: List[Tuple[str, type]] = [
    ("deal_id", int),
    ("approval_status", str),
    ("date_closed", datetime.date),
    ("deal_type", str),
    ("fundraising_type", str),
    ("fundraising_rationale", str),
    ("amount_raised", str),
    ("target_name", str),
    ("target_ownership", str),
    ("target_pe_investors", str),
    ("target_business_description", str),
    ("target_website", str),
    ("target_country", str),
    ("target_industry", str),
    ("target_sector", str),
    ("target_turnover", str),
    ("target_ebitda", str),
    ("target_adjusted_ebitda", str),
    ("buyer_name", str),
    ("buyer_ownership", str),
    ("buyer_pe_investors", str),
    ("buyer_business_description", str),
    ("buyer_website", str),
    ("buyer_country", str),
    ("buyer_industry", str),
    ("buyer_sector", str),
    ("buyer_turnover", str),
    ("buyer_ebitda", str),
    ("seller_name", str),
    ("seller_ownership", str),
    ("seller_pe_investors", str),
    ("seller_business_description", str),
    ("seller_website", str),
    ("seller_country", str),
    ("seller_industry", str),
    ("seller_sector", str),
    ("case_study", str),
    ("oaklins_member_firm", str),
    ("oaklins_main_contact", str),
    ("oaklins_main_contact_email", str),
    ("oaklins_other_members_involved", str),
    ("sector_commentary", str)
]

# Postgres Table Scehma
postgres_table_schema = {
    "table_name": "oaklins_deals",
    "creation_sql": """
        CREATE TABLE oaklins_deals (
            deal_id SERIAL PRIMARY KEY,
            approval_status TEXT NOT NULL,
            date_closed DATE,
            deal_type TEXT,
            fundraising_type TEXT,
            fundraising_rationale TEXT,
            amount_raised TEXT,
            target_name TEXT,
            target_ownership TEXT,
            target_pe_investors TEXT,
            target_business_description TEXT,
            target_website TEXT,
            target_country TEXT,
            target_industry TEXT,
            target_sector TEXT,
            target_turnover TEXT,
            target_ebitda TEXT,
            target_adjusted_ebitda TEXT,
            buyer_name TEXT,
            buyer_ownership TEXT,
            buyer_pe_investors TEXT,
            buyer_business_description TEXT,
            buyer_website TEXT,
            buyer_country TEXT,
            buyer_industry TEXT,
            buyer_sector TEXT,
            buyer_turnover TEXT,
            buyer_ebitda TEXT,
            seller_name TEXT,
            seller_ownership TEXT,
            seller_pe_investors TEXT,
            seller_business_description TEXT,
            seller_website TEXT,
            seller_country TEXT,
            seller_industry TEXT,
            seller_sector TEXT,
            case_study TEXT,
            oaklins_member_firm TEXT,
            oaklins_main_contact TEXT,
            oaklins_main_contact_email TEXT,
            oaklins_other_members_involved TEXT,
            sector_commentary TEXT
        );
    """,
    "index_sql": """
        CREATE INDEX IF NOT EXISTS idx_deal_id ON oaklins_deals(deal_id);
        CREATE INDEX IF NOT EXISTS idx_target_desc ON oaklins_deals(target_business_description);
        CREATE INDEX IF NOT EXISTS idx_buyer_desc ON oaklins_deals(buyer_business_description);
        CREATE INDEX IF NOT EXISTS idx_seller_desc ON oaklins_deals(seller_business_description);
    """
}