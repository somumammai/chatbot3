/* =====================================================
   SkillBot — Frontend Chat Controller
   Handles: API calls, message rendering, markdown,
            Q&A accordion, theme, sidebar, follow-ups
   ===================================================== */

'use strict';

// =====================================================
//  CONFIG
// =====================================================
const API_BASE = 'http://localhost:5000/api';

const DAILY_TIPS = [
    "Use the STAR method (Situation, Task, Action, Result) for all behavioral questions.",
    "Research the company's core values before every interview — align your answers to them.",
    "Practice coding problems out loud. Interviewers evaluate your thought process, not just the answer.",
    "For aptitude tests, eliminate wrong answers first — saves valuable time.",
    "Prepare 3 smart questions to ask the interviewer at the end. It shows genuine interest.",
    "Body language matters — sit upright, maintain eye contact, and smile naturally.",
    "A firm, confident handshake (or a warm virtual greeting) sets a positive first impression.",
    "Quantify your achievements: '20% improvement' is more compelling than 'I improved things'.",
    "Practice active listening — summarize what you heard before answering behavioral questions.",
    "For technical rounds: Think aloud, write clean code, and always discuss time/space complexity."
];

// =====================================================
//  STATE
// =====================================================
let isDarkTheme = true;
let chatHistory = [];
let isSending = false;

// =====================================================
//  DOM REFERENCES
// =====================================================
const themeToggle = document.getElementById('themeToggle');
const themeToggleMobile = document.getElementById('themeToggleMobile');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const sidebarToggle = document.getElementById('sidebarToggle');
const messagesContainer = document.getElementById('messagesContainer');
const messagesList = document.getElementById('messagesList');
const welcomeScreen = document.getElementById('welcomeScreen');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const randomBtn = document.getElementById('randomBtn');
const followUpChips = document.getElementById('followUpChips');
const newChatBtn = document.getElementById('newChatBtn');
const dailyTipEl = document.getElementById('dailyTip').querySelector('.tip-text');

// =====================================================
//  INITIALIZATION
// =====================================================
function init() {
    // Load saved theme
    const savedTheme = localStorage.getItem('skillbot-theme') || 'dark';
    setTheme(savedTheme);

    // Set daily tip
    const tipIndex = new Date().getDate() % DAILY_TIPS.length;
    dailyTipEl.textContent = DAILY_TIPS[tipIndex];

    // Bind events
    bindEvents();

    // Focus input on desktop
    if (window.innerWidth > 768) {
        chatInput.focus();
    }
}

// =====================================================
//  EVENT BINDING
// =====================================================
function bindEvents() {
    // Theme toggle
    [themeToggle, themeToggleMobile].forEach(btn => {
        btn.addEventListener('click', () => {
            setTheme(isDarkTheme ? 'light' : 'dark');
        });
    });

    // Sidebar toggle (mobile)
    sidebarToggle.addEventListener('click', toggleSidebar);
    sidebarOverlay.addEventListener('click', closeSidebar);

    // Send button
    sendBtn.addEventListener('click', handleSend);

    // Textarea keyboard
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    // Auto-resize textarea
    chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 160) + 'px';
    });

    // Random question button
    randomBtn.addEventListener('click', handleRandomQuestion);

    // New chat button
    newChatBtn.addEventListener('click', clearChat);

    // Quick links (sidebar)
    document.querySelectorAll('.quick-link').forEach(link => {
        link.addEventListener('click', () => {
            sendMessage(link.dataset.query);
            closeSidebar();
        });
    });

    // Company chips (sidebar)
    document.querySelectorAll('.company-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            sendMessage(chip.dataset.query);
            closeSidebar();
        });
    });

    // Suggestion cards (welcome screen)
    document.querySelectorAll('.suggestion-card').forEach(card => {
        card.addEventListener('click', () => {
            sendMessage(card.dataset.query);
        });
    });
}

// =====================================================
//  THEME
// =====================================================
function setTheme(theme) {
    isDarkTheme = theme === 'dark';
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('skillbot-theme', theme);
}

// =====================================================
//  SIDEBAR
// =====================================================
function toggleSidebar() {
    sidebar.classList.toggle('open');
    sidebarOverlay.classList.toggle('show');
}

function closeSidebar() {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('show');
}

// =====================================================
//  CLEAR CHAT
// =====================================================
function clearChat() {
    chatHistory = [];
    messagesList.innerHTML = '';
    followUpChips.innerHTML = '';
    welcomeScreen.style.display = 'flex';
    chatInput.value = '';
    chatInput.style.height = 'auto';
}

// =====================================================
//  SEND HANDLER
// =====================================================
function handleSend() {
    const text = chatInput.value.trim();
    if (!text || isSending) return;
    sendMessage(text);
}

