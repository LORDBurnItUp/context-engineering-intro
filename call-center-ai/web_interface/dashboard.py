"""FastAPI Dashboard for AI Call Center monitoring."""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
from datetime import datetime

from config import settings
from livekit_integration.session_manager import session_manager
from crm.lead_tracker import lead_tracker
from loguru import logger

app = FastAPI(title="AI Call Center Dashboard", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket connections for real-time updates
active_connections: List[WebSocket] = []


@app.get("/")
async def root():
    """Root endpoint with simple dashboard."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Call Center Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                text-align: center;
                font-size: 3em;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                font-size: 1.2em;
                opacity: 0.9;
                margin-bottom: 40px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }
            .stat-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                transition: transform 0.3s;
            }
            .stat-card:hover {
                transform: translateY(-5px);
                background: rgba(255, 255, 255, 0.15);
            }
            .stat-value {
                font-size: 3em;
                font-weight: bold;
                margin: 10px 0;
            }
            .stat-label {
                font-size: 1.1em;
                opacity: 0.9;
            }
            .section {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 20px;
            }
            .section h2 {
                margin-top: 0;
                border-bottom: 2px solid rgba(255, 255, 255, 0.3);
                padding-bottom: 10px;
            }
            .api-links {
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                margin-top: 20px;
            }
            .api-link {
                background: rgba(255, 255, 255, 0.2);
                padding: 12px 24px;
                border-radius: 8px;
                text-decoration: none;
                color: white;
                transition: all 0.3s;
            }
            .api-link:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: scale(1.05);
            }
            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #00ff00;
                animation: pulse 2s infinite;
                margin-right: 8px;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Call Center Army</h1>
            <p class="subtitle">
                <span class="status-indicator"></span>
                System Online • Autonomous Agent Platform
            </p>

            <div class="stats" id="stats">
                <div class="stat-card">
                    <div class="stat-label">Active Calls</div>
                    <div class="stat-value" id="active-calls">0</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Total Leads</div>
                    <div class="stat-value" id="total-leads">0</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">System Load</div>
                    <div class="stat-value" id="system-load">0%</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Uptime</div>
                    <div class="stat-value">99.9%</div>
                </div>
            </div>

            <div class="section">
                <h2>📊 API Endpoints</h2>
                <div class="api-links">
                    <a href="/health" class="api-link">🏥 Health Check</a>
                    <a href="/stats" class="api-link">📈 Statistics</a>
                    <a href="/sessions" class="api-link">📞 Active Sessions</a>
                    <a href="/leads" class="api-link">🎯 Leads</a>
                    <a href="/docs" class="api-link">📚 API Docs</a>
                </div>
            </div>

            <div class="section">
                <h2>🎯 Quick Stats</h2>
                <p>✅ Orchestrator Agent: Active</p>
                <p>✅ Industry Specialists: HVAC, Roofing, Solar</p>
                <p>✅ Role Agents: Support, Sales, Troubleshooting</p>
                <p>✅ RAG Memory: Connected</p>
                <p>✅ CRM System: Operational</p>
            </div>
        </div>

        <script>
            // Auto-refresh stats every 5 seconds
            async function updateStats() {
                try {
                    const response = await fetch('/stats');
                    const data = await response.json();

                    document.getElementById('active-calls').textContent = data.active_sessions;
                    document.getElementById('total-leads').textContent = data.total_leads;
                    document.getElementById('system-load').textContent = data.load_percentage.toFixed(1) + '%';
                } catch (error) {
                    console.error('Error updating stats:', error);
                }
            }

            // Update immediately and then every 5 seconds
            updateStats();
            setInterval(updateStats, 5000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/stats")
async def get_stats():
    """Get system statistics."""
    pipeline = await lead_tracker.get_pipeline_summary()

    return {
        "active_sessions": session_manager.get_active_sessions_count(),
        "load_percentage": session_manager.get_load_percentage(),
        "max_concurrent": session_manager.max_concurrent_sessions,
        "total_leads": pipeline["total_leads"],
        "leads_by_status": pipeline["by_status"],
        "leads_by_industry": pipeline["by_industry"],
        "estimated_pipeline_value": pipeline["total_estimated_value"],
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/sessions")
async def get_sessions():
    """Get all active call sessions."""
    sessions = await session_manager.get_all_sessions()

    return {
        "count": len(sessions),
        "sessions": [
            {
                "session_id": s.session_id,
                "participant_id": s.participant_id,
                "industry": s.industry,
                "role": s.role,
                "agent_id": s.agent_id,
                "status": s.status,
                "start_time": s.start_time.isoformat(),
                "duration_seconds": (datetime.utcnow() - s.start_time).total_seconds(),
            }
            for s in sessions
        ],
    }


@app.get("/leads")
async def get_leads():
    """Get lead pipeline summary."""
    pipeline = await lead_tracker.get_pipeline_summary()
    follow_ups = await lead_tracker.get_leads_needing_follow_up()

    return {
        "summary": pipeline,
        "follow_ups_needed": len(follow_ups),
        "follow_up_leads": [
            {
                "lead_id": lead.lead_id,
                "name": lead.name,
                "industry": lead.industry,
                "status": lead.status.value,
                "next_follow_up": lead.next_follow_up.isoformat() if lead.next_follow_up else None,
            }
            for lead in follow_ups[:10]  # Show top 10
        ],
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates."""
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            # Send stats every 2 seconds
            stats = await get_stats()
            await websocket.send_json(stats)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.on_event("startup")
async def startup_event():
    """Startup tasks."""
    logger.info(f"🚀 Starting AI Call Center Dashboard on port 8080")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Version: {settings.app_version}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "web_interface.dashboard:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.debug,
    )
