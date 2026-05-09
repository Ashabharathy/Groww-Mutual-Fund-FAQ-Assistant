import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  Send, Bot, User, ShieldAlert, ExternalLink, Calendar,
  Trash2, SplitSquareHorizontal, Settings, Sun, Moon, LogOut,
  BarChart2, HelpCircle, Database, ChevronRight, X, Plus,
  MessageSquare,
} from 'lucide-react';

const SUGGESTIONS = [
  "Who is the fund manager of Tata Small Cap Fund?",
  "Expense ratio of Tata ELSS Fund?",
  "Exit load for Tata Digital India Fund?",
  "Minimum SIP for Tata Ethical Fund?",
];

// Use environment variable for API base URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const INITIAL_MSG = {
  role: 'assistant',
  content: 'Hello! I am your Tata Mutual Fund FAQ Assistant. I provide strictly factual information based on official documents. How can I help you today?',
};

// ── Mock user ──────────────────────────────────────────────
const MOCK_USER = {
  name: 'Asha',
  email: 'ashabharathy@gmail.com',
  avatar: 'AB',
  plan: 'Pro Investor',
};

export default function App() {
  // Theme
  const [theme, setTheme] = useState('dark'); // 'dark' | 'light'

  // Sidebar
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [settingsOpen, setSettingsOpen] = useState(false);

  // Dual chat
  const [dualMode, setDualMode] = useState(false);

  // Chat A
  const [messagesA, setMessagesA] = useState([{ ...INITIAL_MSG }]);
  const [inputA, setInputA] = useState('');
  const [loadingA, setLoadingA] = useState(false);
  const chatEndA = useRef(null);

  // Chat B (dual mode)
  const [messagesB, setMessagesB] = useState([{ ...INITIAL_MSG }]);
  const [inputB, setInputB] = useState('');
  const [loadingB, setLoadingB] = useState(false);
  const chatEndB = useRef(null);

  useEffect(() => {
    chatEndA.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messagesA, loadingA]);

  useEffect(() => {
    chatEndB.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messagesB, loadingB]);

  // Apply theme to root
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const parseContent = (content) => {
    const lines = content.split('\n');
    let answer = [], source = null, date = null;
    lines.forEach((line) => {
      if (line.startsWith('Source:'))                    source = line.replace('Source:', '').trim();
      else if (line.startsWith('Last updated from sources:')) date = line.replace('Last updated from sources:', '').trim();
      else if (line.trim())                              answer.push(line);
    });
    return { text: answer.join('\n'), source, date };
  };

  const sendMessage = async (query, setMessages, setInput, setLoading) => {
    if (!query.trim()) return;
    setMessages((prev) => [...prev, { role: 'user', content: query }]);
    setInput('');
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE_URL}/query`, { query });
      setMessages((prev) => [...prev, { role: 'assistant', content: res.data.answer }]);
    } catch {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: "I'm sorry, I encountered an error connecting to the backend. Please ensure the FastAPI server is running.",
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSendA = (text) => sendMessage(text || inputA, setMessagesA, setInputA, setLoadingA);
  const handleSendB = (text) => sendMessage(text || inputB, setMessagesB, setInputB, setLoadingB);

  const clearChat = (which) => {
    if (which === 'A') setMessagesA([{ ...INITIAL_MSG }]);
    else               setMessagesB([{ ...INITIAL_MSG }]);
  };

  // ── Chat panel component ──────────────────────────────────
  const ChatPanel = ({ messages, input, setInput, loading, onSend, onClear, label, chatEndRef }) => (
    <div className="chat-panel">
      {/* Panel header */}
      <div className="panel-header">
        <div className="panel-title">
          <MessageSquare size={13} />
          {label}
        </div>
        <button className="icon-btn" onClick={onClear} title="Clear chat">
          <Trash2 size={14} />
        </button>
      </div>

      {/* Messages */}
      <div className="chat-window">
        {messages.map((msg, idx) => {
          const { text, source, date } =
            msg.role === 'assistant'
              ? parseContent(msg.content)
              : { text: msg.content, source: null, date: null };
          return (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="msg-header">
                <span className="icon-wrap">
                  {msg.role === 'assistant' ? <Bot size={12} /> : <User size={12} />}
                </span>
                {msg.role === 'assistant' ? 'Factual Assistant' : 'You'}
              </div>
              <div className="msg-content">{text}</div>
              {source && (
                <a href={source} target="_blank" rel="noopener noreferrer" className="source-link">
                  <ExternalLink size={11} /> View Source Document
                </a>
              )}
              {date && (
                <div className="footer-text">
                  <Calendar size={10} /> Verified on: {date}
                </div>
              )}
            </div>
          );
        })}
        {loading && (
          <div className="message assistant loading">
            <div className="msg-header">
              <span className="icon-wrap"><Bot size={12} /></span>
              Factual Assistant
            </div>
            <div className="typing-dots"><span /><span /><span /></div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Suggestions */}
      <div className="suggestions">
        {SUGGESTIONS.map((s, i) => (
          <button key={i} className="suggestion-btn" onClick={() => onSend(s)} disabled={loading}>{s}</button>
        ))}
      </div>

      {/* Input */}
      <div className="input-area">
        <div className="input-wrap">
          <input
            type="text"
            placeholder="Ask a factual question about Tata Mutual Funds..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && onSend()}
            disabled={loading}
            autoComplete="off"
          />
        </div>
        <button className="send-btn" onClick={() => onSend()} disabled={loading || !input.trim()}>
          <Send size={18} strokeWidth={2.5} />
        </button>
      </div>
    </div>
  );

  return (
    <div className={`page-root theme-${theme}`}>
      <div className="card-wrapper">
        <div className="app-shell">

          {/* ══════════════ SIDEBAR ══════════════ */}
          <aside className={`sidebar ${sidebarOpen ? 'open' : 'collapsed'}`}>

            {/* Top: logo + collapse */}
            <div className="sb-top">
              <div className="sb-logo">
                {/* Groww logo — circle with blue top / teal bottom split by zigzag */}
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style={{flexShrink:0}}>
                  <circle cx="16" cy="16" r="16" fill="#5B5BD6"/>
                  <clipPath id="circ">
                    <circle cx="16" cy="16" r="16"/>
                  </clipPath>
                  <g clipPath="url(#circ)">
                    <path d="M0 32 L0 19 L7 13 L12 18 L16 14 L21 19 L32 11 L32 32 Z" fill="#00D09C"/>
                  </g>
                </svg>
                {sidebarOpen && <span className="sb-logo-text">Groww MF Saathi</span>}
              </div>
              <button className="sb-collapse-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
                <ChevronRight size={15} style={{ transform: sidebarOpen ? 'rotate(180deg)' : 'none', transition: 'transform 0.3s' }} />
              </button>
            </div>

            {/* User card */}
            <div className="sb-user-card">
              <div className="sb-avatar">{MOCK_USER.avatar}</div>
              {sidebarOpen && (
                <div className="sb-user-info">
                  <div className="sb-user-name">{MOCK_USER.name}</div>
                  <div className="sb-user-email">{MOCK_USER.email}</div>
                  <span className="sb-plan-badge">{MOCK_USER.plan}</span>
                </div>
              )}
            </div>

            <div className="sb-divider" />

            {/* Main actions */}
            <nav className="sb-nav">
              <button
                className={`sb-nav-item ${!dualMode ? 'active' : ''}`}
                onClick={() => setDualMode(false)}
                title="Single Chat"
              >
                <MessageSquare size={16} />
                {sidebarOpen && <span>Single Chat</span>}
              </button>

              <button
                className={`sb-nav-item ${dualMode ? 'active' : ''}`}
                onClick={() => setDualMode(true)}
                title="Dual Chat"
              >
                <SplitSquareHorizontal size={16} />
                {sidebarOpen && <span>Dual Chat</span>}
              </button>

              <button
                className="sb-nav-item"
                onClick={() => { clearChat('A'); clearChat('B'); }}
                title="Clear All Chats"
              >
                <Trash2 size={16} />
                {sidebarOpen && <span>Clear Chat</span>}
              </button>

              <button
                className="sb-nav-item"
                onClick={() => setSettingsOpen(true)}
                title="Settings"
              >
                <Settings size={16} />
                {sidebarOpen && <span>Settings</span>}
              </button>
            </nav>

            {/* Spacer */}
            <div style={{ flex: 1 }} />

            <div className="sb-divider" />

            {/* Bottom nav: Market Trends, Investment FAQ, Historic Data */}
            <nav className="sb-nav sb-bottom-nav">
              {sidebarOpen && <div className="sb-section-label">Explore</div>}

              <button className="sb-nav-item" title="Market Trends">
                <BarChart2 size={16} />
                {sidebarOpen && <span>Market Trends</span>}
              </button>

              <button className="sb-nav-item" title="Investment FAQ">
                <HelpCircle size={16} />
                {sidebarOpen && <span>Investment FAQ</span>}
              </button>

              <button className="sb-nav-item" title="Historic Data">
                <Database size={16} />
                {sidebarOpen && <span>Historic Data</span>}
              </button>

              <div className="sb-divider" />

              <button className="sb-nav-item sb-logout" title="Sign Out">
                <LogOut size={16} />
                {sidebarOpen && <span>Sign Out</span>}
              </button>
            </nav>
          </aside>

          {/* ══════════════ MAIN AREA ══════════════ */}
          <div className="main-area">

            {/* ── Top header bar ── */}
            <header>
              <div className="header-left">
                <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="16" cy="16" r="16" fill="#5B5BD6"/>
                  <clipPath id="circ2">
                    <circle cx="16" cy="16" r="16"/>
                  </clipPath>
                  <g clipPath="url(#circ2)">
                    <path d="M0 32 L0 19 L7 13 L12 18 L16 14 L21 19 L32 11 L32 32 Z" fill="#00D09C"/>
                  </g>
                </svg>
                <div className="status-dot">Live</div>
                {dualMode && <span className="dual-badge"><SplitSquareHorizontal size={11} /> Dual Mode</span>}
              </div>
              <div className="header-right">
                <div className="disclaimer-badge">
                  <ShieldAlert size={12} />
                  Facts only · No investment advice
                </div>
              </div>
            </header>

            {/* ── Chat area ── */}
            <div className={`chats-area ${dualMode ? 'dual' : 'single'}`}>
              <ChatPanel
                messages={messagesA}
                input={inputA}
                setInput={setInputA}
                loading={loadingA}
                onSend={handleSendA}
                onClear={() => clearChat('A')}
                label={dualMode ? 'Chat A' : 'Chat'}
                chatEndRef={chatEndA}
              />
              {dualMode && (
                <ChatPanel
                  messages={messagesB}
                  input={inputB}
                  setInput={setInputB}
                  loading={loadingB}
                  onSend={handleSendB}
                  onClear={() => clearChat('B')}
                  label="Chat B"
                  chatEndRef={chatEndB}
                />
              )}
            </div>
          </div>
        </div>
      </div>

      {/* ══════════════ SETTINGS MODAL ══════════════ */}
      {settingsOpen && (
        <div className="modal-overlay" onClick={() => setSettingsOpen(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-title"><Settings size={16} /> Settings</div>
              <button className="icon-btn" onClick={() => setSettingsOpen(false)}><X size={16} /></button>
            </div>

            <div className="modal-section-label">Appearance</div>
            <div className="theme-toggle-row">
              <button
                className={`theme-btn ${theme === 'dark' ? 'active' : ''}`}
                onClick={() => setTheme('dark')}
              >
                <Moon size={15} /> Dark
              </button>
              <button
                className={`theme-btn ${theme === 'light' ? 'active' : ''}`}
                onClick={() => setTheme('light')}
              >
                <Sun size={15} /> Light
              </button>
            </div>

            <div className="modal-section-label">Chat Mode</div>
            <div className="theme-toggle-row">
              <button
                className={`theme-btn ${!dualMode ? 'active' : ''}`}
                onClick={() => { setDualMode(false); setSettingsOpen(false); }}
              >
                <MessageSquare size={15} /> Single
              </button>
              <button
                className={`theme-btn ${dualMode ? 'active' : ''}`}
                onClick={() => { setDualMode(true); setSettingsOpen(false); }}
              >
                <SplitSquareHorizontal size={15} /> Dual
              </button>
            </div>

            <div className="modal-section-label">Account</div>
            <div className="modal-user-row">
              <div className="sb-avatar sm">{MOCK_USER.avatar}</div>
              <div>
                <div className="sb-user-name">{MOCK_USER.name}</div>
                <div className="sb-user-email">{MOCK_USER.email}</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
