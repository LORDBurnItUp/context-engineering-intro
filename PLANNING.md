# AI Call Center Army - Planning Document

## 🎯 Project Vision
Build an autonomous, self-improving AI call center system using LiveKit for real-time voice interactions, combining multiple AI frameworks (OttoAgents, Archon, Context Protocol) with RAG-based memory to create specialized agents for support, troubleshooting, and sales across HVAC, roofing, solar, and cold-calling campaigns.

## 🏗️ Architecture Overview

### Core Components

1. **LiveKit Voice Infrastructure**
   - Real-time TTS/STT using LiveKit agents
   - WebRTC for low-latency voice communication
   - Multi-session management for concurrent calls
   - Voice quality monitoring and optimization

2. **Agent Hierarchy**
   - **Master Orchestrator**: Routes calls, monitors performance, spawns new agents
   - **Industry Specialists**: HVAC, Roofing, Solar experts
   - **Role Specialists**: Support, Troubleshooting, Sales, Cold Calling
   - **Learning Agent**: Analyzes call patterns, improves prompts

3. **RAG Memory System**
   - Vector database (ChromaDB/Qdrant) for conversation history
   - Company knowledge base per industry
   - Customer profile memory
   - Call outcome tracking
   - Auto-updating knowledge from successful calls

4. **MCP Server Integration**
   - Dynamic tool loading based on call context
   - CRM integration (custom or open-source)
   - Email automation
   - Calendar scheduling
   - Payment processing hooks

5. **Self-Improvement Loop**
   - Call recording and transcription
   - Success metric tracking (conversion, satisfaction, resolution)
   - Automated A/B testing of prompts
   - Fine-tuning suggestions based on patterns

6. **Lead Management & CRM**
   - Call outcome classification (Hot Lead, Follow-up, Rejection)
   - Automated email follow-ups
   - Task creation for human team
   - Pipeline tracking
   - ROI analytics

## 📁 Project Structure

```
call-center-ai/
├── agents/
│   ├── orchestrator/
│   │   ├── agent.py          # Master routing agent
│   │   ├── tools.py          # Call routing, load balancing
│   │   └── prompts.py        # Dynamic routing logic
│   ├── industry/
│   │   ├── hvac_agent/       # HVAC specialist
│   │   ├── roofing_agent/    # Roofing specialist
│   │   └── solar_agent/      # Solar specialist
│   ├── role/
│   │   ├── support_agent/    # Customer support
│   │   ├── troubleshoot_agent/ # Technical troubleshooting
│   │   ├── sales_agent/      # Sales closer
│   │   └── cold_call_agent/  # Outbound cold calling
│   └── learning_agent/
│       ├── agent.py          # Analyzes and improves system
│       ├── tools.py          # Prompt optimization, A/B testing
│       └── prompts.py        # Meta-learning prompts
├── livekit_integration/
│   ├── voice_agent.py        # LiveKit agent wrapper
│   ├── session_manager.py    # Handle multiple concurrent calls
│   ├── tts_config.py         # TTS provider config (ElevenLabs/OpenAI)
│   └── stt_config.py         # STT provider config
├── rag_system/
│   ├── vector_store.py       # Vector DB operations
│   ├── embeddings.py         # Embedding generation
│   ├── retrieval.py          # Context retrieval
│   └── memory_manager.py     # Conversation memory
├── crm/
│   ├── lead_tracker.py       # Lead management
│   ├── email_automation.py   # Follow-up emails
│   ├── analytics.py          # Performance metrics
│   └── pipeline.py           # Sales pipeline management
├── mcp_servers/
│   ├── crm_server/           # Custom CRM MCP server
│   ├── calendar_server/      # Scheduling MCP server
│   └── dynamic_loader.py     # Load MCPs as needed
├── web_interface/
│   ├── dashboard.py          # FastAPI dashboard
│   ├── call_monitor.py       # Real-time call monitoring
│   └── analytics_ui.py       # Performance analytics UI
├── deployment/
│   ├── docker-compose.yml    # Full stack deployment
│   ├── hostinger_deploy.sh   # Hostinger deployment script
│   └── nginx.conf            # Reverse proxy config
├── tests/
│   ├── test_agents/
│   ├── test_livekit/
│   └── test_rag/
├── config/
│   ├── industry_knowledge/   # Knowledge bases per industry
│   ├── prompts/              # Versioned prompt templates
│   └── settings.py           # Environment configuration
├── venv_linux/               # Python virtual environment
├── requirements.txt
├── .env.example
└── README.md
```

## 🧠 Intelligence Design

### Token Efficiency Strategies
1. **Prompt Caching**: Cache common knowledge base chunks
2. **Selective RAG**: Only retrieve relevant context (max 3-5 chunks)
3. **Streaming Responses**: Use streaming to reduce latency
4. **Model Selection**: Use Haiku for routing, Sonnet for complex reasoning
5. **Context Pruning**: Summarize old conversation turns