function sendMessage(text) {
    if (!text || isSending) return;

    // Hide welcome screen
    welcomeScreen.style.display = 'none';

    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // Clear follow-up chips
    followUpChips.innerHTML = '';

    // Append user message
    appendUserMessage(text);

    // Show typing indicator
    const typingId = showTypingIndicator();

    // Call API
    isSending = true;
    sendBtn.disabled = true;

    fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
    .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    })
    .then(data => {
        removeTypingIndicator(typingId);
        if (data.success && data.response) {
            appendBotMessage(data.response);
        } else {
            appendBotMessage({
                content: "⚠️ Sorry, I couldn't process that. Please try again.",
                type: 'error',
                follow_up: [],
                items: []
            });
        }
    })
    .catch(err => {
        removeTypingIndicator(typingId);
        console.error('API Error:', err);
        appendBotMessage({
            content: "❌ **Connection Error**\n\nI couldn't reach the backend server. Please make sure the Python server is running at `http://localhost:5000`.\n\nRun: `python app.py` in the chatbot directory.",
            type: 'error',
            follow_up: [],
            items: []
        });
    })
    .finally(() => {
        isSending = false;
        sendBtn.disabled = false;
        chatInput.focus();
    });
}

// =====================================================
//  RANDOM QUESTION
// =====================================================
function handleRandomQuestion() {
    if (isSending) return;

    welcomeScreen.style.display = 'none';
    followUpChips.innerHTML = '';

    const typingId = showTypingIndicator();
    isSending = true;
    sendBtn.disabled = true;

    fetch(`${API_BASE}/random-question`)
    .then(res => res.json())
    .then(data => {
        removeTypingIndicator(typingId);

        // Display a random question as bot message
        const qItem = data.question;
        const categoryLabel = data.category || 'General';
        const badgeClass = getCategoryBadgeClass(data.category);

        const fakeResponse = {
            content: `## 🎲 Random Interview Question\n\n<span class="category-badge ${badgeClass}">${categoryLabel} — ${data.subcategory}</span>`,
            type: 'random',
            follow_up: ["Another random question", "More questions like this", "Aptitude practice", "Technical questions"],
            items: [qItem]
        };

        appendBotMessage(fakeResponse);
    })
    .catch(err => {
        removeTypingIndicator(typingId);
        appendBotMessage({
            content: "❌ Couldn't fetch a random question. Please check the backend.",
            type: 'error',
            follow_up: [],
            items: []
        });
    })
    .finally(() => {
        isSending = false;
        sendBtn.disabled = false;
    });
}

function getCategoryBadgeClass(category) {
    const map = {
        'Soft Skills': 'badge-soft',
        'Aptitude': 'badge-aptitude',
        'Communication': 'badge-communication',
        'Technical': 'badge-technical'
    };
    return map[category] || 'badge-info';
}

// =====================================================
//  MESSAGE RENDERING
// =====================================================
function appendUserMessage(text) {
    const initials = 'YOU';
    const el = document.createElement('div');
    el.className = 'message user';
    el.innerHTML = `
        <div class="message-avatar">${initials}</div>
        <div class="message-content-wrapper">
            <div class="message-bubble">${escapeHtml(text)}</div>
        </div>
    `;
    messagesList.appendChild(el);
    scrollToBottom();
    chatHistory.push({ role: 'user', content: text });
}

function appendBotMessage(response) {
    const el = document.createElement('div');
    el.className = 'message bot';

    const avatarSVG = `<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="48" height="48" rx="12" fill="url(#mg1)"/>
        <path d="M14 24c0-5.5 4.5-10 10-10s10 4.5 10 10-4.5 10-10 10" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M24 24l-6 3 6-13 6 13-6-3z" fill="white"/>
        <defs><linearGradient id="mg1" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse"><stop stop-color="#6C63FF"/><stop offset="1" stop-color="#3ECFCF"/></linearGradient></defs>
    </svg>`;

    // Render main markdown content
    let mainHtml = renderMarkdown(response.content || '');

    // Render Q&A items as accordion cards
    let itemsHtml = '';
    if (response.items && response.items.length > 0) {
        response.items.forEach((item, idx) => {
            if (!item || (!item.q && !item.question)) return;

            const question = item.q || item.question || '';
            const answer = item.a || item.answer || '';
            const tip = item.tip || '';
            const companies = item.companies || [];

            const companyTags = companies.slice(0, 4).map(c =>
                `<span class="company-tag">${escapeHtml(c)}</span>`
            ).join('');

            const answerId = `answer-${Date.now()}-${idx}`;

            itemsHtml += `
                <div class="qa-item">
                    <button class="qa-question" onclick="toggleAnswer('${answerId}')">
                        <span class="qa-question-text">${escapeHtml(question)}</span>
                        <span class="qa-toggle">View Answer</span>
                    </button>
                    <div class="qa-answer" id="${answerId}">
                        <div>${renderMarkdown(answer)}</div>
                        ${(tip || companyTags) ? `
                        <div class="qa-meta">
                            ${tip ? `<div class="qa-tip">${escapeHtml(tip)}</div>` : ''}
                        </div>
                        ${companyTags ? `<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:5px;">${companyTags}</div>` : ''}
                        ` : ''}
                    </div>
                </div>
            `;
        });
    }

    el.innerHTML = `
        <div class="message-avatar">${avatarSVG}</div>
        <div class="message-content-wrapper">
            <div class="message-bubble">
                ${mainHtml}
                ${itemsHtml}
            </div>
        </div>
    `;

    messagesList.appendChild(el);
    scrollToBottom();

    // Render follow-up chips
    if (response.follow_up && response.follow_up.length > 0) {
        renderFollowUpChips(response.follow_up);
    }

    chatHistory.push({ role: 'bot', content: response.content });
}

