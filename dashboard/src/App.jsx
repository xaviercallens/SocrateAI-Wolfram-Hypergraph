import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, DollarSign, Hexagon, Server, Database, TrendingUp, Clock, Zap
} from 'lucide-react';
import { 
  LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar 
} from 'recharts';

// Mock data based on the real GCP batch_status.json to simulate Data Lake fetching
const mockData = {
  status: "RUNNING",
  current_step: 3774,
  elapsed_seconds: 1901.32,
  duration_seconds: 3600.0,
  progress_pct: 52.8,
  unique_hashes: 1,
  latest_step_record: {
    step: 3774,
    elapsed_sec: 1901.32,
    remaining_sec: 1698.68,
    non_zero_edges: 48,
    masked_sum: 1616.0,
    unmasked_sum: 641632.0,
    top_eigenvalues: [400.0, 1.0, 0.9239, 0.9239, 0.7071, 0.7071, 0.3827, 0.3827],
    vram_mb: 8.14,
    hash: "3fc347341564714feb024f2f4cc0b5fa",
    is_pruned: true
  },
  cost_summary: {
    region: "us-central1",
    elapsed_seconds: 1901.32,
    elapsed_hours: 0.528,
    hourly_burn_rate_usd: 0.1844,
    total_cost_usd: 0.0973,
    remaining_budget_usd: 99.9027,
    max_remaining_compute_hours: 541.77,
    budget_used_pct: 0.09
  }
};

// Timeseries for charts
const performanceData = Array.from({ length: 20 }).map((_, i) => ({
  time: `T-${20-i}m`,
  vram: 8.1 + Math.random() * 0.1,
  edges: 48,
  cost: 0.05 + (i * 0.002)
}));

const eigenData = mockData.latest_step_record.top_eigenvalues.map((val, i) => ({
  index: `λ${i+1}`,
  value: val
}));

