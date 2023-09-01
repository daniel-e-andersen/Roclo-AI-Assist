node_schema = [
    {
        "label":"Company",
        "main_table":"companies",
        "key_property":{
            "name":"id",
            "col":"id",
            "type":"long",
            "index":"range"
        },
        "properties":{
            "name":{
                "table":"main_table",
                "col":"name",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "country_code":{
                "table":"main_table",
                "col":"country",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "revenue":{
                "table":"main_table",
                "col":"revenue",
                "type":"double",
                "index":"range"
            },
            "ebitda":{
                "table":"main_table",
                "col":"ebitda",
                "type":"double",
                "index":"range"
            },
            # "remote_id":{
            #     "table":"main_table",
            #     "col":"remote_id",
            #     "type":"string",
            #     "index":"text"
            # },
            # "remote_type":{
            #     "table":"main_table",
            #     "col":"remote_type",
            #     "type":"string",
            #     "index":"text"
            # },
            "ownership":{
                "table":"ownerships",
                "match":[
                    [
                        ["companies", "ownership_id"],
                        ["ownerships", "id"]    
                    ]
                ],
                "col":"name",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "website_url":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"website",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "market_capital":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"market_capital",
                "type":"double",
                "index":"range"
            },
            "cash":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"cash",
                "type":"long",
                "index":"range"
            },
            "current_asset":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"current_asset",
                "type":"long",
                "index":"range"
            },
            "enterprise_value":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"enterprise_value",
                "type":"long",
                "index":"range"
            },
            "net_dept":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"net_dept",
                "type":"long",
                "index":"range"
            },
            "profit_before_tax":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"profit_before_tax",
                "type":"long",
                "index":"range"
            },
            "investor_name":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"pe_vc",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "general_net_assets":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"general_net_assets",
                "type":"long",
                "index":"range"
            },
            "tangible_net_assets":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"tangible_net_assets",
                "type":"long",
                "index":"range"
            },
            "house_no":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"company_house_no",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "type":{
                "table":"company_types",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ],
                    [
                        ["company_details", "company_type_id"],
                        ["company_types", "id"]
                    ]
                ],
                "col":"title",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "corporate_status":{
                "table":"corporate_statuses",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ],
                    [
                        ["company_details", "corporate_status_id"],
                        ["corporate_statuses", "id"]
                    ]
                ],
                "col":"title",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            # "source_type":{
            #     "table":"source_types",
            #     "match":[
            #         [
            #             ["companies", "id"],
            #             ["company_details", "company_id"]
            #         ],
            #         [
            #             ["company_details", "source_id"],
            #             ["source_types", "id"]
            #         ]
            #     ],
            #     "col":"title",
            #     "type":"string",
            #     "index":"text",
            #     "full_text_index":True
            # },
            # "trading_status":{
            #     "table":"trading_statuses",
            #     "match":[
            #         [
            #             ["companies", "id"],
            #             ["company_details", "company_id"]
            #         ],
            #         [
            #             ["company_details", "trading_status_id"],
            #             ["trading_statuses", "id"]
            #         ]
            #     ],
            #     "col":"title",
            #     "type":"string",
            #     "index":"text",
            #     "full_text_index":True
            # },
            "current_fund_size":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"current_fund_size",
                "type":"double",
                "index":"range"
            },
            "left_to_deploy":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"left_to_deploy",
                "type":"double",
                "index":"range"
            },
            "max_investment_size":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"max_investment_size",
                "type":"double",
                "index":"range"
            },
            "min_investment_size":{
                "table":"company_details",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ]
                ],
                "col":"min_investment_size",
                "type":"double",
                "index":"range"
            },
            "sub_types":{
                "table":"company_subtypes",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ],
                    [
                        ["company_details", "id"],
                        ["company_details_company_subtypes", "companydetails_id"]
                    ],
                    [
                        ["company_details_company_subtypes", "companysubtypes_id", "list"],
                        ["company_subtypes", "id", "list"]
                    ]
                ],
                "col":"title",
                "type":"string[]",
                "index":"text",
                "full_text_index":True
            },
            "sectors":{
                "table":"sectors",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ],
                    [
                        ["company_details", "id"],
                        ["company_details_sectors", "companydetails_id"]
                    ],
                    [
                        ["company_details_sectors", "sectors_id", "list"],
                        ["sectors", "id", "list"]
                    ]
                ],
                "col":"title",
                "type":"string[]",
                "index":"text",
                "full_text_index":True
            },
            "sub_sectors":{
                "table":"sub_sectors",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_details", "company_id"]
                    ],
                    [
                        ["company_details", "id"],
                        ["company_details_sub_sectors", "companydetails_id"]
                    ],
                    [
                        ["company_details_sub_sectors", "subsectors_id", "list"],
                        ["sub_sectors", "id", "list"]
                    ]
                ],
                "col":"title",
                "type":"string[]",
                "index":"text",
                "full_text_index":True
            },
            "profit_and_loss":{
                "table":"company_financials",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_financials", "company_id"]
                    ]
                ],
                "col":"profit_and_loss",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "balance_sheet":{
                "table":"company_financials",
                "match":[
                    [
                        ["companies", "id"],
                        ["company_financials", "company_id"]
                    ]
                ],
                "col":"balance_sheet",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "descriptions":{
                "table":"descriptions",
                "match":[
                    [
                        ["companies", "id"],
                        ["descriptions", "company_id"]
                    ]
                ],
                "col":"text",
                "type":"string",
                "index":"text",
                "full_text_index":True
            }
        }
    },
    {
        "label":"User",
        "main_table":"user",
        "key_property":{
            "name":"id",
            "col":"id",
            "type":"long",
            "index":"range"
        },
        "properties":{
            "name":{
                "table":"user_profile",
                "match":[
                    [
                        ["user", "id"],
                        ["user_profile", "user_id"]
                    ]
                ],
                "col":"name",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "email":{
                "table":"main_table",
                "col":"email",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "phone_number":{
                "table":"main_table",
                "col":"phone",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "phone_code":{
                "table":"main_table",
                "col":"phone_codes",
                "type":"string",
                "index":"text",
                "full_text_index":False
            }
        }
    },
    {
        "label":"Office",
        "main_table":"office_addresses",
        "key_property":{
            "name":"id",
            "col":"id",
            "type":"long",
            "index":"range"
        },
        "properties":{
            "name":{
                "table":"main_table",
                "col":"branch",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "street_address":{
                "table":"main_table",
                "col":"street_address",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "postcode":{
                "table":"main_table",
                "col":"postcode",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "phone_number":{
                "table":"main_table",
                "col":"phone",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "city":{
                "table":"main_table",
                "col":"city",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "state":{
                "table":"main_table",
                "col":"state",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "country_code":{
                "table":"main_table",
                "col":"country",
                "type":"string",
                "index":"text",
                "full_text_index":False
            }
        }
    },
    {
        "label":"Employee",
        "main_table":"contacts",
        "key_property":{
            "name":"id",
            "col":"id",
            "type":"long",
            "index":"range"
        },
        "properties":{
            "email":{
                "table":"main_table",
                "col":"email",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "name":{
                "table":"main_table",
                "col":"name",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "landline_number":{
                "table":"main_table",
                "col":"direct_phone",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "mobile_number":{
                "table":"main_table",
                "col":"direct_mobile",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            # "title":{
            #     "table":"user_title",
            #     "match":[
            #         [
            #             ["contacts", "title_id"],
            #             ["user_title", "id"]
            #         ]
            #     ],
            #     "col":'title',
            #     "type":"string",
            #     "index":"text",
            #     "full_text_index":False
            # }
        }
    },
    {
        "label":"Shareholder",
        "main_table":"company_shareholders",
        "key_property":{
            "name":"name",
            "col":"name",
            "type":"string",
            "index":"text",
            "full_text_index":True
        },
    },
    {
        "label":"Project",
        "main_table":"projects",
        "key_property":{
            "name":"id",
            "col":"id",
            "type":"long",
            "index":"range"
        },
        "properties":{
            "name":{
                "table":"main_table",
                "col":"name",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "stage":{
                "table":"project_stages",
                "match":[
                    [
                        ["projects", "project_stage_id"],
                        ["project_stages", "id"]
                    ]
                ],
                "col":'name',
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "transaction_type":{
                "table":"transaction_types",
                "match":[
                    [
                        ["projects", "project_type_id"],
                        ["transaction_types", "id"]
                    ]
                ],
                "col":'title',
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "status":{
                "table":"project_status",
                "match":[
                    [
                        ["projects", "status_id"],
                        ["project_status", "id"]
                    ]
                ],
                "col":'title',
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "expected_fee":{
                "table":"main_table",
                "col":'value',
                "type":"double",
                "index":"range"
            },
            "expected_close_date":{
                "table":"main_table",
                "col":'close_date',
                "type":"datetime",
                "index":"range"
            },
            # "hide_buyer_tracker":{
            #     "table":"main_table",
            #     "col":'hide_buyer_tracker',
            #     "type":"boolean"
            # },
            # "hide_company_name":{
            #     "table":"main_table",
            #     "col":'hide_company_name',
            #     "type":"boolean"
            # },
            "start_date":{
                "table":"main_table",
                "col":'engagement_date',
                "type":"datetime",
                "index":"range"
            }
        }
    },
    {
        "label":"Project_comment",
        "main_table":"project_buyer_comments",
        "key_property":{
            "name":"id",
            "col":"id",
            "type":"long",
            "index":"range"
        },
        "properties":{
            "text":{
                "table":"main_table",
                "col":"comment",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            # "hidden_from_others":{
            #     "table":"main_table",
            #     "col":"internal",
            #     "type":"boolean"
            # },
            "created_date":{
                "table":"main_table",
                "col":"created",
                "type":"datetime",
                "index":"range"
            },
        }
    },
    {
        "label":"Opportunity",
        "main_table":"crm_opportunities",
        "key_property":{
            "name":"id",
            "col":"id",
            "type":"long",
            "index":"range"
        },
        "properties":{
            "name":{
                "table":"main_table",
                "col":"title",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            # "pitch_date":{
            #     "table":"main_table",
            #     "col":"pitch_date",
            #     "type":"datetime",
            #     "index":"range"
            # },
            "pipeline":{
                "table":"crm_pipelines",
                "match":[
                    [
                        ["crm_opportunities", "pipeline_id"],
                        ["crm_pipelines", "id"]
                    ]
                ],
                "col":"name",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "pipeline_stage":{
                "table":"crm_pipeline_stages",
                "match":[
                    [
                        ["crm_opportunities", "pipeline_stage_id"],
                        ["crm_pipeline_stages", "id"]
                    ]
                ],
                "col":"name",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "last_activity_date":{
                "table":"main_table",
                "col":"last_activity_date",
                "type":"datetime",
                "index":"range"
            },
            "next_activity_date":{
                "table":"main_table",
                "col":"next_activity_date",
                "type":"datetime",
                "index":"range"
            },
            "is_active":{
                "table":"crm_opportunity_status",
                "match":[
                    [
                        ["crm_opportunities", "opportunity_status_id"],
                        ["crm_opportunity_status", "id"]
                    ]
                ],
                "col":"title",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "expected_exit_date":{
                "table":"main_table",
                "col":"expected_exit_date",
                "type":"datetime",
                "index":"range"
            },
            "lost_reason":{
                "table":"crm_lost_reasons",
                "match":[
                    [
                        ["crm_opportunities", "id"],
                        ["crm_opportuntiny_lost_reasons", "opportunity_id"]
                    ],
                    [
                        ["crm_opportuntiny_lost_reasons", "lost_reason_id"],
                        ["crm_lost_reasons", "id"]
                    ]
                ],
                "col":"reason",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
        }
    },
    {
        "label":"Opportunity_note",
        "main_table":"crm_opportunity_notes",
        "key_property":{
            "name":"id",
            "col":"id",
            "type":"long",
            "index":"range"
        },
        "properties":{
            "text":{
                "table":"main_table",
                "col":"text",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "created_date":{
                "table":"main_table",
                "col":"created",
                "type":"datetime",
                "index":"range"
            },
        }
    },
    {
        "label":"Opportunity_activity",
        "main_table":"crm_opportunity_schedules",
        "key_property":{
            "name":"id",
            "col":"id",
            "type":"long",
            "index":"range"
        },
        "properties":{
            "name":{
                "table":"main_table",
                "col":"name",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "type":{
                "table":"main_table",
                "col":"type",
                "type":"string",
                "index":"text",
                "full_text_index":False
            },
            "text":{
                "table":"main_table",
                "col":"text",
                "type":"string",
                "index":"text",
                "full_text_index":True
            },
            "activity_date":{
                "table":"main_table",
                "col":"from_date",
                "type":"datetime",
                "index":"range"
            },
            "created_date":{
                "table":"main_table",
                "col":"created",
                "type":"datetime",
                "index":"range"
            },
        }
    },
]