# Roclo AI Bot

A sophisticated AI-powered chatbot system built for Oaklins, featuring multi-agent architecture, knowledge graph integration, and advanced data retrieval capabilities.

## 🚀 Overview

Roclo AI Bot is an enterprise-grade conversational AI system that combines multiple AI agents to provide intelligent responses by querying various data sources including knowledge graphs, vector databases, and traditional databases. The system uses a multi-agent workflow to plan, retrieve, and augment responses based on user queries.

## 🏗️ Architecture

The system follows a multi-agent architecture with the following key components:

### Core Agents
- **Rational Planner**: Analyzes user queries and determines the optimal approach
- **Query Generator**: Creates appropriate database queries based on the plan
- **Data Retriever**: Executes queries against various data sources
- **Result Augmenter**: Enhances retrieved data with additional context
- **Plain Augmenter**: Provides direct responses for simple queries
- **Table Augmenter**: Formats tabular data for better presentation
- **Prioritizer**: Manages and prioritizes multiple data sources

### Data Sources
- **Neo4j Knowledge Graph**: Stores entity relationships and semantic data
- **Milvus Vector Database**: Handles vector embeddings for semantic search
- **PostgreSQL**: Traditional relational database operations
- **Supabase**: User authentication and additional data storage
- **DynamoDB**: Chat history and session management

## 🛠️ Technology Stack

- **Framework**: Python with LangChain and LangGraph
- **UI**: Chainlit for conversational interface
- **Databases**: 
  - Neo4j (Knowledge Graph)
  - Milvus (Vector Database)
  - PostgreSQL (Relational Data)
  - Supabase (Authentication)
  - DynamoDB (Chat History)
- **AI/ML**: 
  - LangChain for AI orchestration
  - Opik for experiment tracking
  - Various LLM integrations (AWS Bedrock, Cerebras, etc.)
- **Infrastructure**: 
  - Docker Compose for local development
  - AWS services integration
  - Google Sheets API integration

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- AWS CLI configured
- Neo4j database
- Access to required AI model APIs

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd roclo_ai_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Configure AWS credentials for Secrets Manager
   - Set up database connection strings
   - Configure AI model API keys

4. **Start supporting services**
   ```bash
   docker-compose up -d
   ```

5. **Initialize databases**
   ```bash
   python kg_constructor.py  # Set up knowledge graph
   python milvus_constructor.py  # Initialize vector database
   python postgres_constructor.py  # Set up PostgreSQL
   ```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
