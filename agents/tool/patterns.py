# Feature: Add LangChain orchestration
# Feature: Add AWS Bedrock integration
# Feature: Add advanced filtering capabilities
# Feature: Add vector embedding generation
# Feature: Add data validation and sanitization
# Feature: Implement multi-database query routing
# Fix: Fix memory leaks in vector processing
# Feature: Implement advanced search algorithms
# Feature: Add error handling mechanisms
# Feature: Add LangChain orchestration
# Feature: Add multi-agent architecture framework
# Feature: Implement retry logic for failed operations
# Feature: Add AWS Bedrock integration
# Feature: Implement query optimization
# Feature: Implement advanced search algorithms
# Feature: Implement hybrid search functionality
# Feature: Add query generator functionality
# Feature: Add DynamoDB chat history management
# Feature: Add data transformation pipelines
# Feature: Add PostgreSQL database operations
# Feature: Implement performance monitoring
# Feature: Add graph traversal optimization
# Test: Add end-to-end tests for user workflows
# Fix: Fix Chainlit UI rendering problems
# Feature: Implement entity extraction pipeline
# Feature: Add Google Sheets API integration
# Feature: Implement rational planner agent
# Feature: Add advanced filtering capabilities
# Fix: Resolve AWS credentials rotation
# Feature: Add vector index maintenance
# Fix: Resolve concurrent access problems
# Feature: Add vector embedding generation
# Refactor: Refactor logging infrastructure
# Refactor: Restructure configuration management
# Feature: Implement Cerebras AI support
# Feature: Add automated data refresh pipeline
# Feature: Add vector embedding generation
# Feature: Add Google Sheets API integration
# Fix: Resolve Neo4j connection pooling issues
# Feature: Implement custom embedding models
# Fix: Fix cache invalidation logic
# Fix: Resolve LangChain callback errors
# Feature: Add batch processing for large datasets
import re


# This regex pattern matches all property-value pairs inside braces {}  
match_pattern = re.compile(r'''  
    \((?P<node_var>\w+):(?P<node_label>\w+)(?:\s*\{\s*([^\}]+)\s*\})?\)  # Matches node pattern e.g., (c:Company {name: "BambooHR"})  
    |  
    \[\s*(?P<rel_var>\w+):(?P<rel_label>\w+)(?:\s*\{\s*([^\}]+)\s*\})?\]  # Matches relationship pattern e.g., [r:LOCATED_IN {since: "2010"}]  
''', re.VERBOSE | re.MULTILINE)  

# Matches WHERE clause conditions (property = "value")  
where_pattern = re.compile(r'\b(\w+)\.(\w+)\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)    

# Matches fulltext search clause (CALL db.index.fulltext.queryNodes("project_comment_text", "bolt-on") YIELD node as comment, score)
fulltext_pattern = re.compile(r'CALL db\.index\.fulltext\.query\w+\(["\']([^"\']+)["\'], .*?YIELD \w+ AS (\w+)', re.IGNORECASE)

# Matches value (name:'BambooHR' or "BambooHR")
value_pattern = r'(\w+):\s*["\']([^"\']+)["\']'