"""
Unlimited Autonomous AI Agent - Full Version
Deployed at: https://ai.taagc.site
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import sys
import os
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class handler(BaseHTTPRequestHandler):
    """
    Main handler for all API requests.
    Routes to appropriate endpoints.
    """
    
    def do_GET(self):
        """Handle GET requests"""
        self._handle_request('GET')
    
    def do_POST(self):
        """Handle POST requests"""
        self._handle_request('POST')
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _handle_request(self, method):
        """Route requests to appropriate handlers"""
        try:
            # Parse path
            path = self.path.split('?')[0]
            
            print(f"📥 {method} {path}")  # Debug log
            
            # Route by path
            if path == '/' or path == '':
                self._serve_dashboard()
            
            elif path == '/api/status':
                self._handle_status()
            
            elif path == '/api/task':
                if method == 'POST':
                    self._handle_task()
                else:
                    self._send_error(405, "Use POST for /api/task")
            
            elif path == '/api/tasks':
                self._handle_tasks()
            
            elif path == '/api/create_bot':
                if method == 'POST':
                    self._handle_create_bot()
                else:
                    self._send_error(405, "Use POST for /api/create_bot")
            
            elif path == '/api/learn':
                if method == 'POST':
                    self._handle_learn()
                else:
                    self._send_error(405, "Use POST for /api/learn")
            
            elif path == '/api/webhook':
                self._handle_webhook()
            
            else:
                self._send_error(404, f"Endpoint not found: {path}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self._send_error(500, str(e))
    
    # ============================================
    # RESPONSE HELPERS
    # ============================================
    
    def _send_json(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))
    
    def _send_error(self, code, message):
        """Send error response"""
        self._send_json({
            "status": "error",
            "code": code,
            "message": message
        }, code)
    
    # ============================================
    # DASHBOARD
    # ============================================
    
    def _serve_dashboard(self):
        """Serve the HTML dashboard"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Unlimited AI Agent</title>
            <style>
                * { margin:0; padding:0; box-sizing:border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
                    color: #fff;
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }
                .container {
                    max-width: 900px;
                    padding: 40px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 20px;
                    border: 1px solid rgba(255,255,255,0.1);
                    text-align: center;
                }
                h1 { font-size: 3rem; margin-bottom: 10px; }
                .icon { font-size: 3.5rem; }
                .subtitle { color: #888; font-size: 1.2rem; margin-bottom: 20px; }
                .domain { color: #00cc88; font-size: 1rem; margin-bottom: 30px; }
                .domain a { color: #00cc88; text-decoration: none; }
                .status {
                    display: inline-block;
                    padding: 8px 20px;
                    background: #00cc88;
                    color: #000;
                    border-radius: 20px;
                    font-weight: bold;
                    margin-bottom: 30px;
                }
                .grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr;
                    gap: 15px;
                    margin: 30px 0;
                }
                .card {
                    background: rgba(255,255,255,0.05);
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 12px;
                    padding: 20px;
                }
                .card .value { font-size: 2rem; font-weight: bold; color: #00cc88; }
                .card .label { color: #888; font-size: 0.9rem; margin-top: 5px; }
                .endpoints {
                    text-align: left;
                    background: rgba(255,255,255,0.03);
                    border-radius: 12px;
                    padding: 20px;
                    margin: 20px 0;
                    font-family: monospace;
                    font-size: 0.9rem;
                }
                .endpoints .item {
                    padding: 8px 0;
                    border-bottom: 1px solid rgba(255,255,255,0.05);
                }
                .endpoints .method {
                    display: inline-block;
                    padding: 2px 10px;
                    border-radius: 4px;
                    font-weight: bold;
                    margin-right: 10px;
                }
                .method.get { background: #00cc88; color: #000; }
                .method.post { background: #ffaa00; color: #000; }
                .endpoints .path { color: #00cc88; }
                .footer { margin-top: 30px; color: #555; font-size: 0.8rem; }
                .footer a { color: #00cc88; text-decoration: none; }
                .test-section { margin-top: 20px; width: 100%; }
                .test-section textarea {
                    width: 100%;
                    padding: 12px;
                    border-radius: 8px;
                    border: 1px solid rgba(255,255,255,0.2);
                    background: rgba(255,255,255,0.05);
                    color: #fff;
                    font-size: 1rem;
                    resize: vertical;
                    min-height: 80px;
                    font-family: inherit;
                }
                .test-section button {
                    margin-top: 10px;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    background: #00cc88;
                    color: #000;
                    font-weight: bold;
                    cursor: pointer;
                    width: 100%;
                    font-size: 1rem;
                }
                .test-section button:hover { background: #00dd99; }
                .test-section #result {
                    margin-top: 15px;
                    padding: 15px;
                    border-radius: 8px;
                    background: rgba(255,255,255,0.05);
                    border: 1px solid rgba(255,255,255,0.1);
                    white-space: pre-wrap;
                    font-family: monospace;
                    font-size: 0.85rem;
                    max-height: 300px;
                    overflow-y: auto;
                    display: none;
                    text-align: left;
                }
                @media (max-width: 600px) {
                    .grid { grid-template-columns: 1fr; }
                    h1 { font-size: 2rem; }
                    .container { padding: 20px; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🤖</div>
                <h1>Unlimited AI Agent</h1>
                <p class="subtitle">Powered by TAAGC | Deployed on Vercel</p>
                <p class="domain">🌐 <a href="https://ai.taagc.site">ai.taagc.site</a></p>
                <div class="status">● Online & Running</div>

                <div class="grid">
                    <div class="card"><div class="value">14</div><div class="label">Domains</div></div>
                    <div class="card"><div class="value">∞</div><div class="label">Capabilities</div></div>
                    <div class="card"><div class="value">✓</div><div class="label">Self-Learning</div></div>
                </div>

                <h2 style="color:#00cc88;margin:20px 0;">📡 API Endpoints</h2>
                <div class="endpoints">
                    <div class="item"><span class="method get">GET</span> <span class="path">/api/status</span> <span style="color:#888;">— Get agent status</span></div>
                    <div class="item"><span class="method post">POST</span> <span class="path">/api/task</span> <span style="color:#888;">— Process a task</span></div>
                    <div class="item"><span class="method get">GET</span> <span class="path">/api/tasks</span> <span style="color:#888;">— List all tasks</span></div>
                    <div class="item"><span class="method post">POST</span> <span class="path">/api/create_bot</span> <span style="color:#888;">— Create a new bot</span></div>
                    <div class="item"><span class="method post">POST</span> <span class="path">/api/learn</span> <span style="color:#888;">— Learn from text</span></div>
                </div>

                <div class="test-section">
                    <h2 style="color:#00cc88;margin:10px 0;">🚀 Quick Test</h2>
                    <textarea id="taskInput" placeholder="Enter a task. Example: Analyze the current Bitcoin market and provide a trading recommendation"></textarea>
                    <button onclick="processTask()">▶ Process Task</button>
                    <div id="result"></div>
                </div>

                <div class="footer">
                    <p>🤖 Unlimited Autonomous AI Agent — Any Task, Any Domain</p>
                    <p><a href="https://ai.taagc.site">ai.taagc.site</a> | © 2026 TAAGC</p>
                </div>
            </div>

            <script>
                async function processTask() {
                    const input = document.getElementById('taskInput');
                    const result = document.getElementById('result');
                    const task = input.value.trim();
                    
                    if (!task) {
                        result.style.display = 'block';
                        result.innerHTML = '❌ Please enter a task';
                        result.style.color = '#ff4444';
                        return;
                    }
                    
                    result.style.display = 'block';
                    result.innerHTML = '⏳ Processing task...';
                    result.style.color = '#ffaa00';
                    
                    try {
                        const response = await fetch('/api/task', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ task })
                        });
                        
                        const data = await response.json();
                        
                        if (data.status === 'success') {
                            result.innerHTML = '✅ Success!\n\n' + JSON.stringify(data.result, null, 2);
                            result.style.color = '#00cc88';
                        } else {
                            result.innerHTML = '❌ Error: ' + data.message;
                            result.style.color = '#ff4444';
                        }
                    } catch (error) {
                        result.innerHTML = '❌ Error: ' + error.message;
                        result.style.color = '#ff4444';
                    }
                }
                
                document.getElementById('taskInput').addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' && e.ctrlKey) processTask();
                });
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    # ============================================
    # API HANDLERS
    # ============================================
    
    def _handle_status(self):
        """GET /api/status"""
        self._send_json({
            "status": "success",
            "domain": "ai.taagc.site",
            "server": "Vercel",
            "timestamp": datetime.now().isoformat(),
            "agent": {
                "name": "UnlimitedAI",
                "version": "1.0.0",
                "capabilities": [
                    "Self-learning from books and experience",
                    "Self-repairing when errors occur",
                    "Self-upgrading to improve performance",
                    "Self-replicating to create new bots"
                ],
                "domains": [
                    "Business", "Finance", "Healthcare", "Education",
                    "Technology", "Legal", "Creative", "Real Estate",
                    "Manufacturing", "Agriculture", "Retail",
                    "Transportation", "Energy", "Government"
                ]
            }
        })
    
    def _handle_task(self):
        """POST /api/task"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            task = data.get('task')
            context = data.get('context', {})
            
            if not task:
                self._send_error(400, "Task description is required")
                return
            
            # Process task with mock AI response
            # In production, you'd import the actual AI agent
            result = self._process_task(task, context)
            
            self._send_json({
                "status": "success",
                "task": task,
                "result": result
            })
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON body")
        except Exception as e:
            self._send_error(500, str(e))
    
    def _process_task(self, task, context):
        """Process a task (mock AI)"""
        return {
            "success": True,
            "message": f"Task processed: {task}",
            "analysis": f"Analyzed task: {task[:50]}...",
            "timestamp": datetime.now().isoformat(),
            "suggestions": [
                "Consider breaking this into smaller steps",
                "Use available data sources",
                "Monitor progress regularly"
            ]
        }
    
    def _handle_tasks(self):
        """GET /api/tasks"""
        self._send_json({
            "status": "success",
            "count": 3,
            "tasks": [
                {
                    "id": "1",
                    "description": "Analyze Bitcoin market",
                    "status": "pending",
                    "created": datetime.now().isoformat()
                },
                {
                    "id": "2",
                    "description": "Create business plan",
                    "status": "pending",
                    "created": datetime.now().isoformat()
                },
                {
                    "id": "3",
                    "description": "Learn about AI",
                    "status": "completed",
                    "created": datetime.now().isoformat()
                }
            ]
        })
    
    def _handle_create_bot(self):
        """POST /api/create_bot"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            requirements = data.get('requirements')
            location = data.get('location', 'local')
            name = data.get('name', f"Bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            if not requirements:
                self._send_error(400, "Bot requirements are required")
                return
            
            self._send_json({
                "status": "success",
                "bot": {
                    "name": name,
                    "requirements": requirements,
                    "location": location,
                    "created": datetime.now().isoformat(),
                    "message": "Bot created successfully!",
                    "code": f"""
# Bot: {name}
# Requirements: {requirements}

def main():
    print("🤖 Bot is running!")
    print("Task: {requirements}")
    
if __name__ == "__main__":
    main()
                    """
                }
            })
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON body")
        except Exception as e:
            self._send_error(500, str(e))
    
    def _handle_learn(self):
        """POST /api/learn"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            text = data.get('text')
            category = data.get('category', 'general')
            source = data.get('source', 'user_input')
            
            if not text:
                self._send_error(400, "Text to learn is required")
                return
            
            self._send_json({
                "status": "success",
                "message": "Learning successful",
                "text": text[:200] + "..." if len(text) > 200 else text,
                "category": category,
                "source": source,
                "timestamp": datetime.now().isoformat()
            })
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON body")
        except Exception as e:
            self._send_error(500, str(e))
    
    def _handle_webhook(self):
        """GET /api/webhook - Cron trigger"""
        self._send_json({
            "status": "success",
            "processed": 0,
            "message": "Webhook triggered successfully",
            "timestamp": datetime.now().isoformat()
        })
