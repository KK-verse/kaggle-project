"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useStore } from '@/store/useStore';
import { 
  Sparkles, 
  TrendingUp, 
  FileText, 
  Briefcase, 
  Map, 
  Plus, 
  AlertTriangle, 
  ArrowLeft,
  Search,
  Filter,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Download,
  Check,
  ChevronRight,
  BookOpen,
  Milestone,
  ExternalLink,
  RefreshCw,
  Info
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const router = useRouter();
  const { 
    activeResumeId, 
    resumeData, 
    careerScore, 
    jobMatches, 
    jobsList, 
    activeRoadmap, 
    optimizedResume, 
    isLoading, 
    error,
    fetchJobsList,
    generateRoadmap,
    optimizeResume,
    resetStore
  } = useStore();

  const [activeTab, setActiveTab] = useState<'dashboard' | 'analysis' | 'jobs' | 'roadmap' | 'optimizer'>('dashboard');
  
  // Job filter states
  const [jobSearch, setJobSearch] = useState('');
  const [jobWorkType, setJobWorkType] = useState('all');
  const [jobLocation, setJobLocation] = useState('all');
  const [jobFresher, setJobFresher] = useState(false);
  const [jobWomen, setJobWomen] = useState(false);
  const [jobDiversity, setJobDiversity] = useState(false);

  // Roadmap target role state
  const [roadmapRole, setRoadmapRole] = useState('');

  // Optimizer states
  const [selectedJobForOpt, setSelectedJobForOpt] = useState<any>(null);
  const [customOptRole, setCustomOptRole] = useState('');
  const [customOptCompany, setCustomOptCompany] = useState('');
  const [customOptJD, setCustomOptJD] = useState('');
  const [optSuccessMsg, setOptSuccessMsg] = useState(false);

  // Redirect to home if no resume is active
  useEffect(() => {
    if (!activeResumeId) {
      router.push('/');
    }
  }, [activeResumeId, router]);

  // Fetch jobs list on mount or when filters change
  useEffect(() => {
    if (activeResumeId) {
      fetchJobsList({
        search: jobSearch,
        location: jobLocation !== 'all' ? jobLocation : undefined,
        work_type: jobWorkType !== 'all' ? jobWorkType : undefined,
        fresher_friendly: jobFresher || undefined,
        women_hiring: jobWomen || undefined,
        diversity_hiring: jobDiversity || undefined
      });
    }
  }, [activeResumeId, jobSearch, jobWorkType, jobLocation, jobFresher, jobWomen, jobDiversity, fetchJobsList]);

  if (!resumeData) {
    return (
      <div className="min-h-screen bg-[#09090b] flex flex-col items-center justify-center gap-4 relative">
        <div className="absolute inset-0 bg-blue-500/5 blur-[100px] pointer-events-none" />
        <AlertTriangle className="w-12 h-12 text-zinc-500 animate-bounce" />
        <div className="text-zinc-300 font-bold text-lg">No Active Session Resume</div>
        <p className="text-zinc-500 text-sm max-w-xs text-center">
          Please upload a resume or select a sandbox candidate to open the dashboard workspace.
        </p>
        <button 
          onClick={() => router.push('/')}
          className="mt-2 px-5 py-2 rounded-xl bg-blue-500 hover:bg-blue-600 text-white font-semibold text-sm transition-all"
        >
          Go to Home Page
        </button>
      </div>
    );
  }

  // Charts data preparation
  const chartData = [
    { name: 'ATS Score', value: resumeData.ats_score, fill: '#3b82f6' },
    { name: 'Quality Score', value: resumeData.quality_score, fill: '#8b5cf6' }
  ];

  const handleGenerateRoadmap = async () => {
    if (!roadmapRole.trim()) return;
    await generateRoadmap(resumeData.id, roadmapRole.trim());
  };

  const handlePrepopulateOptimizer = (match: any) => {
    setSelectedJobForOpt(match);
    setCustomOptRole(match.role);
    setCustomOptCompany(match.company);
    
    // Find job description from jobs list
    const originalJob = jobsList.find(j => j.id === match.job_id);
    setCustomOptJD(originalJob ? originalJob.description : "Analyze and write code to build technical backend and frontend pipelines.");
    setActiveTab('optimizer');
  };

  const handleRunOptimizer = async () => {
    if (!customOptRole || !customOptCompany || !customOptJD) return;
    setOptSuccessMsg(false);
    await optimizeResume(
      resumeData.id,
      selectedJobForOpt?.job_id || null,
      customOptRole,
      customOptCompany,
      customOptJD
    );
    setOptSuccessMsg(true);
  };

  const handleDownloadOriginalPDF = () => {
    if (!resumeData) return;
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    window.open(`${baseUrl}/api/resumes/download/${resumeData.id}`, '_blank');
  };

  const handleDownloadOptimizedPDF = () => {
    if (!optimizedResume) return;
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    window.open(`${baseUrl}${optimizedResume.pdf_url}`, '_blank');
  };



  return (
    <div className="min-h-screen bg-[#09090b] text-[#fafafa] flex flex-col font-sans relative pb-12 select-none">
      {/* Dynamic Background Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[50%] rounded-full bg-blue-500/5 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[50%] rounded-full bg-indigo-500/5 blur-[120px] pointer-events-none" />

      {/* Header Workspace */}
      <header className="w-full max-w-7xl mx-auto px-6 py-5 flex flex-col md:flex-row items-start md:items-center justify-between border-b border-white/5 gap-4 relative z-10">
        <div className="flex items-center gap-3">
          <button 
            onClick={() => { resetStore(); router.push('/'); }}
            className="p-2 rounded-lg bg-zinc-900 border border-white/5 text-zinc-400 hover:text-white hover:border-white/10 active:scale-95 transition-all cursor-pointer"
            title="Return to Home"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-heading font-extrabold text-xl tracking-tight">
                Career<span className="text-blue-500">Pilot</span> Dashboard
              </span>
              <span className="px-2 py-0.5 rounded-full bg-zinc-800 border border-zinc-700 text-[10px] text-zinc-400 uppercase tracking-widest">
                Workspace
              </span>
            </div>
            <p className="text-zinc-500 text-xs mt-0.5">
              Active: <span className="text-zinc-300 font-semibold">{resumeData.name || resumeData.filename}</span>
            </p>
          </div>
        </div>

        {/* Quick Details Bar */}
        <div className="flex items-center gap-4 bg-zinc-900/40 border border-white/5 px-4 py-2 rounded-xl text-xs text-zinc-400 max-w-full overflow-x-auto">
          {resumeData.email && <span>📧 {resumeData.email}</span>}
          {resumeData.phone && <span className="hidden sm:inline">|</span>}
          {resumeData.phone && <span>📞 {resumeData.phone}</span>}
          <span className="hidden sm:inline">|</span>
          <span>ATS: <strong className="text-blue-400">{resumeData.ats_score}/100</strong></span>
        </div>
      </header>

      {/* Main Tab Links */}
      <div className="w-full max-w-7xl mx-auto px-6 mt-6 relative z-10">
        <div className="flex border-b border-white/5 overflow-x-auto whitespace-nowrap scrollbar-none gap-2">
          {[
            { id: 'dashboard', label: 'Dashboard', icon: TrendingUp },
            { id: 'analysis', label: 'Resume Analysis', icon: FileText },
            { id: 'jobs', label: 'Job Matches', icon: Briefcase },
            { id: 'roadmap', label: 'Learning Roadmap', icon: Map },
            { id: 'optimizer', label: 'Resume Optimizer', icon: Sparkles },
          ].map((tab) => {
            const Icon = tab.icon;
            const isSelected = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 px-5 py-3 border-b-2 font-semibold text-sm transition-all duration-200 cursor-pointer ${
                  isSelected 
                    ? 'border-blue-500 text-blue-400 bg-blue-500/5' 
                    : 'border-transparent text-zinc-400 hover:text-zinc-200 hover:bg-white/5'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Panels */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-6 mt-8 relative z-10">
        {isLoading && (
          <div className="absolute inset-0 bg-[#09090b]/80 backdrop-blur-sm flex flex-col items-center justify-center z-50 rounded-2xl gap-3">
            <div className="w-10 h-10 rounded-full border-4 border-blue-500/10 border-t-blue-500 animate-spin" />
            <span className="text-xs text-zinc-400 font-semibold animate-pulse">AI Agent working...</span>
          </div>
        )}

        {/* ERROR MESSAGE DISPLAY */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-sm text-red-400 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
            <div>
              <div className="font-bold">Execution Error</div>
              <p className="text-xs text-zinc-400 mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* 1. DASHBOARD VIEW */}
        {activeTab === 'dashboard' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left/Middle Column */}
            <div className="lg:col-span-2 flex flex-col gap-8">
              
              {/* SWOT Summary Checklist */}
              <div className="glass-card p-6 rounded-2xl border border-white/5 flex flex-col gap-6">
                <div>
                  <h3 className="text-lg font-bold text-white">SWOT Analysis Overview</h3>
                  <p className="text-xs text-zinc-500 mt-0.5">Quick synthesis of strengths, weaknesses, and key actions.</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-xl bg-zinc-900/60 border border-white/5">
                    <span className="text-xs font-bold text-blue-400 uppercase tracking-widest block mb-2">Strengths</span>
                    <ul className="text-xs text-zinc-300 space-y-1.5 list-disc pl-4 leading-relaxed">
                      {resumeData.strengths?.slice(0, 3).map((st, i) => (
                        <li key={i}>{st}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="p-4 rounded-xl bg-zinc-900/60 border border-white/5">
                    <span className="text-xs font-bold text-purple-400 uppercase tracking-widest block mb-2">Weaknesses</span>
                    <ul className="text-xs text-zinc-300 space-y-1.5 list-disc pl-4 leading-relaxed">
                      {resumeData.weaknesses?.slice(0, 3).map((wk, i) => (
                        <li key={i}>{wk}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              {/* Career Readiness Checklist */}
              <div className="glass-card p-6 rounded-2xl border border-white/5 flex flex-col gap-4">
                <div>
                  <h3 className="text-lg font-bold text-white">How to Reach 90+ Score</h3>
                  <p className="text-xs text-zinc-500 mt-0.5">Tailored action checklist from your Career Coach Mentor.</p>
                </div>
                
                <div className="flex flex-col gap-3 mt-2">
                  {careerScore?.action_plan?.map((action, i) => (
                    <div key={i} className="flex items-start gap-3 p-3.5 rounded-xl bg-zinc-900/30 border border-white/5 hover:border-zinc-800 transition-all">
                      <div className="w-5 h-5 rounded-full border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0 bg-blue-500/5 mt-0.5 text-xs font-bold font-mono">
                        {i + 1}
                      </div>
                      <span className="text-sm text-zinc-300 leading-relaxed font-medium">{action}</span>
                    </div>
                  ))}
                  {(!careerScore?.action_plan || careerScore.action_plan.length === 0) && (
                    <div className="text-zinc-500 text-sm text-center py-6">
                      No action plan pre-calculated. Re-upload your resume or evaluate score to generate.
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Right Column: Readiness Score Visual Gauge */}
            <div className="flex flex-col gap-8">
              
              {/* Circular Gauge Card */}
              <div className="glass-card p-8 rounded-2xl border border-white/5 flex flex-col items-center justify-center text-center relative overflow-hidden glow-blue">
                <div className="absolute top-2 right-2 cursor-pointer text-zinc-500 hover:text-zinc-300" title="Calculated from SWOT + Job Matches">
                  <Info className="w-4 h-4" />
                </div>
                
                <span className="text-xs font-bold text-zinc-400 tracking-wider uppercase mb-6">Career Readiness Score</span>
                
                {/* SVG Radial Progress Circle */}
                <div className="relative w-36 h-36 flex items-center justify-center mb-6">
                  {/* Outer glow ring */}
                  <svg className="w-full h-full transform -rotate-90">
                    <circle 
                      cx="72" 
                      cy="72" 
                      r="64" 
                      stroke="rgba(255,255,255,0.02)" 
                      strokeWidth="10" 
                      fill="transparent" 
                    />
                    <circle 
                      cx="72" 
                      cy="72" 
                      r="64" 
                      stroke="url(#blueGradient)" 
                      strokeWidth="10" 
                      fill="transparent" 
                      strokeDasharray="402"
                      strokeDashoffset={402 - (402 * (careerScore?.readiness_score || 70)) / 100}
                      strokeLinecap="round"
                      className="transition-all duration-1000 ease-out"
                    />
                    <defs>
                      <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#3b82f6" />
                        <stop offset="100%" stopColor="#6366f1" />
                      </linearGradient>
                    </defs>
                  </svg>
                  {/* Score text */}
                  <div className="absolute flex flex-col items-center justify-center">
                    <span className="text-4xl font-extrabold text-white tracking-tight">{careerScore?.readiness_score || 70}</span>
                    <span className="text-[10px] font-bold text-zinc-500 tracking-widest uppercase mt-0.5">percent</span>
                  </div>
                </div>

                <div className="flex flex-col items-center">
                  <span className="px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-xs font-bold text-blue-400 mb-4 tracking-wide">
                    {careerScore?.readiness_score && careerScore.readiness_score >= 80 ? 'Industry Ready' : 'Getting Ready'}
                  </span>
                  <p className="text-zinc-400 text-xs leading-relaxed max-w-[240px]">
                    {careerScore?.explanation || "You are currently developing industry readiness. Follow the mentor checklist items to boost your compatibility score."}
                  </p>
                </div>
              </div>

              {/* SWOT Mini-Scores Visuals */}
              <div className="glass-card p-6 rounded-2xl border border-white/5">
                <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-4">Core Criteria Scores</h4>
                
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-xs font-semibold text-zinc-300 mb-1.5">
                      <span>ATS Keyword Match</span>
                      <span className="text-blue-400">{resumeData.ats_score}%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-zinc-800">
                      <div className="h-full rounded-full bg-blue-500 transition-all duration-500" style={{ width: `${resumeData.ats_score}%` }} />
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-xs font-semibold text-zinc-300 mb-1.5">
                      <span>Resume Quality Score</span>
                      <span className="text-purple-400">{resumeData.quality_score}%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-zinc-800">
                      <div className="h-full rounded-full bg-purple-500 transition-all duration-500" style={{ width: `${resumeData.quality_score}%` }} />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 2. RESUME ANALYSIS VIEW */}
        {activeTab === 'analysis' && (
          <div className="flex flex-col gap-8">
            
            {/* Score Comparison Graph */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 glass-card p-6 rounded-2xl border border-white/5 flex flex-col gap-6">
                <div>
                  <h3 className="text-lg font-bold text-white">Resume Scores Comparison</h3>
                  <p className="text-xs text-zinc-500 mt-0.5">visual evaluation of ATS keyword mapping against overall layout structure quality.</p>
                </div>
                <div className="h-[220px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                      <XAxis dataKey="name" stroke="#71717a" fontSize={12} tickLine={false} />
                      <YAxis stroke="#71717a" fontSize={12} domain={[0, 100]} axisLine={false} tickLine={false} />
                      <Tooltip contentStyle={{ backgroundColor: '#18181b', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8, fontSize: 12, color: '#fff' }} />
                      <Bar dataKey="value" radius={[8, 8, 0, 0]} barSize={50} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Score Explanation Details */}
              <div className="glass-card p-6 rounded-2xl border border-white/5 flex flex-col gap-4 justify-between">
                <div>
                  <h4 className="text-sm font-bold text-white mb-2">Analysis Breakdown</h4>
                  <div className="text-xs text-zinc-400 space-y-3 leading-relaxed">
                    <p>
                      <strong>ATS score (Keywords):</strong> Checks if your resume contains the primary keywords related to technical stacks (like Git, databases, API testing) standard for entry roles.
                    </p>
                    <p>
                      <strong>Quality Score (Content):</strong> Evaluates if you have metrics-oriented experience listings, structured project sections, and neat education logs.
                    </p>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <button 
                    onClick={handleDownloadOriginalPDF}
                    className="flex-1 text-center py-2.5 rounded-xl border border-white/5 bg-zinc-900/60 hover:bg-zinc-800 text-zinc-300 text-xs font-semibold hover:text-white transition-all flex items-center justify-center gap-1.5 cursor-pointer"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Download Original PDF</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Strengths / Weaknesses Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="glass-card p-6 rounded-2xl border border-white/5">
                <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-blue-400" />
                  <span>Key Strengths Identified</span>
                </h3>
                <ul className="space-y-3 text-xs text-zinc-400 leading-relaxed">
                  {resumeData.strengths?.map((st, i) => (
                    <li key={i} className="flex gap-2 p-2.5 rounded-lg bg-blue-500/5 border border-blue-500/10">
                      <span className="text-blue-400 font-bold shrink-0">&bull;</span>
                      <span>{st}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="glass-card p-6 rounded-2xl border border-white/5">
                <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
                  <AlertCircle className="w-5 h-5 text-purple-400" />
                  <span>Areas of Improvement (Weaknesses)</span>
                </h3>
                <ul className="space-y-3 text-xs text-zinc-400 leading-relaxed">
                  {resumeData.weaknesses?.map((wk, i) => (
                    <li key={i} className="flex gap-2 p-2.5 rounded-lg bg-purple-500/5 border border-purple-500/10">
                      <span className="text-purple-400 font-bold shrink-0">&bull;</span>
                      <span>{wk}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Missing Keywords & Improvement Suggestions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Missing keywords tag list */}
              <div className="glass-card p-6 rounded-2xl border border-white/5 md:col-span-1">
                <h3 className="text-sm font-bold text-white mb-4">Recommended Keywords</h3>
                <div className="flex flex-wrap gap-2">
                  {resumeData.missing_keywords?.map((kw, i) => (
                    <span 
                      key={i}
                      className="px-2.5 py-1 rounded-lg bg-zinc-900 border border-white/5 text-xs text-zinc-300 font-medium hover:border-zinc-700 transition-all cursor-default"
                    >
                      {kw}
                    </span>
                  ))}
                  {(!resumeData.missing_keywords || resumeData.missing_keywords.length === 0) && (
                    <div className="text-zinc-500 text-xs py-4">No missing keywords detected. Good job!</div>
                  )}
                </div>
              </div>

              {/* Suggestions bullets */}
              <div className="glass-card p-6 rounded-2xl border border-white/5 md:col-span-2">
                <h3 className="text-sm font-bold text-white mb-4">Coach suggestions</h3>
                <ul className="space-y-3 text-xs text-zinc-400 leading-relaxed">
                  {resumeData.suggestions?.map((sug, i) => (
                    <li key={i} className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-white/5 transition-all">
                      <div className="w-5 h-5 rounded-full bg-zinc-800 border border-white/5 text-[10px] text-zinc-400 flex items-center justify-center shrink-0">
                        {i+1}
                      </div>
                      <span>{sug}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* 3. SMART JOB MATCH VIEW */}
        {activeTab === 'jobs' && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            
            {/* Sidebar Filter Panel */}
            <div className="lg:col-span-1 glass-card p-6 rounded-2xl border border-white/5 flex flex-col gap-6 h-fit">
              <div className="flex items-center gap-2 border-b border-white/5 pb-3">
                <Filter className="w-4 h-4 text-blue-500" />
                <h3 className="font-bold text-sm text-white">Filter Job Openings</h3>
              </div>
              
              {/* Search text query */}
              <div className="flex flex-col gap-2">
                <label className="text-xs font-semibold text-zinc-400">Search Keywords</label>
                <div className="relative">
                  <Search className="absolute left-3 top-2.5 w-4 h-4 text-zinc-500" />
                  <input 
                    type="text"
                    value={jobSearch}
                    onChange={(e) => setJobSearch(e.target.value)}
                    placeholder="e.g. React, SQL, Pune"
                    className="w-full bg-zinc-900 border border-white/5 rounded-xl pl-9 pr-4 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-zinc-600"
                  />
                </div>
              </div>

              {/* Work Type drop filter */}
              <div className="flex flex-col gap-2">
                <label className="text-xs font-semibold text-zinc-400">Work Setup</label>
                <select
                  value={jobWorkType}
                  onChange={(e) => setJobWorkType(e.target.value)}
                  className="w-full bg-zinc-900 border border-white/5 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition-all cursor-pointer"
                >
                  <option value="all">All Setups</option>
                  <option value="Remote">Remote</option>
                  <option value="Hybrid">Hybrid</option>
                  <option value="Onsite">Onsite</option>
                </select>
              </div>

              {/* Location drop filter */}
              <div className="flex flex-col gap-2">
                <label className="text-xs font-semibold text-zinc-400">Location</label>
                <select
                  value={jobLocation}
                  onChange={(e) => setJobLocation(e.target.value)}
                  className="w-full bg-zinc-900 border border-white/5 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition-all cursor-pointer"
                >
                  <option value="all">All Cities</option>
                  <option value="Bangalore">Bangalore</option>
                  <option value="Pune">Pune</option>
                  <option value="Mumbai">Mumbai</option>
                  <option value="Chennai">Chennai</option>
                  <option value="Hyderabad">Hyderabad</option>
                </select>
              </div>

              {/* Checkbox filters */}
              <div className="flex flex-col gap-3 pt-2 border-t border-white/5">
                <label className="flex items-center gap-2.5 text-xs text-zinc-300 cursor-pointer select-none">
                  <input 
                    type="checkbox"
                    checked={jobFresher}
                    onChange={(e) => setJobFresher(e.target.checked)}
                    className="rounded border-zinc-800 text-blue-500 focus:ring-blue-500/20 bg-zinc-900 cursor-pointer"
                  />
                  <span>Fresher Friendly</span>
                </label>
                
                <label className="flex items-center gap-2.5 text-xs text-zinc-300 cursor-pointer select-none">
                  <input 
                    type="checkbox"
                    checked={jobWomen}
                    onChange={(e) => setJobWomen(e.target.checked)}
                    className="rounded border-zinc-800 text-blue-500 focus:ring-blue-500/20 bg-zinc-900 cursor-pointer"
                  />
                  <span>Women Hiring Programs</span>
                </label>

                <label className="flex items-center gap-2.5 text-xs text-zinc-300 cursor-pointer select-none">
                  <input 
                    type="checkbox"
                    checked={jobDiversity}
                    onChange={(e) => setJobDiversity(e.target.checked)}
                    className="rounded border-zinc-800 text-blue-500 focus:ring-blue-500/20 bg-zinc-900 cursor-pointer"
                  />
                  <span>Diversity Hiring</span>
                </label>
              </div>
            </div>


            {/* Matching Jobs List Column */}
            <div className="lg:col-span-3 flex flex-col gap-4">
              {(() => {
                const displayedMatches = jobMatches.filter(match => 
                  jobsList.some(j => j.id === match.job_id)
                );
                
                return (
                  <>
                    <div className="flex items-center justify-between text-xs text-zinc-500 px-1 font-semibold">
                      <span>Displaying {displayedMatches.length} matching jobs based on your filters</span>
                      <span>Sorted by Compatibility</span>
                    </div>
                    
                    <div className="flex flex-col gap-4">
                      {displayedMatches.map((match) => {
                        const originalJob = jobsList.find(j => j.id === match.job_id);
                        if (!originalJob) return null;
                        const score = match.compatibility_score;
                        const scoreColor = score >= 80 
                          ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/25 glow-emerald-sm' 
                          : score >= 65 
                            ? 'text-blue-400 bg-blue-500/10 border-blue-500/25 glow-blue-sm' 
                            : 'text-zinc-400 bg-zinc-900 border-white/5';
                        
                        return (
                          <div 
                            key={match.id}
                            className="glass-card p-6 rounded-2xl border border-white/5 flex flex-col gap-4 hover:border-zinc-800 transition-all duration-300 relative overflow-hidden"
                          >
                            {/* Subtle left border indicator based on score */}
                            <div className={`absolute left-0 top-0 bottom-0 w-1 ${
                              score >= 80 ? 'bg-emerald-500' : score >= 65 ? 'bg-blue-500' : 'bg-zinc-700'
                            }`} />

                            {/* Title, company and score row */}
                            <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-2">
                              <div>
                                <h4 className="text-base font-bold text-white">{match.role}</h4>
                                <div className="flex flex-wrap items-center gap-2 mt-1.5 text-xs text-zinc-400">
                                  <span className="font-semibold text-zinc-300">{match.company}</span>
                                  <span className="text-zinc-600">&bull;</span>
                                  <span>📍 {originalJob.location} ({originalJob.work_type})</span>
                                  <span className="text-zinc-600">&bull;</span>
                                  <span className="text-blue-400 font-medium">💰 {originalJob.salary_range}</span>
                                </div>
                              </div>
                              <div className={`px-3 py-1.5 rounded-xl border text-xs font-extrabold text-center shrink-0 h-fit ${scoreColor}`}>
                                {score}% Match
                              </div>
                            </div>

                            {/* Job Badges Row */}
                            <div className="flex flex-wrap gap-2 text-[10px] font-semibold">
                              <span className="px-2 py-0.5 rounded-md bg-zinc-800/80 border border-white/5 text-zinc-300">
                                💼 {originalJob.role_type}
                              </span>
                              {originalJob.fresher_friendly && (
                                <span className="px-2 py-0.5 rounded-md bg-blue-500/10 border border-blue-500/20 text-blue-400">
                                  🎓 Fresher Friendly
                                </span>
                              )}
                              {originalJob.women_hiring_program && (
                                <span className="px-2 py-0.5 rounded-md bg-purple-500/10 border border-purple-500/20 text-purple-400">
                                  👩 Women Hiring
                                </span>
                              )}
                              {originalJob.diversity_hiring && (
                                <span className="px-2 py-0.5 rounded-md bg-pink-500/10 border border-pink-500/20 text-pink-400">
                                  🌈 Diversity Focus
                                </span>
                              )}
                            </div>

                            {/* Description snippet */}
                            <p className="text-xs text-zinc-400 leading-relaxed bg-zinc-950/20 p-3 rounded-xl border border-white/[0.02]">
                              {originalJob.description}
                            </p>

                            {/* Skills breakdown */}
                            <div className="flex flex-col gap-2">
                              <div className="flex flex-wrap gap-1.5 text-[10px] items-center">
                                <span className="text-zinc-500 font-semibold uppercase tracking-wider mr-1">Matched Skills:</span>
                                {match.matched_skills?.map((sk, i) => (
                                  <span key={i} className="px-2 py-0.5 rounded bg-green-500/10 text-green-400 border border-green-500/20 font-medium">
                                    {sk}
                                  </span>
                                ))}
                                {(!match.matched_skills || match.matched_skills.length === 0) && (
                                  <span className="text-zinc-600 italic">None matched</span>
                                )}
                              </div>
                              
                              <div className="flex flex-wrap gap-1.5 text-[10px] items-center">
                                <span className="text-zinc-500 font-semibold uppercase tracking-wider mr-1">Missing Gaps:</span>
                                {match.missing_skills?.map((sk, i) => (
                                  <span key={i} className="px-2 py-0.5 rounded bg-red-500/10 text-red-400 border border-red-500/20 font-medium">
                                    {sk}
                                  </span>
                                ))}
                                {(!match.missing_skills || match.missing_skills.length === 0) && (
                                  <span className="text-zinc-600 italic">None. Fully aligned!</span>
                                )}
                              </div>
                            </div>

                            {/* Coach fit explanation */}
                            <div className="bg-zinc-900/60 p-4 rounded-xl border border-white/5 flex flex-col gap-2">
                              <span className="text-[10px] font-bold text-blue-400 uppercase tracking-widest flex items-center gap-1">
                                <Sparkles className="w-3.5 h-3.5" /> Coach Evaluation Fit
                              </span>
                              <p className="text-xs text-zinc-300 leading-relaxed font-medium">
                                {match.explanation}
                              </p>
                              <p className="text-xs text-zinc-400 leading-relaxed mt-1 border-t border-white/5 pt-2 italic">
                                <strong>How to improve:</strong> {match.how_to_improve}
                              </p>
                            </div>

                            {/* Call to Actions */}
                            <div className="flex gap-2 justify-end pt-2 border-t border-white/5">
                              <button
                                onClick={() => {
                                  setRoadmapRole(match.role);
                                  setActiveTab('roadmap');
                                }}
                                className="px-4 py-2 rounded-xl border border-white/5 bg-zinc-900/50 hover:bg-zinc-800 text-zinc-300 text-xs font-semibold hover:text-white transition-all cursor-pointer"
                              >
                                Build Learning Timeline
                              </button>
                              <button
                                onClick={() => handlePrepopulateOptimizer(match)}
                                className="px-4 py-2 rounded-xl bg-blue-500 hover:bg-blue-600 text-white text-xs font-semibold transition-all flex items-center gap-1.5 cursor-pointer"
                              >
                                <Sparkles className="w-3.5 h-3.5" /> Optimize Resume
                              </button>
                            </div>
                          </div>
                        );
                      })}
                      {displayedMatches.length === 0 && (
                        <div className="text-zinc-500 text-sm text-center py-12 glass-card border border-white/5 rounded-2xl">
                          No jobs matched your current skills or filter parameters. Try checking other search tags!
                        </div>
                      )}
                    </div>
                  </>
                );
              })()}
            </div>
          </div>
        )}

        {/* 4. LEARNING ROADMAP VIEW */}
        {activeTab === 'roadmap' && (
          <div className="flex flex-col gap-8">
            
            {/* Input Selection Header */}
            <div className="glass-card p-6 rounded-2xl border border-white/5 flex flex-col sm:flex-row items-end gap-4">
              <div className="flex-1 flex flex-col gap-2 w-full">
                <label className="text-xs font-semibold text-zinc-400">Target Role Title</label>
                <div className="relative">
                  <Briefcase className="absolute left-3 top-2.5 w-4 h-4 text-zinc-500" />
                  <input 
                    type="text"
                    value={roadmapRole}
                    onChange={(e) => setRoadmapRole(e.target.value)}
                    placeholder="e.g. Software Engineer, Junior Data Analyst"
                    className="w-full bg-zinc-900 border border-white/5 rounded-xl pl-9 pr-4 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-zinc-600"
                  />
                </div>
              </div>
              <button 
                onClick={handleGenerateRoadmap}
                disabled={isLoading || !roadmapRole.trim()}
                className="px-6 py-2.5 rounded-xl bg-blue-500 hover:bg-blue-600 disabled:bg-zinc-800 disabled:text-zinc-600 disabled:cursor-not-allowed text-white text-xs font-semibold transition-all shrink-0 w-full sm:w-auto h-fit cursor-pointer flex items-center justify-center gap-1.5"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
                <span>Build Roadmap Timeline</span>
              </button>
            </div>

            {/* Roadmap Content */}
            {activeRoadmap ? (
              <div className="flex flex-col gap-8">
                
                {/* Roadmap intro widget */}
                <div className="p-4 rounded-xl bg-blue-500/5 border border-blue-500/10 text-xs text-zinc-300 leading-relaxed flex items-start gap-3 max-w-3xl">
                  <Sparkles className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-white block">Custom 4-Month Curriculum: {activeRoadmap.target_role}</span>
                    This syllabus targets your missing skills. Spend 8-10 hours weekly completing milestones, studying free tutorials, and building projects.
                  </div>
                </div>

                {/* Timeline months timeline */}
                <div className="relative pl-8 md:pl-12 border-l border-white/10 flex flex-col gap-12 max-w-4xl py-2">
                  
                  {/* Month items */}
                  {Object.entries(activeRoadmap.roadmap_data).map(([key, value]: [string, any], index) => {
                    const monthNum = index + 1;
                    return (
                      <div key={key} className="relative group">
                        
                        {/* Dot indicator */}
                        <div className="absolute left-[-42px] md:left-[-58px] top-1.5 w-7 h-7 rounded-full bg-zinc-900 border-2 border-blue-500 flex items-center justify-center text-[10px] font-bold text-blue-400 group-hover:scale-110 group-hover:bg-blue-500 group-hover:text-white transition-all font-mono">
                          M{monthNum}
                        </div>

                        {/* Content box */}
                        <div className="glass-card p-6 rounded-2xl border border-white/5 flex flex-col gap-5 hover:border-zinc-800 transition-all duration-300">
                          
                          {/* Title */}
                          <div className="flex items-start justify-between gap-4">
                            <div>
                              <span className="text-[10px] font-bold text-blue-400 uppercase tracking-widest font-mono">Month 0{monthNum}</span>
                              <h4 className="text-base font-bold text-white mt-0.5">{value.title}</h4>
                            </div>
                            <span className="px-2 py-0.5 rounded bg-zinc-900 border border-white/5 text-[9px] text-zinc-500 uppercase tracking-wider">
                              Weeks {index * 4 + 1}-{index * 4 + 4}
                            </span>
                          </div>

                          {/* Goals, milestones & resources grid */}
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            
                            {/* Learning goals column */}
                            <div className="flex flex-col gap-2.5">
                              <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider flex items-center gap-1">
                                <BookOpen className="w-3.5 h-3.5" /> Syllabus Goals
                              </span>
                              <ul className="text-xs text-zinc-300 space-y-1.5 list-disc pl-4 leading-relaxed">
                                {value.learning_goals?.map((goal: string, idx: number) => (
                                  <li key={idx}>{goal}</li>
                                ))}
                              </ul>
                            </div>

                            {/* Milestones column */}
                            <div className="flex flex-col gap-2.5">
                              <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider flex items-center gap-1">
                                <Milestone className="w-3.5 h-3.5" /> Milestones
                              </span>
                              <ul className="text-xs text-zinc-300 space-y-1.5 list-disc pl-4 leading-relaxed">
                                {value.milestones?.map((milestone: string, idx: number) => (
                                  <li key={idx}>{milestone}</li>
                                ))}
                              </ul>
                            </div>

                            {/* Free Resources column */}
                            <div className="flex flex-col gap-2.5">
                              <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider flex items-center gap-1">
                                <ExternalLink className="w-3.5 h-3.5" /> Free Resources
                              </span>
                              <ul className="text-xs text-zinc-300 space-y-1.5 list-disc pl-4 leading-relaxed">
                                {value.resources?.map((res: string, idx: number) => (
                                  <li key={idx}>{res}</li>
                                ))}
                              </ul>
                            </div>

                          </div>

                          {/* Mini Project details row */}
                          <div className="border-t border-white/5 pt-4 flex flex-col gap-2 bg-zinc-900/30 p-4 rounded-xl">
                            <div className="flex items-center gap-1 text-[10px] font-bold text-purple-400 uppercase tracking-wider">
                              <CheckCircle2 className="w-3.5 h-3.5" /> Hands-On Mini Project
                            </div>
                            <span className="text-xs font-bold text-zinc-200 mt-0.5">{value.mini_project?.title}</span>
                            <p className="text-xs text-zinc-400 leading-relaxed">{value.mini_project?.description}</p>
                          </div>

                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="text-zinc-500 text-sm text-center py-16 glass-card border border-white/5 rounded-2xl max-w-4xl">
                Enter your target role at the top and click generate to build your personalized 4-month syllabus.
              </div>
            )}
          </div>
        )}

        {/* 5. RESUME OPTIMIZER VIEW */}
        {activeTab === 'optimizer' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            {/* Input requirements left pane */}
            <div className="lg:col-span-4 flex flex-col gap-6">
              
              {/* Info panel */}
              <div className="glass-card p-6 rounded-2xl border border-white/5 flex flex-col gap-4">
                <div>
                  <h3 className="font-bold text-base text-white">Resume Optimizer</h3>
                  <p className="text-xs text-zinc-500 mt-0.5">Tailors bullet points and structures keyword matrices to boost scoring.</p>
                </div>
                
                {selectedJobForOpt && (
                  <div className="p-3 rounded-lg bg-zinc-900 border border-white/5 text-xs text-zinc-400">
                    Pre-selected: <strong className="text-white">{selectedJobForOpt.role}</strong> at {selectedJobForOpt.company}.
                    <button 
                      onClick={() => { setSelectedJobForOpt(null); setCustomOptRole(''); setCustomOptCompany(''); setCustomOptJD(''); }}
                      className="text-xs text-blue-400 hover:text-blue-300 block mt-1 hover:underline cursor-pointer"
                    >
                      Clear Selection & Build Custom
                    </button>
                  </div>
                )}

                <div className="flex flex-col gap-4 mt-2">
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[10px] font-bold text-zinc-400 uppercase">Target Role</label>
                    <input 
                      type="text"
                      value={customOptRole}
                      onChange={(e) => setCustomOptRole(e.target.value)}
                      placeholder="e.g. Software Engineer"
                      className="w-full bg-zinc-900 border border-white/5 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-zinc-600"
                    />
                  </div>
                  
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[10px] font-bold text-zinc-400 uppercase">Target Company</label>
                    <input 
                      type="text"
                      value={customOptCompany}
                      onChange={(e) => setCustomOptCompany(e.target.value)}
                      placeholder="e.g. TechCorp Solutions"
                      className="w-full bg-zinc-900 border border-white/5 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-zinc-600"
                    />
                  </div>
                  
                  <div className="flex flex-col gap-1.5">
                    <label className="text-[10px] font-bold text-zinc-400 uppercase">Job Description (JD)</label>
                    <textarea 
                      rows={6}
                      value={customOptJD}
                      onChange={(e) => setCustomOptJD(e.target.value)}
                      placeholder="Paste the target job description requirements here..."
                      className="w-full bg-zinc-900 border border-white/5 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-zinc-600 resize-none"
                    />
                  </div>
                </div>

                <button
                  onClick={handleRunOptimizer}
                  disabled={isLoading || !customOptRole || !customOptCompany || !customOptJD}
                  className="w-full py-2.5 rounded-xl bg-blue-500 hover:bg-blue-600 disabled:bg-zinc-800 disabled:text-zinc-600 disabled:cursor-not-allowed text-white text-xs font-semibold transition-all flex items-center justify-center gap-1.5 cursor-pointer mt-2"
                >
                  <Sparkles className="w-3.5 h-3.5 animate-pulse" />
                  <span>Tailor & Compile PDF</span>
                </button>
              </div>

            </div>

            {/* Results comparison right pane */}
            <div className="lg:col-span-8 flex flex-col gap-6">
              
              {optimizedResume ? (
                <div className="flex flex-col gap-6">
                  
                  {/* Optimization Success Indicator */}
                  {optSuccessMsg && (
                    <div className="p-4 rounded-xl bg-green-500/10 border border-green-500/20 text-xs text-green-400 flex items-start gap-3">
                      <Check className="w-5 h-5 shrink-0 mt-0.5" />
                      <div>
                        <span className="font-bold text-white block">Resume Tailored Successfully!</span>
                        A newly formatted PDF has been compiled using ReportLab flowables. You can download it below.
                      </div>
                    </div>
                  )}

                  {/* Score improvement panel */}
                  <div className="glass-card p-6 rounded-2xl border border-white/5 flex flex-col sm:flex-row items-center justify-between gap-6">
                    <div className="flex items-center gap-6">
                      
                      {/* Before score */}
                      <div className="flex flex-col items-center">
                        <span className="text-xs text-zinc-500 font-semibold mb-1">Before Match</span>
                        <div className="w-14 h-14 rounded-full bg-zinc-900 border-2 border-zinc-700 flex items-center justify-center text-sm font-bold text-zinc-400">
                          {optimizedResume.match_score_before}%
                        </div>
                      </div>

                      <ChevronRight className="w-5 h-5 text-zinc-600 hidden sm:block" />

                      {/* After score */}
                      <div className="flex flex-col items-center">
                        <span className="text-xs text-zinc-500 font-semibold mb-1">After Tailor</span>
                        <div className="w-14 h-14 rounded-full bg-green-500/10 border-2 border-green-500 flex items-center justify-center text-sm font-bold text-green-400">
                          {optimizedResume.match_score_after}%
                        </div>
                      </div>
                      
                      <div>
                        <span className="font-bold text-white text-sm block">ATS Score Jump: +{optimizedResume.match_score_after - optimizedResume.match_score_before}%</span>
                        <p className="text-zinc-500 text-xs mt-0.5">Bullet points optimized using industry keyword injection.</p>
                      </div>
                    </div>

                    <button 
                      onClick={handleDownloadOptimizedPDF}
                      className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white text-xs font-semibold transition-all flex items-center gap-1.5 cursor-pointer glow-blue w-full sm:w-auto justify-center"
                    >
                      <Download className="w-4 h-4" />
                      <span>Download Optimized PDF</span>
                    </button>
                  </div>

                  {/* Tailored Content Preview Drawer */}
                  <div className="glass-card p-6 rounded-2xl border border-white/5 flex flex-col gap-6">
                    <div>
                      <h3 className="font-bold text-base text-white">Tailored Resume Preview</h3>
                      <p className="text-xs text-zinc-500 mt-0.5">Below is the structured output used to compile the PDF.</p>
                    </div>

                    <div className="flex flex-col gap-5 text-xs text-zinc-300 divide-y divide-white/5">
                      {/* Summary */}
                      <div className="pb-4">
                        <span className="text-[10px] font-bold text-blue-400 uppercase tracking-widest block mb-2">Professional Summary</span>
                        <p className="leading-relaxed">{optimizedResume.optimized_text.summary}</p>
                      </div>
                      
                      {/* Skills */}
                      <div className="py-4">
                        <span className="text-[10px] font-bold text-blue-400 uppercase tracking-widest block mb-2">Technical Skills Matrix</span>
                        <div className="flex flex-wrap gap-1.5">
                          {optimizedResume.optimized_text.skills?.map((sk: string, i: number) => (
                            <span key={i} className="px-2 py-0.5 rounded bg-zinc-900 border border-white/5 font-medium">{sk}</span>
                          ))}
                        </div>
                      </div>

                      {/* Work history */}
                      <div className="py-4">
                        <span className="text-[10px] font-bold text-blue-400 uppercase tracking-widest block mb-3">Tailored Experience Bullets</span>
                        <div className="space-y-4">
                          {optimizedResume.optimized_text.experience?.map((exp: any, i: number) => (
                            <div key={i} className="flex flex-col gap-1.5">
                              <span className="font-bold text-white">{exp.role} at {exp.company} ({exp.duration})</span>
                              <ul className="list-disc pl-4 space-y-1 text-zinc-400">
                                {exp.achievements?.map((ach: string, idx: number) => (
                                  <li key={idx}>{ach}</li>
                                ))}
                              </ul>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                </div>
              ) : (
                <div className="text-zinc-500 text-sm text-center py-20 glass-card border border-white/5 rounded-2xl h-full flex flex-col items-center justify-center gap-2">
                  <Sparkles className="w-8 h-8 text-zinc-600 animate-pulse" />
                  <span>Your tailored resume preview will appear here once compiled.</span>
                </div>
              )}

            </div>

          </div>
        )}

      </main>
    </div>
  );
}