### Self-Improvement Mechanisms
1. **Call Analysis**: Post-call automated analysis for learnings
2. **Success Pattern Detection**: Identify what works across calls
3. **Prompt Evolution**: Version and A/B test prompt variations
4. **Knowledge Base Updates**: Auto-add successful responses to RAG
5. **Agent Cloning**: Spawn new specialized agents based on needs

## 🔧 Technology Stack

### Core
- **Python 3.11+** with asyncio for concurrency
- **LiveKit** for real-time voice
- **Pydantic AI** for agent framework
- **FastAPI** for web API and dashboard
- **SQLModel** for database ORM

### AI/ML
- **Claude Sonnet 4.5** for complex reasoning
- **Claude Haiku** for fast routing
- **ChromaDB/Qdrant** for vector storage
- **Sentence Transformers** for embeddings

### Infrastructure
- **Docker** for containerization
- **PostgreSQL** for relational data
- **Redis** for caching and queues
- **Nginx** for reverse proxy
- **Hostinger VPS** for hosting

### LiveKit Stack
- **livekit** - Core SDK
- **livekit-agents** - Agent framework
- **livekit-plugins-openai** - OpenAI TTS/STT
- **livekit-plugins-elevenlabs** - ElevenLabs TTS (premium voice)
- **livekit-plugins-deepgram** - Deepgram STT (fast)

## 🎨 Design Patterns

### Agent Communication
- **Message Bus**: Redis pub/sub for agent coordination
- **Event-Driven**: Agents react to call events (started, ended, transferred)
- **Hierarchical**: Orchestrator -> Industry Agent -> Role Agent

### RAG Pattern
- **Hybrid Search**: Vector similarity + keyword matching
- **Reranking**: Use cross-encoder for better relevance
- **Metadata Filtering**: Filter by industry, role, outcome

### Error Handling
- **Graceful Degradation**: Fallback to simpler agents if complex fails
- **Circuit Breaker**: Stop calling failing services
- **Retry Logic**: Exponential backoff for transient failures

## 📊 Success Metrics

### Call Quality
- Average Handle Time (AHT)
- First Call Resolution (FCR)
- Customer Satisfaction Score (CSAT)
- Sentiment analysis score

### Business Impact
- Lead conversion rate
- Revenue per call
- Follow-up completion rate
- Cost per acquisition

### System Performance
- Tokens used per call
- Response latency
- Concurrent call capacity
- Uptime percentage

## 🚀 Implementation Phases

### Phase 1: Foundation (Days 1-2)
- Set up project structure
- Install dependencies
- Configure LiveKit server
- Basic voice agent with TTS/STT
- Simple conversation loop

### Phase 2: Agent System (Days 3-4)
- Implement orchestrator agent
- Create industry specialist templates
- Create role specialist templates
- Agent routing logic

### Phase 3: RAG & Memory (Days 5-6)
- Set up vector database
- Implement embeddings pipeline
- Build retrieval system
- Conversation memory management

### Phase 4: CRM & Tracking (Days 7-8)
- Lead tracking database
- Email automation
- Call analytics
- Dashboard UI

### Phase 5: Self-Improvement (Days 9-10)
- Call analysis system
- Prompt versioning
- A/B testing framework
- Learning agent implementation

### Phase 6: Deployment (Days 11-12)
- Docker containerization
- Hostinger deployment
- Monitoring setup
- Load testing

## 🔒 Security & Compliance

- **Data Privacy**: Encrypt call recordings at rest
- **PII Protection**: Mask sensitive information in logs
- **GDPR/CCPA**: Right to deletion, data export
- **Rate Limiting**: Prevent abuse
- **Authentication**: JWT for API access

## 💰 Cost Optimization

- **Model Selection**: Haiku for 80% of operations
- **Caching**: Aggressive caching of common queries
- **Batch Processing**: Batch non-urgent tasks
- **Open Source**: Use open-source tools where possible
- **Monitoring**: Track costs per call, optimize hot paths

## 🎯 JetBrains IDE Integration

- **.idea/** configuration for WebStorm/PyCharm
- **Run Configurations** for all services
- **Remote Debugging** setup for deployed agents
- **Database Tools** integration for PostgreSQL
- **Live Templates** for common patterns

## 📝 Naming Conventions

- **Files**: snake_case (e.g., `lead_tracker.py`)
- **Classes**: PascalCase (e.g., `LeadTracker`)
- **Functions**: snake_case (e.g., `track_lead`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`)
- **Agents**: {purpose}_agent (e.g., `sales_agent`)
- **Tools**: {action}_{object} (e.g., `search_knowledge_base`)

## 🔄 Git Workflow

- **Main Branch**: `main` (production-ready)
- **Feature Branches**: `feature/{feature-name}`
- **Claude Branches**: `claude/{session-id}` (auto-created)
- **Commit Style**: Conventional commits (feat:, fix:, docs:, etc.)

## 📚 Documentation Standards

- **README.md**: Setup and quick start
- **API docs**: Auto-generated with FastAPI
- **Agent docs**: Markdown in each agent folder
- **Deployment docs**: Step-by-step in deployment/

---

**Last Updated**: 2026-01-21
**Status**: Active Development
**Version**: 0.1.0-alpha