./run.sh
```
or
```bash
chainlit run app.py -h --host 0.0.0.0 --port 8001
```

### Production Mode
Configure your production environment and run:
```bash
python app.py
```

## 🔧 Configuration

### AWS Secrets Manager
The application uses AWS Secrets Manager for credential management. Ensure your secrets are stored under:
```
roclo_chatbot/main_credentials
```

### Database Configuration
- **Neo4j**: Configure connection details in `core/graph_database.py`
- **Milvus**: Set up vector database parameters in `core/milvus_vector.py`
- **PostgreSQL**: Configure connection in `core/postgres_database.py`
- **Supabase**: Set up authentication in `core/supabase_database.py`

## 📊 Features

### Multi-Agent Workflow
- Intelligent query planning and routing
- Dynamic data source selection
- Context-aware response generation
- Error handling and retry mechanisms

### Knowledge Graph Integration
- Entity extraction and relationship mapping
- Semantic search capabilities
- Graph-based query optimization
- Real-time knowledge graph updates

### Vector Search
- Semantic similarity search
- Document embedding and retrieval
- Hybrid search combining vector and traditional methods

### User Management
- Secure authentication system
- Session management
- User activity tracking
- Role-based access control

### Monitoring and Tracking
- Opik integration for experiment tracking
- Comprehensive logging system
- Performance monitoring
- User feedback collection

## 🔄 Data Pipeline

### Knowledge Graph Population
```bash
python kg_population/kg_populator.py
```

### Vector Index Updates
```bash
python kg_population/vector_indexer.py
```

### Data Refresh
```bash
python refresher.py
```

## 📝 API Usage

The system provides a conversational interface through Chainlit. Users can:

1. **Ask Questions**: Natural language queries about business data
2. **Get Insights**: AI-powered analysis of complex datasets
3. **Explore Relationships**: Navigate through knowledge graph connections
4. **Access Reports**: Generate formatted reports from multiple data sources

## 🧪 Testing

Run test queries:
```bash
python -c "from test_query import *; run_test()"
```

## 📁 Project Structure

```
roclo_ai_bot/
├── agents/                 # AI agent implementations
│   ├── augmenter/         # Response augmentation agents
│   ├── planner/           # Query planning agents
│   ├── prioritizer/       # Data prioritization
│   ├── query/             # Query generation
│   ├── retriever/         # Data retrieval
│   └── tool/              # Utility tools
├── build/                 # Agent chain builders
├── core/                  # Core system components
├── kg_population/         # Knowledge graph management
├── public/                # Static assets
├── utils/                 # Utility functions
├── app.py                 # Main application
├── chain.py               # Agent workflow orchestration
├── config.py              # Configuration management
└── requirements.txt       # Dependencies
```

## 🔒 Security

- AWS Secrets Manager for credential management
- User authentication through Supabase
- Session-based security
- Input validation and sanitization
- Secure database connections

## 📈 Monitoring

The system includes comprehensive monitoring through:
- Opik experiment tracking
- Structured logging
- Performance metrics
- User interaction analytics
- Error tracking and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For support and questions:
- Check the logs in the application
- Review the configuration settings
- Contact the development team

## 🔄 Updates

The system includes automatic data refresh capabilities:
- Scheduled knowledge graph updates
- Vector index maintenance
- Database synchronization
- Model performance monitoring

---

**Note**: This system is designed for enterprise use and requires proper configuration of all external services and credentials before deployment.

<!-- Update changelog -->

<!-- Update contributing guidelines -->

<!-- Add monitoring and logging guide -->

<!-- Update configuration guide -->

<!-- Add deployment guide -->

<!-- Update configuration guide -->

<!-- Update configuration guide -->

<!-- Add performance tuning guide -->

<!-- Add API documentation -->

<!-- Update security guidelines -->

<!-- Implement load tests for concurrent users -->

<!-- Update contributing guidelines -->

<!-- Update security guidelines -->

<!-- Add API documentation -->

<!-- Add API documentation -->

<!-- Update README with installation instructions -->

<!-- Add monitoring and logging guide -->

<!-- Update configuration guide -->

<!-- Update configuration guide -->

<!-- Implement integration tests for database operations -->

<!-- Add troubleshooting section -->

<!-- Add deployment guide -->

<!-- Add security tests for authentication -->

<!-- Implement integration tests for database operations -->

<!-- Update database schema documentation -->

<!-- Update architecture documentation -->

<!-- Update FAQ section -->

<!-- Update security guidelines -->

<!-- Add code examples and tutorials -->

<!-- Update README with installation instructions -->

<!-- Update changelog -->

<!-- Update FAQ section -->

<!-- Update architecture documentation -->

<!-- Add code examples and tutorials -->

<!-- Add deployment guide -->

<!-- Restructure configuration management -->

<!-- Add troubleshooting section -->

<!-- Restructure project directory layout -->

<!-- Add API documentation -->

<!-- Add troubleshooting section -->

<!-- Refactor UI components for reusability -->

<!-- Refactor UI components for reusability -->

<!-- Update architecture documentation -->

<!-- Update architecture documentation -->

<!-- Restructure configuration management -->

<!-- Update README with installation instructions -->

<!-- Add deployment guide -->

<!-- Restructure database connection management -->

<!-- Add code examples and tutorials -->

<!-- Add monitoring and logging guide -->

<!-- Implement mock tests for external services -->

<!-- Update README with installation instructions -->

<!-- Update FAQ section -->

<!-- Refactor agent communication protocols -->

<!-- Add code examples and tutorials -->

<!-- Update FAQ section -->

<!-- Refactor UI components for reusability -->

<!-- Add performance tuning guide -->

<!-- Add monitoring and logging guide -->

<!-- Optimize caching strategies -->

<!-- Update database schema documentation -->

<!-- Add API documentation -->

<!-- Update configuration guide -->

<!-- Update README with installation instructions -->

<!-- Restructure test frameworks -->

<!-- Add code examples and tutorials -->

<!-- Update configuration guide -->

<!-- Add code examples and tutorials -->

<!-- Restructure data processing pipeline -->

<!-- Update security guidelines -->

<!-- Update architecture documentation -->

<!-- Update architecture documentation -->

<!-- Add security tests for authentication -->

<!-- Add performance tuning guide -->

<!-- Add regression tests for critical paths -->

<!-- Refactor logging infrastructure -->

<!-- Add code examples and tutorials -->

<!-- Add code examples and tutorials -->

<!-- Restructure data processing pipeline -->

<!-- Refactor UI components for reusability -->

<!-- Optimize caching strategies -->

<!-- Update FAQ section -->

<!-- Update database schema documentation -->

<!-- Update configuration guide -->

<!-- Update README with installation instructions -->

<!-- Add advanced performance metrics -->

<!-- Implement intelligent health monitoring -->

<!-- Implement advanced search optimization -->

<!-- Implement advanced workflow automation -->

<!-- Implement intelligent resource allocation -->

<!-- Implement advanced authentication flows -->

<!-- Add intelligent data validation -->

<!-- Add intelligent query routing -->

<!-- Implement advanced memory management -->

<!-- Implement intelligent failover mechanisms -->

<!-- Update documentation formatting -->

<!-- Fix minor UI inconsistencies -->

<!-- Optimize database queries -->

<!-- Update dependency versions -->

<!-- Fix logging configuration -->

<!-- Update API documentation -->

<!-- Improve error messages -->

<!-- Update configuration examples -->

<!-- Fix minor security issues -->

<!-- Update deployment scripts -->

<!-- Improve code comments -->

<!-- Update testing framework -->

<!-- Add table augmenter for data formatting -->

<!-- Implement data retriever agent -->

<!-- Implement data retriever agent -->

<!-- Add multi-agent architecture framework -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Implement plain augmenter for simple queries -->

<!-- Update configuration guide -->

<!-- Add result augmenter capabilities -->

<!-- Add multi-agent architecture framework -->

<!-- Add API documentation -->

<!-- Restructure database connection management -->

<!-- Resolve query generation edge cases -->

<!-- Add AWS Bedrock integration -->

<!-- Implement data retriever agent -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add result augmenter capabilities -->

<!-- Update README with installation instructions -->

<!-- Fix Milvus index corruption -->

<!-- Add AWS Bedrock integration -->

<!-- Fix Milvus index corruption -->

<!-- Update dependencies to latest versions -->

<!-- Bump Python version requirements -->

<!-- Implement Opik experiment tracking -->

<!-- Add API documentation -->

<!-- Update Docker base images -->

<!-- Implement plain augmenter for simple queries -->

<!-- Update dependencies to latest versions -->

<!-- Add DynamoDB chat history management -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add result augmenter capabilities -->

<!-- Add Google Sheets API integration -->

<!-- Fix authentication flow issues -->

<!-- Resolve query generation edge cases -->

<!-- Refactor agent architecture for better modularity -->

<!-- Implement Chainlit UI interface -->

<!-- Implement rational planner agent -->

<!-- Implement Opik experiment tracking -->

<!-- Add DynamoDB chat history management -->

<!-- Implement prioritizer for data sources -->

<!-- Implement Milvus vector database support -->

<!-- Implement rational planner agent -->

<!-- Resolve query generation edge cases -->

<!-- Implement rational planner agent -->

<!-- Implement Supabase authentication -->

<!-- Add LangChain orchestration -->

<!-- Add AWS Bedrock integration -->

<!-- Add DynamoDB chat history management -->

<!-- Implement Opik experiment tracking -->

<!-- Update Docker base images -->

<!-- Add query generator functionality -->

<!-- Implement Milvus vector database support -->

<!-- Implement Milvus vector database support -->

<!-- Add troubleshooting section -->

<!-- Implement Milvus vector database support -->

<!-- Fix authentication flow issues -->

<!-- Implement Chainlit UI interface -->

<!-- Add API documentation -->

<!-- Fix memory leaks in vector processing -->

<!-- Refresh security certificates -->

<!-- Fix memory leaks in vector processing -->

<!-- Update README with installation instructions -->

<!-- Add query generator functionality -->

<!-- Optimize vector search algorithms -->

<!-- Bump Python version requirements -->

<!-- Add API documentation -->

<!-- Implement Supabase authentication -->

<!-- Implement prioritizer for data sources -->

<!-- Implement entity extraction pipeline -->

<!-- Implement prioritizer for data sources -->

<!-- Implement Opik experiment tracking -->

<!-- Refactor agent architecture for better modularity -->

<!-- Implement Chainlit UI interface -->

<!-- Update dependencies to latest versions -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Fix session management bugs -->

<!-- Fix session management bugs -->

<!-- Implement rational planner agent -->

<!-- Fix session management bugs -->

<!-- Implement plain augmenter for simple queries -->

<!-- Update Docker base images -->

<!-- Implement Opik experiment tracking -->

<!-- Add result augmenter capabilities -->

<!-- Implement Milvus vector database support -->

<!-- Implement plain augmenter for simple queries -->

<!-- Implement rational planner agent -->

<!-- Add AWS Bedrock integration -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add LangChain orchestration -->

<!-- Resolve query generation edge cases -->

<!-- Refactor agent architecture for better modularity -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Resolve database connection timeouts -->

<!-- Refactor query generation logic -->

<!-- Refactor query generation logic -->

<!-- Add result augmenter capabilities -->

<!-- Fix authentication flow issues -->

<!-- Resolve database connection timeouts -->

<!-- Implement rational planner agent -->

<!-- Update dependencies to latest versions -->

<!-- Add troubleshooting section -->

<!-- Update README with installation instructions -->

<!-- Implement data retriever agent -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Add multi-agent architecture framework -->

<!-- Add Google Sheets API integration -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Update Docker base images -->

<!-- Implement entity extraction pipeline -->

<!-- Add Google Sheets API integration -->

<!-- Add AWS Bedrock integration -->

<!-- Restructure database connection management -->

<!-- Implement prioritizer for data sources -->

<!-- Implement Cerebras AI support -->

<!-- Update README with installation instructions -->

<!-- Add table augmenter for data formatting -->

<!-- Refresh security certificates -->

<!-- Implement Chainlit UI interface -->

<!-- Refactor query generation logic -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Implement prioritizer for data sources -->

<!-- Add DynamoDB chat history management -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Implement Supabase authentication -->

<!-- Update dependencies to latest versions -->

<!-- Fix Milvus index corruption -->

<!-- Update configuration guide -->

<!-- Implement prioritizer for data sources -->

<!-- Implement entity extraction pipeline -->

<!-- Add Google Sheets API integration -->

<!-- Fix authentication flow issues -->

<!-- Fix session management bugs -->

<!-- Update dependencies to latest versions -->

<!-- Add Google Sheets API integration -->

<!-- Add table augmenter for data formatting -->

<!-- Add table augmenter for data formatting -->

<!-- Implement Supabase authentication -->

<!-- Implement plain augmenter for simple queries -->

<!-- Update Docker base images -->

<!-- Add query generator functionality -->

<!-- Add troubleshooting section -->

<!-- Update Docker base images -->

<!-- Implement Milvus vector database support -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Refactor agent architecture for better modularity -->

<!-- Resolve query generation edge cases -->

<!-- Fix Milvus index corruption -->

<!-- Implement prioritizer for data sources -->

<!-- Add AWS Bedrock integration -->

<!-- Implement Cerebras AI support -->

<!-- Implement Opik experiment tracking -->

<!-- Implement entity extraction pipeline -->

<!-- Bump Python version requirements -->

<!-- Implement Supabase authentication -->

<!-- Refactor agent architecture for better modularity -->

<!-- Add DynamoDB chat history management -->

<!-- Bump Python version requirements -->

<!-- Add result augmenter capabilities -->

<!-- Add query generator functionality -->

<!-- Update README with installation instructions -->

<!-- Add query generator functionality -->

<!-- Add API documentation -->

<!-- Add PostgreSQL database operations -->

<!-- Implement Milvus vector database support -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Add query generator functionality -->

<!-- Resolve database connection timeouts -->

<!-- Fix memory leaks in vector processing -->

<!-- Bump Python version requirements -->

<!-- Fix Milvus index corruption -->

<!-- Restructure database connection management -->

<!-- Add API documentation -->

<!-- Refactor query generation logic -->

<!-- Add result augmenter capabilities -->

<!-- Restructure database connection management -->

<!-- Refactor agent architecture for better modularity -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Resolve query generation edge cases -->

<!-- Implement Chainlit UI interface -->

<!-- Add table augmenter for data formatting -->

<!-- Update README with installation instructions -->

<!-- Add table augmenter for data formatting -->

<!-- Add DynamoDB chat history management -->

<!-- Fix Milvus index corruption -->

<!-- Implement Chainlit UI interface -->

<!-- Update configuration guide -->

<!-- Implement plain augmenter for simple queries -->

<!-- Fix Milvus index corruption -->

<!-- Implement Milvus vector database support -->

<!-- Implement data retriever agent -->

<!-- Update dependencies to latest versions -->

<!-- Resolve query generation edge cases -->

<!-- Fix authentication flow issues -->

<!-- Refresh security certificates -->

<!-- Refactor agent architecture for better modularity -->

<!-- Add troubleshooting section -->

<!-- Add AWS Bedrock integration -->

<!-- Add PostgreSQL database operations -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Implement entity extraction pipeline -->

<!-- Add multi-agent architecture framework -->

<!-- Add query generator functionality -->

<!-- Update README with installation instructions -->

<!-- Add result augmenter capabilities -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Refactor agent architecture for better modularity -->

<!-- Add multi-agent architecture framework -->

<!-- Implement Chainlit UI interface -->

<!-- Fix session management bugs -->

<!-- Optimize vector search algorithms -->

<!-- Implement data retriever agent -->

<!-- Implement prioritizer for data sources -->

<!-- Restructure database connection management -->

<!-- Add query generator functionality -->

<!-- Resolve database connection timeouts -->

<!-- Implement Opik experiment tracking -->

<!-- Add AWS Bedrock integration -->

<!-- Refactor agent architecture for better modularity -->

<!-- Implement data retriever agent -->

<!-- Implement Supabase authentication -->

<!-- Implement rational planner agent -->

<!-- Implement Cerebras AI support -->

<!-- Add troubleshooting section -->

<!-- Implement Milvus vector database support -->

<!-- Implement Cerebras AI support -->

<!-- Add result augmenter capabilities -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add multi-agent architecture framework -->

<!-- Implement prioritizer for data sources -->

<!-- Refactor query generation logic -->

<!-- Implement rational planner agent -->

<!-- Add API documentation -->

<!-- Update dependencies to latest versions -->

<!-- Add DynamoDB chat history management -->

<!-- Refactor query generation logic -->

<!-- Add troubleshooting section -->

<!-- Fix Milvus index corruption -->

<!-- Implement entity extraction pipeline -->

<!-- Update configuration guide -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Implement Supabase authentication -->

<!-- Resolve database connection timeouts -->

<!-- Update dependencies to latest versions -->

<!-- Fix memory leaks in vector processing -->

<!-- Add query generator functionality -->

<!-- Resolve query generation edge cases -->

<!-- Implement Supabase authentication -->

<!-- Update configuration guide -->

<!-- Restructure database connection management -->

<!-- Add LangChain orchestration -->

<!-- Fix session management bugs -->

<!-- Implement entity extraction pipeline -->

<!-- Add result augmenter capabilities -->

<!-- Add multi-agent architecture framework -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Bump Python version requirements -->

<!-- Implement data retriever agent -->

<!-- Implement rational planner agent -->

<!-- Implement data retriever agent -->

<!-- Resolve database connection timeouts -->

<!-- Implement Milvus vector database support -->

<!-- Refresh security certificates -->

<!-- Update configuration guide -->

<!-- Implement Supabase authentication -->

<!-- Implement Supabase authentication -->

<!-- Add LangChain orchestration -->

<!-- Add DynamoDB chat history management -->

<!-- Implement prioritizer for data sources -->

<!-- Add DynamoDB chat history management -->

<!-- Implement Opik experiment tracking -->

<!-- Resolve database connection timeouts -->

<!-- Refresh security certificates -->

<!-- Add PostgreSQL database operations -->

<!-- Add PostgreSQL database operations -->

<!-- Implement prioritizer for data sources -->

<!-- Add result augmenter capabilities -->

<!-- Add query generator functionality -->

<!-- Update dependencies to latest versions -->

<!-- Resolve database connection timeouts -->

<!-- Refresh security certificates -->

<!-- Add result augmenter capabilities -->

<!-- Fix authentication flow issues -->

<!-- Add LangChain orchestration -->

<!-- Implement Milvus vector database support -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Add LangChain orchestration -->

<!-- Implement Cerebras AI support -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Fix authentication flow issues -->

<!-- Update README with installation instructions -->

<!-- Fix memory leaks in vector processing -->

<!-- Update configuration guide -->

<!-- Update Docker base images -->

<!-- Fix Milvus index corruption -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add table augmenter for data formatting -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Update dependencies to latest versions -->

<!-- Add query generator functionality -->

<!-- Add PostgreSQL database operations -->

<!-- Implement entity extraction pipeline -->

<!-- Add API documentation -->

<!-- Update README with installation instructions -->

<!-- Restructure database connection management -->

<!-- Implement Cerebras AI support -->

<!-- Update Docker base images -->

<!-- Implement Opik experiment tracking -->

<!-- Fix authentication flow issues -->

<!-- Fix session management bugs -->

<!-- Implement rational planner agent -->

<!-- Add table augmenter for data formatting -->

<!-- Fix Milvus index corruption -->

<!-- Refactor agent architecture for better modularity -->

<!-- Fix memory leaks in vector processing -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Implement Milvus vector database support -->

<!-- Add Google Sheets API integration -->

<!-- Update configuration guide -->

<!-- Add result augmenter capabilities -->

<!-- Refactor query generation logic -->

<!-- Add AWS Bedrock integration -->

<!-- Implement Supabase authentication -->

<!-- Resolve database connection timeouts -->

<!-- Implement Milvus vector database support -->

<!-- Add PostgreSQL database operations -->

<!-- Implement rational planner agent -->

<!-- Implement plain augmenter for simple queries -->

<!-- Implement data retriever agent -->

<!-- Implement rational planner agent -->

<!-- Implement Cerebras AI support -->

<!-- Restructure database connection management -->

<!-- Bump Python version requirements -->

<!-- Fix Milvus index corruption -->

<!-- Implement prioritizer for data sources -->

<!-- Implement entity extraction pipeline -->

<!-- Add API documentation -->

<!-- Add PostgreSQL database operations -->

<!-- Fix memory leaks in vector processing -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add table augmenter for data formatting -->

<!-- Fix session management bugs -->

<!-- Fix authentication flow issues -->

<!-- Fix memory leaks in vector processing -->

<!-- Add query generator functionality -->

<!-- Fix memory leaks in vector processing -->

<!-- Implement Supabase authentication -->

<!-- Implement rational planner agent -->

<!-- Add Google Sheets API integration -->

<!-- Update README with installation instructions -->

<!-- Add LangChain orchestration -->

<!-- Fix session management bugs -->

<!-- Add multi-agent architecture framework -->

<!-- Restructure database connection management -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Update configuration guide -->

<!-- Implement Cerebras AI support -->

<!-- Implement rational planner agent -->

<!-- Optimize vector search algorithms -->

<!-- Add troubleshooting section -->

<!-- Implement data retriever agent -->

<!-- Add LangChain orchestration -->

<!-- Refactor query generation logic -->

<!-- Add multi-agent architecture framework -->

<!-- Implement Chainlit UI interface -->

<!-- Implement prioritizer for data sources -->

<!-- Implement data retriever agent -->

<!-- Optimize vector search algorithms -->

<!-- Implement data retriever agent -->

<!-- Optimize vector search algorithms -->

<!-- Add DynamoDB chat history management -->

<!-- Implement Chainlit UI interface -->

<!-- Add query generator functionality -->

<!-- Add result augmenter capabilities -->

<!-- Add table augmenter for data formatting -->

<!-- Implement data retriever agent -->

<!-- Implement entity extraction pipeline -->

<!-- Add PostgreSQL database operations -->

<!-- Optimize vector search algorithms -->

<!-- Implement Chainlit UI interface -->

<!-- Add table augmenter for data formatting -->

<!-- Add DynamoDB chat history management -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Optimize vector search algorithms -->

<!-- Fix memory leaks in vector processing -->

<!-- Resolve database connection timeouts -->

<!-- Add PostgreSQL database operations -->

<!-- Restructure database connection management -->

<!-- Update configuration guide -->

<!-- Refactor agent architecture for better modularity -->

<!-- Implement entity extraction pipeline -->

<!-- Fix authentication flow issues -->

<!-- Add DynamoDB chat history management -->

<!-- Implement Supabase authentication -->

<!-- Implement data retriever agent -->

<!-- Optimize vector search algorithms -->

<!-- Restructure database connection management -->

<!-- Restructure database connection management -->

<!-- Implement Milvus vector database support -->

<!-- Add DynamoDB chat history management -->

<!-- Fix session management bugs -->

<!-- Add DynamoDB chat history management -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Add query generator functionality -->

<!-- Update Docker base images -->

<!-- Refresh security certificates -->

<!-- Add API documentation -->

<!-- Optimize vector search algorithms -->

<!-- Implement Supabase authentication -->

<!-- Resolve database connection timeouts -->

<!-- Add query generator functionality -->

<!-- Implement rational planner agent -->

<!-- Resolve database connection timeouts -->

<!-- Implement entity extraction pipeline -->

<!-- Fix session management bugs -->

<!-- Add result augmenter capabilities -->

<!-- Implement plain augmenter for simple queries -->

<!-- Update Docker base images -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Refresh security certificates -->

<!-- Add API documentation -->

<!-- Fix authentication flow issues -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add AWS Bedrock integration -->

<!-- Add multi-agent architecture framework -->

<!-- Fix memory leaks in vector processing -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add PostgreSQL database operations -->

<!-- Update configuration guide -->

<!-- Add Google Sheets API integration -->

<!-- Add AWS Bedrock integration -->

<!-- Implement Supabase authentication -->

<!-- Update dependencies to latest versions -->

<!-- Fix authentication flow issues -->

<!-- Add AWS Bedrock integration -->

<!-- Add troubleshooting section -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add Google Sheets API integration -->

<!-- Update configuration guide -->

<!-- Add LangChain orchestration -->

<!-- Update configuration guide -->

<!-- Fix Milvus index corruption -->

<!-- Fix memory leaks in vector processing -->

<!-- Refresh security certificates -->

<!-- Resolve database connection timeouts -->

<!-- Refresh security certificates -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Update README with installation instructions -->

<!-- Bump Python version requirements -->

<!-- Add troubleshooting section -->

<!-- Implement Chainlit UI interface -->

<!-- Implement Opik experiment tracking -->

<!-- Implement entity extraction pipeline -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add table augmenter for data formatting -->

<!-- Add multi-agent architecture framework -->

<!-- Add query generator functionality -->

<!-- Implement Chainlit UI interface -->

<!-- Implement Cerebras AI support -->

<!-- Add result augmenter capabilities -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add LangChain orchestration -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Implement prioritizer for data sources -->

<!-- Add multi-agent architecture framework -->

<!-- Implement data retriever agent -->

<!-- Add API documentation -->

<!-- Add table augmenter for data formatting -->

<!-- Refactor query generation logic -->

<!-- Resolve query generation edge cases -->

<!-- Update README with installation instructions -->

<!-- Add AWS Bedrock integration -->

<!-- Resolve query generation edge cases -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add AWS Bedrock integration -->

<!-- Resolve query generation edge cases -->

<!-- Implement prioritizer for data sources -->

<!-- Add DynamoDB chat history management -->

<!-- Add Google Sheets API integration -->

<!-- Implement Cerebras AI support -->

<!-- Implement plain augmenter for simple queries -->

<!-- Resolve database connection timeouts -->

<!-- Add LangChain orchestration -->

<!-- Bump Python version requirements -->

<!-- Fix session management bugs -->

<!-- Add PostgreSQL database operations -->

<!-- Implement Opik experiment tracking -->

<!-- Implement Supabase authentication -->

<!-- Implement data retriever agent -->

<!-- Refactor query generation logic -->

<!-- Implement data retriever agent -->

<!-- Refactor query generation logic -->

<!-- Update configuration guide -->

<!-- Add table augmenter for data formatting -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add result augmenter capabilities -->

<!-- Update Docker base images -->

<!-- Implement Cerebras AI support -->

<!-- Implement Cerebras AI support -->

<!-- Add table augmenter for data formatting -->

<!-- Implement entity extraction pipeline -->

<!-- Implement Milvus vector database support -->

<!-- Implement Chainlit UI interface -->

<!-- Add multi-agent architecture framework -->

<!-- Add troubleshooting section -->

<!-- Optimize vector search algorithms -->

<!-- Add PostgreSQL database operations -->

<!-- Add DynamoDB chat history management -->

<!-- Add troubleshooting section -->

<!-- Add PostgreSQL database operations -->

<!-- Add AWS Bedrock integration -->

<!-- Implement Opik experiment tracking -->

<!-- Refresh security certificates -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add PostgreSQL database operations -->

<!-- Fix session management bugs -->

<!-- Implement prioritizer for data sources -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add LangChain orchestration -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add Google Sheets API integration -->

<!-- Fix authentication flow issues -->

<!-- Add query generator functionality -->

<!-- Fix memory leaks in vector processing -->

<!-- Optimize vector search algorithms -->

<!-- Refactor agent architecture for better modularity -->

<!-- Add API documentation -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Update README with installation instructions -->

<!-- Implement entity extraction pipeline -->

<!-- Optimize vector search algorithms -->

<!-- Fix memory leaks in vector processing -->

<!-- Add table augmenter for data formatting -->

<!-- Add LangChain orchestration -->

<!-- Implement Opik experiment tracking -->

<!-- Implement plain augmenter for simple queries -->

<!-- Resolve query generation edge cases -->

<!-- Add result augmenter capabilities -->

<!-- Implement entity extraction pipeline -->

<!-- Refactor agent architecture for better modularity -->

<!-- Bump Python version requirements -->

<!-- Implement rational planner agent -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add query generator functionality -->

<!-- Implement Chainlit UI interface -->

<!-- Implement Cerebras AI support -->

<!-- Implement rational planner agent -->

<!-- Restructure database connection management -->

<!-- Add Google Sheets API integration -->

<!-- Fix session management bugs -->

<!-- Update Docker base images -->

<!-- Implement Chainlit UI interface -->

<!-- Resolve database connection timeouts -->

<!-- Fix authentication flow issues -->

<!-- Implement Chainlit UI interface -->

<!-- Refactor query generation logic -->

<!-- Add API documentation -->

<!-- Implement Opik experiment tracking -->

<!-- Add LangChain orchestration -->

<!-- Implement Cerebras AI support -->

<!-- Implement rational planner agent -->

<!-- Implement Opik experiment tracking -->

<!-- Add multi-agent architecture framework -->

<!-- Fix Milvus index corruption -->

<!-- Update README with installation instructions -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add multi-agent architecture framework -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Implement prioritizer for data sources -->

<!-- Fix memory leaks in vector processing -->

<!-- Implement plain augmenter for simple queries -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Fix authentication flow issues -->

<!-- Refactor query generation logic -->

<!-- Implement Milvus vector database support -->

<!-- Add PostgreSQL database operations -->

<!-- Implement Milvus vector database support -->

<!-- Add troubleshooting section -->

<!-- Fix Milvus index corruption -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add LangChain orchestration -->

<!-- Add API documentation -->

<!-- Add Google Sheets API integration -->

<!-- Add AWS Bedrock integration -->

<!-- Implement Cerebras AI support -->

<!-- Implement Cerebras AI support -->

<!-- Add LangChain orchestration -->

<!-- Add multi-agent architecture framework -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add troubleshooting section -->

<!-- Bump Python version requirements -->

<!-- Add Google Sheets API integration -->

<!-- Fix session management bugs -->

<!-- Bump Python version requirements -->

<!-- Resolve query generation edge cases -->

<!-- Fix Milvus index corruption -->

<!-- Add troubleshooting section -->

<!-- Add multi-agent architecture framework -->

<!-- Add PostgreSQL database operations -->

<!-- Add table augmenter for data formatting -->

<!-- Add Google Sheets API integration -->

<!-- Update README with installation instructions -->

<!-- Add multi-agent architecture framework -->

<!-- Add Google Sheets API integration -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Implement Opik experiment tracking -->

<!-- Resolve query generation edge cases -->

<!-- Resolve query generation edge cases -->

<!-- Restructure database connection management -->

<!-- Fix memory leaks in vector processing -->

<!-- Update dependencies to latest versions -->

<!-- Add troubleshooting section -->

<!-- Update README with installation instructions -->

<!-- Bump Python version requirements -->

<!-- Add Google Sheets API integration -->

<!-- Implement Milvus vector database support -->

<!-- Add DynamoDB chat history management -->

<!-- Add troubleshooting section -->

<!-- Fix memory leaks in vector processing -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Update README with installation instructions -->

<!-- Implement Supabase authentication -->

<!-- Implement Supabase authentication -->

<!-- Implement Chainlit UI interface -->

<!-- Implement entity extraction pipeline -->

<!-- Add advanced error recovery -->

<!-- Add API documentation -->

<!-- Optimize vector database performance -->

<!-- Add LangChain orchestration -->

<!-- Implement rational planner agent -->

<!-- Add DynamoDB chat history management -->

<!-- Fix session management bugs -->

<!-- Resolve query generation edge cases -->

<!-- Implement Chainlit UI interface -->

<!-- Update configuration guide -->

<!-- Implement Chainlit UI interface -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Fix Milvus index corruption -->

<!-- Add LangChain orchestration -->

<!-- Resolve database connection timeouts -->

<!-- Restructure database connection management -->

<!-- Add table augmenter for data formatting -->

<!-- Add query generator functionality -->

<!-- Fix session management bugs -->

<!-- Refresh security certificates -->

<!-- Add LangChain orchestration -->

<!-- Restructure database connection management -->

<!-- Add PostgreSQL database operations -->

<!-- Add advanced error recovery -->

<!-- Implement advanced security protocols -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Update Docker base images -->

<!-- Fix authentication flow issues -->

<!-- Implement advanced security protocols -->

<!-- Add query generator functionality -->

<!-- Add PostgreSQL database operations -->

<!-- Update dependencies to latest versions -->

<!-- Implement Opik experiment tracking -->

<!-- Implement advanced AI orchestration -->

<!-- Implement plain augmenter for simple queries -->

<!-- Fix Milvus index corruption -->

<!-- Implement data retriever agent -->

<!-- Bump Python version requirements -->

<!-- Add Google Sheets API integration -->

<!-- Resolve query generation edge cases -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Implement intelligent caching -->

<!-- Update README with installation instructions -->

<!-- Bump Python version requirements -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add DynamoDB chat history management -->

<!-- Implement entity extraction pipeline -->

<!-- Add multi-agent architecture framework -->

<!-- Implement rational planner agent -->

<!-- Implement dynamic load balancing -->

<!-- Fix Milvus index corruption -->

<!-- Restructure database connection management -->

<!-- Refresh security certificates -->

<!-- Add Google Sheets API integration -->

<!-- Fix memory leaks in vector processing -->

<!-- Implement Chainlit UI interface -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Fix Milvus index corruption -->

<!-- Implement entity extraction pipeline -->

<!-- Fix memory leaks in vector processing -->

<!-- Implement Supabase authentication -->

<!-- Fix authentication flow issues -->

<!-- Resolve database connection timeouts -->

<!-- Add table augmenter for data formatting -->

<!-- Resolve query generation edge cases -->

<!-- Add LangChain orchestration -->

<!-- Implement prioritizer for data sources -->

<!-- Implement Chainlit UI interface -->

<!-- Implement entity extraction pipeline -->

<!-- Add table augmenter for data formatting -->

<!-- Implement rational planner agent -->

<!-- Fix memory leaks in vector processing -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Implement advanced AI orchestration -->

<!-- Add advanced error recovery -->

<!-- Add troubleshooting section -->

<!-- Add table augmenter for data formatting -->

<!-- Update configuration guide -->

<!-- Implement data retriever agent -->

<!-- Update README with installation instructions -->

<!-- Implement Opik experiment tracking -->

<!-- Implement data retriever agent -->

<!-- Fix session management bugs -->

<!-- Resolve query generation edge cases -->

<!-- Implement Chainlit UI interface -->

<!-- Add multi-agent architecture framework -->

<!-- Implement Cerebras AI support -->

<!-- Add comprehensive monitoring -->

<!-- Update configuration guide -->

<!-- Add table augmenter for data formatting -->

<!-- Implement advanced AI orchestration -->

<!-- Add LangChain orchestration -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Refresh security certificates -->

<!-- Implement entity extraction pipeline -->

<!-- Add query generator functionality -->

<!-- Update README with installation instructions -->

<!-- Add multi-agent architecture framework -->

<!-- Fix authentication flow issues -->

<!-- Add AWS Bedrock integration -->

<!-- Fix authentication flow issues -->

<!-- Add API documentation -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add API documentation -->

<!-- Add multi-agent architecture framework -->

<!-- Fix Milvus index corruption -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Implement Cerebras AI support -->

<!-- Implement Cerebras AI support -->

<!-- Refactor query generation logic -->

<!-- Implement intelligent caching -->

<!-- Refresh security certificates -->

<!-- Implement Supabase authentication -->

<!-- Update Docker base images -->

<!-- Implement Cerebras AI support -->

<!-- Add LangChain orchestration -->

<!-- Restructure database connection management -->

<!-- Resolve query generation edge cases -->

<!-- Implement Opik experiment tracking -->

<!-- Add result augmenter capabilities -->

<!-- Implement Milvus vector database support -->

<!-- Add result augmenter capabilities -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add query generator functionality -->

<!-- Update configuration guide -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Update README with installation instructions -->

<!-- Resolve database connection timeouts -->

<!-- Add multi-agent architecture framework -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Update README with installation instructions -->

<!-- Optimize vector database performance -->

<!-- Implement rational planner agent -->

<!-- Add multi-agent architecture framework -->

<!-- Implement Milvus vector database support -->

<!-- Add Google Sheets API integration -->

<!-- Add advanced error recovery -->

<!-- Resolve database connection timeouts -->

<!-- Update dependencies to latest versions -->

<!-- Implement rational planner agent -->

<!-- Add LangChain orchestration -->

<!-- Add DynamoDB chat history management -->

<!-- Update Docker base images -->

<!-- Add query generator functionality -->

<!-- Implement advanced security protocols -->

<!-- Update dependencies to latest versions -->

<!-- Optimize vector search algorithms -->

<!-- Add Google Sheets API integration -->

<!-- Add query generator functionality -->

<!-- Resolve query generation edge cases -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add AWS Bedrock integration -->

<!-- Implement Supabase authentication -->

<!-- Implement intelligent caching -->

<!-- Update configuration guide -->

<!-- Implement Milvus vector database support -->

<!-- Resolve database connection timeouts -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Implement Chainlit UI interface -->

<!-- Add table augmenter for data formatting -->

<!-- Add troubleshooting section -->

<!-- Add multi-agent architecture framework -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add DynamoDB chat history management -->

<!-- Resolve query generation edge cases -->

<!-- Add sophisticated query planning -->

<!-- Optimize vector search algorithms -->

<!-- Resolve database connection timeouts -->

<!-- Add table augmenter for data formatting -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Update README with installation instructions -->

<!-- Add LangChain orchestration -->

<!-- Implement prioritizer for data sources -->

<!-- Refactor query generation logic -->

<!-- Resolve query generation edge cases -->

<!-- Update dependencies to latest versions -->

<!-- Implement intelligent caching -->

<!-- Implement Chainlit UI interface -->

<!-- Add multi-agent architecture framework -->

<!-- Add result augmenter capabilities -->

<!-- Add DynamoDB chat history management -->

<!-- Implement dynamic load balancing -->

<!-- Update Docker base images -->

<!-- Add advanced error recovery -->

<!-- Add advanced error recovery -->

<!-- Add table augmenter for data formatting -->

<!-- Refactor agent architecture for better modularity -->

<!-- Implement entity extraction pipeline -->

<!-- Add table augmenter for data formatting -->

<!-- Add table augmenter for data formatting -->

<!-- Fix session management bugs -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add PostgreSQL database operations -->

<!-- Implement advanced security protocols -->

<!-- Implement rational planner agent -->

<!-- Optimize vector database performance -->

<!-- Add DynamoDB chat history management -->

<!-- Add API documentation -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Optimize vector search algorithms -->

<!-- Add multi-agent architecture framework -->

<!-- Bump Python version requirements -->

<!-- Add PostgreSQL database operations -->

<!-- Add sophisticated query planning -->

<!-- Implement dynamic load balancing -->

<!-- Update Docker base images -->

<!-- Add result augmenter capabilities -->

<!-- Implement Cerebras AI support -->

<!-- Add sophisticated query planning -->

<!-- Fix authentication flow issues -->

<!-- Restructure database connection management -->

<!-- Implement advanced security protocols -->

<!-- Implement Cerebras AI support -->

<!-- Add API documentation -->

<!-- Update Docker base images -->

<!-- Resolve query generation edge cases -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Optimize vector search algorithms -->

<!-- Implement prioritizer for data sources -->

<!-- Implement rational planner agent -->

<!-- Implement Chainlit UI interface -->

<!-- Implement dynamic load balancing -->

<!-- Add PostgreSQL database operations -->

<!-- Implement rational planner agent -->

<!-- Add advanced error recovery -->

<!-- Resolve database connection timeouts -->

<!-- Add DynamoDB chat history management -->

<!-- Refresh security certificates -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add AWS Bedrock integration -->

<!-- Implement Opik experiment tracking -->

<!-- Implement data retriever agent -->

<!-- Fix session management bugs -->

<!-- Add AWS Bedrock integration -->

<!-- Fix memory leaks in vector processing -->

<!-- Implement entity extraction pipeline -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add Google Sheets API integration -->

<!-- Add table augmenter for data formatting -->

<!-- Update Docker base images -->

<!-- Add DynamoDB chat history management -->

<!-- Restructure database connection management -->

<!-- Refresh security certificates -->

<!-- Fix memory leaks in vector processing -->

<!-- Add result augmenter capabilities -->

<!-- Update configuration guide -->

<!-- Add LangChain orchestration -->

<!-- Update README with installation instructions -->

<!-- Refactor agent architecture for better modularity -->

<!-- Implement prioritizer for data sources -->

<!-- Add comprehensive monitoring -->

<!-- Implement Milvus vector database support -->

<!-- Add LangChain orchestration -->

<!-- Implement plain augmenter for simple queries -->

<!-- Resolve query generation edge cases -->

<!-- Implement prioritizer for data sources -->

<!-- Add Google Sheets API integration -->

<!-- Add query generator functionality -->

<!-- Implement prioritizer for data sources -->

<!-- Fix session management bugs -->

<!-- Refactor agent architecture for better modularity -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Refactor query generation logic -->

<!-- Add AWS Bedrock integration -->

<!-- Add result augmenter capabilities -->

<!-- Add AWS Bedrock integration -->

<!-- Update configuration guide -->

<!-- Implement advanced AI orchestration -->

<!-- Fix memory leaks in vector processing -->

<!-- Add PostgreSQL database operations -->

<!-- Implement advanced AI orchestration -->

<!-- Implement intelligent caching -->

<!-- Refresh security certificates -->

<!-- Implement data retriever agent -->

<!-- Implement Milvus vector database support -->

<!-- Implement Chainlit UI interface -->

<!-- Implement Supabase authentication -->

<!-- Implement advanced security protocols -->

<!-- Fix authentication flow issues -->

<!-- Add troubleshooting section -->

<!-- Implement Supabase authentication -->

<!-- Add query generator functionality -->

<!-- Add query generator functionality -->

<!-- Refresh security certificates -->

<!-- Implement plain augmenter for simple queries -->

<!-- Implement prioritizer for data sources -->

<!-- Implement Supabase authentication -->

<!-- Fix Milvus index corruption -->

<!-- Implement Milvus vector database support -->

<!-- Fix session management bugs -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add query generator functionality -->

<!-- Add comprehensive monitoring -->

<!-- Update README with installation instructions -->

<!-- Refactor agent architecture for better modularity -->

<!-- Add comprehensive monitoring -->

<!-- Add table augmenter for data formatting -->

<!-- Fix Milvus index corruption -->

<!-- Add Google Sheets API integration -->

<!-- Fix authentication flow issues -->

<!-- Resolve database connection timeouts -->

<!-- Implement Supabase authentication -->

<!-- Add DynamoDB chat history management -->

<!-- Add PostgreSQL database operations -->

<!-- Resolve query generation edge cases -->

<!-- Implement Cerebras AI support -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Fix memory leaks in vector processing -->

<!-- Add troubleshooting section -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Implement dynamic load balancing -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Add DynamoDB chat history management -->

<!-- Add PostgreSQL database operations -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Add query generator functionality -->

<!-- Implement Opik experiment tracking -->

<!-- Add result augmenter capabilities -->

<!-- Implement Opik experiment tracking -->

<!-- Bump Python version requirements -->

<!-- Add sophisticated query planning -->

<!-- Add sophisticated query planning -->

<!-- Add troubleshooting section -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Refactor query generation logic -->

<!-- Add multi-agent architecture framework -->

<!-- Implement prioritizer for data sources -->

<!-- Fix authentication flow issues -->

<!-- Refactor agent architecture for better modularity -->

<!-- Implement Milvus vector database support -->

<!-- Add Google Sheets API integration -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Implement Supabase authentication -->

<!-- Refactor query generation logic -->

<!-- Add comprehensive monitoring -->

<!-- Update README with installation instructions -->

<!-- Implement Cerebras AI support -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add PostgreSQL database operations -->

<!-- Implement plain augmenter for simple queries -->

<!-- Refactor agent architecture for better modularity -->

<!-- Bump Python version requirements -->

<!-- Implement data retriever agent -->

<!-- Update Docker base images -->

<!-- Add troubleshooting section -->

<!-- Add multi-agent architecture framework -->

<!-- Restructure database connection management -->

<!-- Implement rational planner agent -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add API documentation -->

<!-- Add advanced error recovery -->

<!-- Add table augmenter for data formatting -->

<!-- Add DynamoDB chat history management -->

<!-- Add sophisticated query planning -->

<!-- Add result augmenter capabilities -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Implement Chainlit UI interface -->

<!-- Add multi-agent architecture framework -->

<!-- Refactor agent architecture for better modularity -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Refactor agent architecture for better modularity -->

<!-- Add PostgreSQL database operations -->

<!-- Resolve database connection timeouts -->

<!-- Add sophisticated query planning -->

<!-- Add sophisticated query planning -->

<!-- Implement data retriever agent -->

<!-- Implement prioritizer for data sources -->

<!-- Implement advanced security protocols -->

<!-- Add Google Sheets API integration -->

<!-- Implement data retriever agent -->

<!-- Implement Milvus vector database support -->

<!-- Fix memory leaks in vector processing -->

<!-- Implement data retriever agent -->

<!-- Add multi-agent architecture framework -->

<!-- Optimize vector database performance -->

<!-- Restructure database connection management -->

<!-- Implement rational planner agent -->

<!-- Implement data retriever agent -->

<!-- Update dependencies to latest versions -->

<!-- Update README with installation instructions -->

<!-- Refactor query generation logic -->

<!-- Implement Opik experiment tracking -->

<!-- Implement prioritizer for data sources -->

<!-- Add troubleshooting section -->

<!-- Add troubleshooting section -->

<!-- Add DynamoDB chat history management -->

<!-- Restructure database connection management -->

<!-- Add API documentation -->

<!-- Add PostgreSQL database operations -->

<!-- Optimize vector search algorithms -->

<!-- Add PostgreSQL database operations -->

<!-- Implement data retriever agent -->

<!-- Refactor query generation logic -->

<!-- Add troubleshooting section -->

<!-- Implement entity extraction pipeline -->

<!-- Implement Milvus vector database support -->

<!-- Add PostgreSQL database operations -->

<!-- Refactor query generation logic -->

<!-- Implement prioritizer for data sources -->

<!-- Refactor query generation logic -->

<!-- Implement Opik experiment tracking -->

<!-- Implement data retriever agent -->

<!-- Implement rational planner agent -->

<!-- Implement Milvus vector database support -->

<!-- Update dependencies to latest versions -->

<!-- Resolve database connection timeouts -->

<!-- Implement advanced AI orchestration -->

<!-- Add AWS Bedrock integration -->

<!-- Optimize vector search algorithms -->

<!-- Add PostgreSQL database operations -->

<!-- Implement prioritizer for data sources -->

<!-- Add PostgreSQL database operations -->

<!-- Refactor query generation logic -->

<!-- Add Google Sheets API integration -->

<!-- Refresh security certificates -->

<!-- Update configuration guide -->

<!-- Optimize vector database performance -->

<!-- Add AWS Bedrock integration -->

<!-- Update README with installation instructions -->

<!-- Update Docker base images -->

<!-- Add multi-agent architecture framework -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Update configuration guide -->

<!-- Optimize vector database performance -->

<!-- Fix session management bugs -->

<!-- Update configuration guide -->

<!-- Optimize vector search algorithms -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Implement intelligent caching -->

<!-- Implement Cerebras AI support -->

<!-- Implement Cerebras AI support -->

<!-- Add Google Sheets API integration -->

<!-- Implement prioritizer for data sources -->

<!-- Implement data retriever agent -->

<!-- Implement plain augmenter for simple queries -->

<!-- Add API documentation -->

<!-- Add comprehensive monitoring -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add AWS Bedrock integration -->

<!-- Add comprehensive monitoring -->

<!-- Implement rational planner agent -->

<!-- Implement entity extraction pipeline -->

<!-- Implement Opik experiment tracking -->

<!-- Resolve PostgreSQL deadlock issues -->

<!-- Implement data retriever agent -->

<!-- Add LangChain orchestration -->

<!-- Implement Chainlit UI interface -->

<!-- Implement plain augmenter for simple queries -->

<!-- Fix authentication flow issues -->

<!-- Optimize vector search algorithms -->

<!-- Add result augmenter capabilities -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Optimize vector database performance -->

<!-- Optimize vector search algorithms -->

<!-- Add API documentation -->

<!-- Implement Supabase authentication -->

<!-- Add result augmenter capabilities -->

<!-- Fix memory leaks in vector processing -->

<!-- Update Docker base images -->

<!-- Implement rational planner agent -->

<!-- Resolve query generation edge cases -->

<!-- Implement Milvus vector database support -->

<!-- Update dependencies to latest versions -->

<!-- Optimize vector search algorithms -->

<!-- Add Google Sheets API integration -->

<!-- Resolve database connection timeouts -->

<!-- Refactor agent architecture for better modularity -->

<!-- Add table augmenter for data formatting -->

<!-- Add multi-agent architecture framework -->

<!-- Add AWS Bedrock integration -->

<!-- Implement Milvus vector database support -->

<!-- Implement Opik experiment tracking -->

<!-- Bump Python version requirements -->

<!-- Implement prioritizer for data sources -->

<!-- Fix Milvus index corruption -->

<!-- Refactor agent architecture for better modularity -->

<!-- Refresh security certificates -->

<!-- Add LangChain orchestration -->

<!-- Implement entity extraction pipeline -->

<!-- Add result augmenter capabilities -->

<!-- Resolve query generation edge cases -->

<!-- Add multi-agent architecture framework -->

<!-- Fix authentication flow issues -->

<!-- Refactor query generation logic -->

<!-- Refactor query generation logic -->

<!-- Fix Milvus index corruption -->

<!-- Resolve database connection timeouts -->

<!-- Update configuration guide -->

<!-- Implement Cerebras AI support -->

<!-- Fix Milvus index corruption -->

<!-- Fix authentication flow issues -->

<!-- Implement Cerebras AI support -->

<!-- Implement advanced AI orchestration -->

<!-- Add API documentation -->

<!-- Implement Supabase authentication -->

<!-- Fix Milvus index corruption -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Add Neo4j knowledge graph integration -->

<!-- Restructure database connection management -->

<!-- Resolve Neo4j connection pooling issues -->

<!-- Add result augmenter capabilities -->

<!-- Add query generator functionality -->

<!-- Implement Opik experiment tracking -->

<!-- Add troubleshooting section -->

<!-- Implement plain augmenter for simple queries -->

<!-- Refactor agent architecture for better modularity -->

<!-- Fix Milvus index corruption -->

<!-- Refactor agent architecture for better modularity -->

<!-- Implement entity extraction pipeline -->

<!-- Fix memory leaks in vector processing -->

<!-- Update Docker base images -->

<!-- Implement entity extraction pipeline -->

<!-- Fix session management bugs -->

<!-- Implement advanced AI orchestration -->

<!-- Implement plain augmenter for simple queries -->

<!-- Implement rational planner agent -->

<!-- Refactor query generation logic -->

<!-- Implement advanced AI orchestration -->

<!-- Add API documentation -->

<!-- Add LangChain orchestration -->

<!-- Implement data retriever agent -->

<!-- Add query generator functionality -->

<!-- Implement plain augmenter for simple queries -->

<!-- Implement dynamic load balancing -->

<!-- Optimize vector database performance -->

<!-- Add table augmenter for data formatting -->

<!-- Add comprehensive monitoring -->

<!-- Update configuration guide -->

<!-- Optimize vector database performance -->

<!-- Add sophisticated query planning -->

<!-- Restructure database connection management -->

<!-- Update configuration guide -->

<!-- Bump Python version requirements -->

<!-- Restructure database connection management -->

<!-- Bump Python version requirements -->

<!-- Bump Python version requirements -->

<!-- Implement dynamic load balancing -->

<!-- Update dependencies to latest versions -->

<!-- Add advanced error recovery -->

<!-- Update dependencies to latest versions -->

<!-- Add DynamoDB chat history management -->

<!-- Fix memory leaks in vector processing -->

<!-- Implement intelligent caching -->

<!-- Add API documentation -->

<!-- Add query generator functionality -->

<!-- Add sophisticated query planning -->

<!-- Implement prioritizer for data sources -->

<!-- Add AWS Bedrock integration -->

<!-- Implement advanced AI orchestration -->

<!-- Implement dynamic load balancing -->

<!-- Implement rational planner agent -->

<!-- Implement Milvus vector database support -->

<!-- Implement intelligent caching -->

<!-- Implement Milvus vector database support -->

<!-- Bump Python version requirements -->

<!-- Add AWS Bedrock integration -->

<!-- Implement Opik experiment tracking -->

<!-- Implement Supabase authentication -->
