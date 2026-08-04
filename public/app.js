/**
 * Unlimited AI Agent - Frontend Application
 * Deployed at: https://ai.taagc.site
 */

const API_BASE = '/api';
const DOMAIN = 'ai.taagc.site';

// ============================================
// 1. INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log(`🤖 Unlimited AI Agent - ${DOMAIN}`);
    
    // Load all data
    loadStatus();
    loadTasks();
    loadStats();
    loadBots();
    
    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadStatus();
        loadTasks();
        loadStats();
        loadBots();
    }, 30000);
});

// ============================================
// 2. LOAD STATS
// ============================================

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        if (data.status === 'success') {
            const agent = data.agent || {};
            
            document.getElementById('statTasks').textContent = 
                agent.tasks_completed || agent.tasks_executed || 0;
            
            document.getElementById('statDomains').textContent = 
                agent.domains?.length || 14;
            
            document.getElementById('statMemory').textContent = 
                agent.memory?.knowledge_graph?.total_concepts || 0;
            
            const successRate = agent.memory?.experience_db?.success_rate || 0;
            document.getElementById('statSuccess').textContent = 
                (successRate * 100).toFixed(1) + '%';
            
            document.getElementById('statBots').textContent = 
                agent.bots_created || 0;
            
            document.getElementById('statUptime').textContent = 
                formatUptime(agent.uptime || 0);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// ============================================
// 3. LOAD STATUS
// ============================================

async function loadStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayStatus(data);
            updateStatusBadge(true);
        } else {
            displayError('statusContainer', 'Failed to load status');
            updateStatusBadge(false);
        }
    } catch (error) {
        displayError('statusContainer', 'Error: ' + error.message);
        updateStatusBadge(false);
    }
}

function displayStatus(data) {
    const container = document.getElementById('statusContainer');
    const agent = data.agent || {};
    const memory = agent.memory || {};
    const experience = memory.experience_db || {};
    
    container.innerHTML = `
        <div class="status-grid">
            <div><strong>Domain:</strong> ${data.domain || DOMAIN}</div>
            <div><strong>Status:</strong> ${agent.state || 'Online'}</div>
            <div><strong>Version:</strong> ${agent.version || '1.0.0'}</div>
            <div><strong>Tasks:</strong> ${agent.tasks_completed || agent.tasks_executed || 0}</div>
            <div><strong>Domains:</strong> ${agent.domains?.length || 14}</div>
            <div><strong>Concepts:</strong> ${memory.knowledge_graph?.total_concepts || 0}</div>
            <div><strong>Experiences:</strong> ${experience.total || 0}</div>
            <div><strong>Success Rate:</strong> ${(experience.success_rate || 0) * 100}%</div>
            <div><strong>Capabilities:</strong> ${agent.capabilities?.length || 0}</div>
            <div><strong>Uptime:</strong> ${formatUptime(agent.uptime || 0)}</div>
        </div>
    `;
}

function updateStatusBadge(isOnline) {
    const badge = document.getElementById('statusBadge');
    if (isOnline) {
        badge.textContent = '● Online';
        badge.style.background = '#00cc88';
        badge.style.color = '#000';
    } else {
        badge.textContent = '● Offline';
        badge.style.background = '#ff4444';
        badge.style.color = '#fff';
    }
}

function formatUptime(seconds) {
    if (seconds < 60) return Math.floor(seconds) + 's';
    if (seconds < 3600) return Math.floor(seconds / 60) + 'm';
    if (seconds < 86400) return Math.floor(seconds / 3600) + 'h';
    return Math.floor(seconds / 86400) + 'd';
}

// ============================================
// 4. LOAD TASKS
// ============================================

async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayTasks(data.tasks, data.count);
        } else {
            displayError('tasksContainer', 'Failed to load tasks');
        }
    } catch (error) {
        displayError('tasksContainer', 'Error: ' + error.message);
    }
}