export default function App() {
  const [activeTab, setActiveTab] = useState('monitoring');
  const [data, setData] = useState(mockData);

  // In a real scenario, this fetches from the GCP API/Data Lake
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulating live updates
      setData(prev => ({
        ...prev,
        current_step: prev.current_step + 10,
        progress_pct: Math.min(100, prev.progress_pct + 0.1)
      }));
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const tabs = [
    { id: 'monitoring', label: 'Batch Monitoring', icon: Activity },
    { id: 'cost', label: 'Cost & Budget', icon: DollarSign },
    { id: 'geometry', label: 'Geometry & Astrophysics', icon: Hexagon },
  ];

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-title">SocrateAI Dashboard</div>
        <div className="nav-menu">
          {tabs.map(tab => {
            const Icon = tab.icon;
            return (
              <div 
                key={tab.id}
                className={`nav-item ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <Icon size={20} />
                <span>{tab.label}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {activeTab === 'monitoring' && <MonitoringDashboard data={data} />}
            {activeTab === 'cost' && <CostDashboard data={data} />}
            {activeTab === 'geometry' && <GeometryDashboard data={data} />}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

function MonitoringDashboard({ data }) {
  return (
    <div className="fade-in">
      <h1 className="page-title">Batch Simulation Monitoring</h1>
      <p className="page-subtitle">Live tracking of the Wolfram Hypergraph execution.</p>

      <div className="grid-3">
        <div className="glass-panel metric-card">
          <div className="metric-header">
            <span>Status</span>
            <Activity size={18} color="var(--success)" />
          </div>
          <div className="metric-value" style={{ color: 'var(--success)'}}>{data.status}</div>
          <div className="metric-sub">{data.progress_pct.toFixed(1)}% Complete</div>
        </div>

        <div className="glass-panel metric-card">
          <div className="metric-header">
            <span>Current Step</span>
            <TrendingUp size={18} color="var(--accent-primary)" />
          </div>
          <div className="metric-value">{data.current_step.toLocaleString()}</div>
          <div className="metric-sub">{Math.floor(data.duration_seconds - data.elapsed_seconds)}s remaining</div>
        </div>

        <div className="glass-panel metric-card">
          <div className="metric-header">
            <span>VRAM Usage</span>
            <Database size={18} color="var(--warning)" />
          </div>
          <div className="metric-value">{data.latest_step_record.vram_mb.toFixed(2)} MB</div>
          <div className="metric-sub">Highly Optimized</div>
        </div>
      </div>

      <div className="glass-panel" style={{ marginTop: '24px' }}>
        <h3 style={{ marginBottom: '16px', color: 'var(--text-secondary)'}}>System Performance (VRAM over time)</h3>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={performanceData}>
              <defs>
                <linearGradient id="colorVram" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="time" stroke="var(--text-secondary)" />
              <YAxis stroke="var(--text-secondary)" domain={[8, 8.5]} />
              <Tooltip contentStyle={{ backgroundColor: 'var(--panel-bg)', border: 'none', borderRadius: '8px' }} />
              <Area type="monotone" dataKey="vram" stroke="var(--accent-primary)" fillOpacity={1} fill="url(#colorVram)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function CostDashboard({ data }) {
  const { cost_summary } = data;
  return (
    <div className="fade-in">
      <h1 className="page-title">Cost & Budget Dashboard</h1>
      <p className="page-subtitle">Real-time burn rate and budget guardrails monitoring.</p>

      <div className="grid-3">
        <div className="glass-panel metric-card">
          <div className="metric-header">
            <span>Hourly Burn Rate</span>
            <Zap size={18} color="var(--danger)" />
          </div>
          <div className="metric-value">${cost_summary.hourly_burn_rate_usd.toFixed(4)}</div>
          <div className="metric-sub">Region: {cost_summary.region}</div>
        </div>

        <div className="glass-panel metric-card">
          <div className="metric-header">
            <span>Total Cost Incurred</span>
            <DollarSign size={18} color="var(--success)" />
          </div>
          <div className="metric-value">${cost_summary.total_cost_usd.toFixed(4)}</div>
          <div className="metric-sub">Budget Used: {cost_summary.budget_used_pct}%</div>
        </div>

        <div className="glass-panel metric-card">
          <div className="metric-header">
            <span>Remaining Budget</span>
            <Clock size={18} color="var(--accent-secondary)" />
          </div>
          <div className="metric-value">${cost_summary.remaining_budget_usd.toFixed(2)}</div>
          <div className="metric-sub">~{cost_summary.max_remaining_compute_hours.toFixed(0)} hours left</div>
        </div>
      </div>

      <div className="glass-panel" style={{ marginTop: '24px' }}>
        <h3 style={{ marginBottom: '16px', color: 'var(--text-secondary)'}}>Cumulative Cost Incurred</h3>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="time" stroke="var(--text-secondary)" />
              <YAxis stroke="var(--text-secondary)" />
              <Tooltip contentStyle={{ backgroundColor: 'var(--panel-bg)', border: 'none', borderRadius: '8px' }} />
              <Line type="monotone" dataKey="cost" stroke="var(--success)" strokeWidth={3} dot={{ r: 4, fill: 'var(--success)' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function GeometryDashboard({ data }) {
  const { latest_step_record } = data;
  return (
    <div className="fade-in">
      <h1 className="page-title">Geometry & Astrophysics</h1>
      <p className="page-subtitle">Topological invariants and graph spectrum for continuum limit analysis.</p>

      <div className="grid-2">
        <div className="glass-panel metric-card">
          <div className="metric-header">
            <span>Non-Zero Edges (Invariant)</span>
            <Hexagon size={18} color="var(--accent-primary)" />
          </div>
          <div className="metric-value">{latest_step_record.non_zero_edges}</div>
          <div className="metric-sub">Stable limit reached</div>
        </div>

        <div className="glass-panel metric-card">
          <div className="metric-header">
            <span>Graph State Space</span>
            <Server size={18} color="var(--warning)" />
          </div>
          <div className="metric-value">{data.unique_hashes} State(s)</div>
          <div className="metric-sub">Isomorphic Pruning Active</div>
        </div>
      </div>

      <div className="grid-2" style={{ marginTop: '24px' }}>
        <div className="glass-panel">
          <h3 style={{ marginBottom: '16px', color: 'var(--text-secondary)'}}>Adjacency Spectral Analysis (Top Eigenvalues)</h3>
          <div className="chart-container" style={{ height: '250px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={eigenData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="index" stroke="var(--text-secondary)" />
                <YAxis stroke="var(--text-secondary)" />
                <Tooltip contentStyle={{ backgroundColor: 'var(--bg-color)', border: '1px solid var(--panel-border)', borderRadius: '8px' }} cursor={{fill: 'rgba(255,255,255,0.05)'}} />
                <Bar dataKey="value" fill="var(--accent-secondary)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel">
          <h3 style={{ marginBottom: '16px', color: 'var(--text-secondary)'}}>Masking Engine Efficiency</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '24px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', color: 'var(--text-primary)' }}>
                <span>Unmasked Tensor Sum</span>
                <span style={{ fontFamily: 'Outfit' }}>{latest_step_record.unmasked_sum.toLocaleString()}</span>
              </div>
              <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: '100%', height: '100%', background: 'var(--danger)' }}></div>
              </div>
            </div>
            
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', color: 'var(--text-primary)' }}>
                <span>Hadamard Masked Sum (Actual)</span>
                <span style={{ fontFamily: 'Outfit' }}>{latest_step_record.masked_sum.toLocaleString()}</span>
              </div>
              <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: `${(latest_step_record.masked_sum / latest_step_record.unmasked_sum) * 100 * 100}%`, minWidth: '5%', height: '100%', background: 'var(--success)' }}></div>
              </div>
            </div>
          </div>
          <p style={{ marginTop: '24px', fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
            The Phase 0 Hadamard masking effectively suppresses exponential state space saturation. The unmasked calculation explodes, while the topological mask limits edges and maintains memory stability at 8.14 MB.
          </p>
        </div>
      </div>
    </div>
  );
}