// =====================================================
//  ACCORDION TOGGLE
// =====================================================
window.toggleAnswer = function(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.toggle('open');

    // Update toggle label
    const btn = el.previousElementSibling;
    const toggleLabel = btn.querySelector('.qa-toggle');
    if (toggleLabel) {
        toggleLabel.textContent = el.classList.contains('open') ? 'Hide Answer' : 'View Answer';
    }
};

// =====================================================
//  FOLLOW-UP CHIPS
// =====================================================
function renderFollowUpChips(suggestions) {
    followUpChips.innerHTML = '';
    suggestions.forEach(text => {
        const chip = document.createElement('button');
        chip.className = 'follow-up-chip';
        chip.textContent = text;
        chip.addEventListener('click', () => sendMessage(text));
        followUpChips.appendChild(chip);
    });
}

// =====================================================
//  TYPING INDICATOR
// =====================================================
function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    const el = document.createElement('div');
    el.className = 'message bot';
    el.id = id;

    const avatarSVG = `<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="48" height="48" rx="12" fill="url(#tg1)"/>
        <path d="M14 24c0-5.5 4.5-10 10-10s10 4.5 10 10" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
        <defs><linearGradient id="tg1" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse"><stop stop-color="#6C63FF"/><stop offset="1" stop-color="#3ECFCF"/></linearGradient></defs>
    </svg>`;

    el.innerHTML = `
        <div class="message-avatar">${avatarSVG}</div>
        <div class="message-content-wrapper">
            <div class="message-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;
    messagesList.appendChild(el);
    scrollToBottom();
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// =====================================================
//  MARKDOWN RENDERER (lightweight, no dependencies)
// =====================================================
function renderMarkdown(text) {
    if (!text) return '';

    let html = text;

    // Escape HTML first (except for already-embedded HTML like spans)
    // We'll handle this carefully by processing line by line

    // Code blocks (```...```) — handle first before inline code
    html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
    });

    // Inline code
    html = html.replace(/`([^`\n]+)`/g, '<code>$1</code>');

    // Bold + Italic
    html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    // Bold
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic
    html = html.replace(/\*([^*\n]+)\*/g, '<em>$1</em>');

    // H2 headings
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    // H3 headings
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');

    // Horizontal rules
    html = html.replace(/^---+$/gm, '<hr>');

    // Unordered lists
    html = html.replace(/^\s*[-*+] (.+)$/gm, '<li>$1</li>');
    // Wrap consecutive <li> in <ul>
    html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>');

    // Ordered lists (simple: "1. ...")
    html = html.replace(/^\d+\. (.+)$/gm, '<oli>$1</oli>');
    html = html.replace(/((?:<oli>.*<\/oli>\n?)+)/g, (match) => {
        return '<ol>' + match.replace(/<oli>/g, '<li>').replace(/<\/oli>/g, '</li>') + '</ol>';
    });

    // Line breaks (double newlines → paragraphs; single → <br>)
    const lines = html.split('\n');
    const blocks = [];
    let currentBlock = [];

    for (const line of lines) {
        const stripped = line.trim();
        if (stripped === '') {
            if (currentBlock.length > 0) {
                blocks.push(currentBlock.join('\n'));
                currentBlock = [];
            }
        } else {
            currentBlock.push(line);
        }
    }
    if (currentBlock.length > 0) {
        blocks.push(currentBlock.join('\n'));
    }

    html = blocks.map(block => {
        // If block is already a block element, don't wrap
        const isBlock = block.trim().match(/^<(h[1-6]|ul|ol|li|pre|hr|div|table)/i);
        if (isBlock) return block;
        // Wrap in paragraph, replace single newlines with <br>
        return `<p>${block.replace(/\n/g, '<br>')}</p>`;
    }).join('\n');

    // Allow certain HTML tags that we specifically inject
    // (like <span class="category-badge"...>) — they won't be escaped

    return html;
}

// =====================================================
//  UTILITIES
// =====================================================
function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function scrollToBottom() {
    requestAnimationFrame(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
}

// =====================================================
//  START
// =====================================================
document.addEventListener('DOMContentLoaded', init);