function displayTasks(tasks, count) {
    const container = document.getElementById('tasksContainer');
    
    if (!tasks || tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <span class="icon">📋</span>
                <p>No tasks yet. Create your first task above!</p>
            </div>
        `;
        return;
    }
    
    let html = `<div class="task-count">📋 ${count || tasks.length} tasks</div>`;
    
    const recent = tasks.slice(-5).reverse();
    recent.forEach(task => {
        const statusClass = task.status || 'pending';
        html += `
            <div class="task-item">
                <div class="task-header">
                    <span class="task-priority">Priority: ${task.priority || 3}</span>
                    <span class="task-status ${statusClass}">${statusClass}</span>
                </div>
                <div class="task-description">${task.description || task.task || 'No description'}</div>
                <div class="task-meta">
                    <span>🕐 ${formatDate(task.created || task.timestamp)}</span>
                    ${task.completed ? `<span>✅ ${formatDate(task.completed)}</span>` : ''}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    try {
        const date = new Date(dateStr);
        return date.toLocaleString();
    } catch {
        return dateStr;
    }
}

// ============================================
// 5. LOAD BOTS
// ============================================

async function loadBots() {
    try {
        const response = await fetch(`${API_BASE}/tasks`);
        const data = await response.json();
        
        // Check if there are any bot-related tasks
        const container = document.getElementById('botsContainer');
        const tasks = data.tasks || [];
        const botTasks = tasks.filter(t => 
            t.description && t.description.toLowerCase().includes('bot')
        );
        
        if (botTasks.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <span class="icon">🤖</span>
                    <p>No bots created yet. Use the form above to create one!</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        botTasks.slice(-3).reverse().forEach(task => {
            html += `
                <div class="bot-item">
                    <div class="bot-name">🤖 ${task.description || 'Bot'}</div>
                    <div class="bot-requirements">Status: ${task.status || 'pending'}</div>
                    <div class="bot-location">🕐 ${formatDate(task.created)}</div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading bots:', error);
    }
}

// ============================================
// 6. PROCESS TASK
// ============================================

async function processTask() {
    const input = document.getElementById('taskInput');
    const priority = document.getElementById('taskPriority');
    const deadline = document.getElementById('taskDeadline');
    const resultDiv = document.getElementById('taskResult');
    const btn = document.getElementById('processBtn');
    
    const task = input.value.trim();
    
    if (!task) {
        showResult(resultDiv, '❌ Please enter a task description', 'error');
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Processing...';
    resultDiv.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/task`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                task: task,
                context: {
                    priority: parseInt(priority.value),
                    deadline: deadline.value || null
                }
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const result = data.result || {};
            showResult(resultDiv, `
✅ Task processed successfully!

📋 Task: ${task}

📊 Result:
${JSON.stringify(result, null, 2)}
            `, 'success');
            
            // Reload data
            loadTasks();
            loadStats();
            loadBots();
            
            // Clear input
            input.value = '';
            deadline.value = '';
        } else {
            showResult(resultDiv, `❌ Error: ${data.message || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        showResult(resultDiv, `❌ Error: ${error.message}`, 'error');
    }
    
    btn.disabled = false;
    btn.textContent = '▶ Process Task';
}

// ============================================
// 7. CREATE BOT
// ============================================

async function createBot() {
    const requirements = document.getElementById('botRequirements').value.trim();
    const location = document.getElementById('botLocation').value;
    const name = document.getElementById('botName').value.trim();
    const resultDiv = document.getElementById('botResult');
    const btn = document.getElementById('createBotBtn');
    
    if (!requirements) {
        showResult(resultDiv, '❌ Please enter bot requirements', 'error');
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Creating...';
    resultDiv.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/create_bot`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                requirements: requirements,
                location: location,
                name: name || undefined
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const bot = data.bot || {};
            showResult(resultDiv, `
✅ Bot created successfully!

🤖 Name: ${bot.name || 'Unnamed'}
📍 Location: ${bot.location || 'local'}
📝 Requirements: ${requirements}

${bot.code ? `📄 Code:\n${bot.code}` : ''}
            `, 'success');
            
            // Reload data
            loadBots();
            loadStats();
            
            // Clear inputs
            document.getElementById('botRequirements').value = '';
            document.getElementById('botName').value = '';
        } else {
            showResult(resultDiv, `❌ Error: ${data.message || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        showResult(resultDiv, `❌ Error: ${error.message}`, 'error');
    }
    
    btn.disabled = false;
    btn.textContent = '🤖 Create Bot';
}

// ============================================
// 8. LEARN FROM TEXT
// ============================================

async function learnText() {
    const text = document.getElementById('learnText').value.trim();
    const category = document.getElementById('learnCategory').value;
    const source = document.getElementById('learnSource').value.trim();
    const resultDiv = document.getElementById('learnResult');
    const btn = document.getElementById('learnBtn');
    
    if (!text) {
        showResult(resultDiv, '❌ Please enter text to learn', 'error');
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Learning...';
    resultDiv.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/learn`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                category: category,
                source: source || 'user_input'
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showResult(resultDiv, `
✅ Learning successful!

📚 Category: ${data.category || 'general'}
📖 Source: ${data.source || 'user_input'}
📝 Learned: ${data.text || text.substring(0, 200) + '...'}

The AI has learned this information and will use it in future tasks.
            `, 'success');
            
            // Reload data
            loadStats();
            
            // Clear inputs
            document.getElementById('learnText').value = '';
            document.getElementById('learnSource').value = '';
        } else {
            showResult(resultDiv, `❌ Error: ${data.message || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        showResult(resultDiv, `❌ Error: ${error.message}`, 'error');
    }
    
    btn.disabled = false;
    btn.textContent = '📚 Learn';
}

// ============================================
// 9. UTILITY FUNCTIONS
// ============================================

function showResult(container, message, type = 'success') {
    container.className = type;
    container.textContent = message;
    container.style.display = 'block';
}

function displayError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="error-state">
            <p>❌ ${message}</p>
        </div>
    `;
}

// ============================================
// 10. KEYBOARD SHORTCUTS
// ============================================

document.getElementById('taskInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        e.preventDefault();
        processTask();
    }
});

document.getElementById('learnText').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        e.preventDefault();
        learnText();
    }
});

document.getElementById('botRequirements').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        e.preventDefault();
        createBot();
    }
});

// ============================================
// 11. EXPOSE FUNCTIONS TO GLOBAL SCOPE
// ============================================

window.processTask = processTask;
window.createBot = createBot;
window.learnText = learnText;
