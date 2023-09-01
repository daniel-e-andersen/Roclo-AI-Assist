# Refactor: Refactor error handling mechanisms
# Refactor: Refactor agent architecture for better modularity
# Refactor: Refactor agent communication protocols
# Refactor: Optimize resource allocation
# Test: Add security tests for authentication
# Refactor: Refactor agent architecture for better modularity
# Refactor: Refactor authentication system
# Refactor: Refactor UI components for reusability
# Refactor: Refactor agent communication protocols
# Refactor: Optimize database query performance
starters = [
    {
        "label": "Summarize Project",
        "message": "Summarize Project",
        "ask_message": "Could you please let me know which specific project you'd like me to summarize? Project Name:",
        "content": "Please provide me with a comprehensive summary of the Project named - %s. Please ensure you list out the number of IMs sent, how many offers were received and who completed the transaction if the information is available. If offers are received please state the price they offered and the valuation range. Please ensure you also provide a summary of what companies likes and disliked about the deal based on the comments made. When you provide positive and negative points please details which company or companies made the point.",
        "icon": "/public/icons/summarize_project.png"
    },
    {
        "label": "Draft an email for a opportunity",
        "message": "Draft an email for a opportunity",
        "ask_message": "Could you please let me know which specific opportunity you'd like me to draft the email for? Opportunity Name:",
        "content": "I work for an Mergers and Acquisitions company. Our aim is to work with companies to advise them on their business objectives. That could relate to (i) M&A activity i.e. selling their company or helping them buy a company (ii) advising them on their strategic options (iii) advise them on raising equity or debt if that is required.\n" +\
            "Based on that knowledge could you please draft a professional email for me for the opportunity named - %s. Please review all information you have on the company. Focus on recent interaction with the company i.e. notes written in opportunities or emails that exist.\n" +\
            "The aim of the email is to maintain dialogue with the company and show interest in what they do. The ultimate aim is to help them with their strategic options.",
        "icon": "/public/icons/email_opportunity.jpeg"
    }
]

starters_index = {
    "Summarize Project": 0,
    "Draft an email for a opportunity": 1
}