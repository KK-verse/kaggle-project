"use client";

import { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useStore } from '@/store/useStore';
import { 
  UploadCloud, 
  Sparkles, 
  TrendingUp, 
  Map, 
  Briefcase, 
  FileText, 
  AlertTriangle, 
  CheckCircle,
  HelpCircle
} from 'lucide-react';

export default function LandingPage() {
  const router = useRouter();
  const { uploadResume, useSampleResume, isLoading, error } = useStore();
  const [isDragActive, setIsDragActive] = useState(false);
  const [dragError, setDragError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const sampleResumes = [
    { name: "Software Freshman", file: "resume_software_freshman.pdf", desc: "For entry-level SWE / internship roles. (Python, Java, OOP)" },
    { name: "Data Analyst Graduate", file: "resume_data_analyst.pdf", desc: "For analytical positions. (SQL, Excel, Pandas, Tableau)" },
    { name: "React Frontend Dev", file: "resume_web_developer.pdf", desc: "For UI-heavy engineering paths. (React, Next.js, CSS)" },
    { name: "General Science", file: "resume_general_science.pdf", desc: "For lab/research roles with basic Python. (Statistics, Excel)" },
    { name: "Unoptimized Resume", file: "resume_unoptimized.pdf", desc: "For testing the Resume Optimizer. Low score to high score jump!" },
  ];

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
      setIsDragActive(false);
    }
  };

  const processFile = async (file: File) => {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setDragError("Only PDF resumes are supported.");
      return;
    }
    setDragError(null);
    const resumeId = await uploadResume(file);
    if (resumeId) {
      router.push('/dashboard');
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      await processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      await processFile(e.target.files[0]);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  const handleSelectSample = async (filename: string) => {
    setDragError(null);
    const resumeId = await useSampleResume(filename);
    if (resumeId) {
      router.push('/dashboard');
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#09090b] flex flex-col font-sans select-none">
      {/* Decorative ambient background glows */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[60%] rounded-full bg-blue-500/10 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[60%] rounded-full bg-purple-500/10 blur-[120px] pointer-events-none" />

      {/* Navigation Header */}
      <header className="w-full max-w-7xl mx-auto px-6 py-6 flex items-center justify-between border-b border-white/5 relative z-10">
        <div className="flex items-center gap-2">
          <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-2 rounded-xl text-white font-bold flex items-center justify-center glow-blue">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <span className="font-heading font-extrabold text-2xl tracking-tight bg-gradient-to-r from-white via-zinc-200 to-zinc-400 bg-clip-text text-transparent">
            Career<span className="text-blue-500">Pilot</span>
          </span>
          <span className="ml-2 px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-[10px] font-semibold text-blue-400 uppercase tracking-widest">
            AI AGENT
          </span>
        </div>
        <div className="text-xs text-zinc-400 font-medium">
          Built for AI Agent Competition
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-6 py-12 md:py-20 flex flex-col lg:flex-row gap-12 lg:gap-16 items-center justify-center relative z-10">
        
        {/* Hero Section */}
        <div className="flex-1 flex flex-col items-start text-left max-w-xl">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-zinc-300 mb-6 hover:border-blue-500/20 transition-all duration-300">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            <span>Hyper-Personalized AI Career Co-Pilot</span>
          </div>
          
          <h1 className="font-heading font-black text-4xl sm:text-5xl lg:text-6xl leading-[1.1] tracking-tight text-white mb-6">
            Navigate Your Career With <span className="bg-gradient-to-r from-blue-400 via-blue-500 to-indigo-600 bg-clip-text text-transparent">AI Guidance</span>
          </h1>
          
          <p className="text-zinc-400 text-lg leading-relaxed mb-8">
            Upload your resume, see your actual industry readiness, find matched roles, trace skill gaps, build timelines, and tailors resumes instantly.
          </p>

          {/* Features Checklist */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full text-zinc-300 text-sm">
            <div className="flex items-center gap-2.5">
              <div className="rounded-lg bg-blue-500/10 p-1 border border-blue-500/20 text-blue-400">
                <CheckCircle className="w-4 h-4" />
              </div>
              <span>ATS SWOT Analysis</span>
            </div>
            <div className="flex items-center gap-2.5">
              <div className="rounded-lg bg-blue-500/10 p-1 border border-blue-500/20 text-blue-400">
                <TrendingUp className="w-4 h-4" />
              </div>
              <span>Career Readiness Score</span>
            </div>
            <div className="flex items-center gap-2.5">
              <div className="rounded-lg bg-blue-500/10 p-1 border border-blue-500/20 text-blue-400">
                <Map className="w-4 h-4" />
              </div>
              <span>4-Month Learning Timeline</span>
            </div>
            <div className="flex items-center gap-2.5">
              <div className="rounded-lg bg-blue-500/10 p-1 border border-blue-500/20 text-blue-400">
                <Briefcase className="w-4 h-4" />
              </div>
              <span>ATS Resume Tailoring</span>
            </div>
          </div>
        </div>

        {/* Upload Panel */}
        <div className="w-full max-w-md flex flex-col gap-6">
          <div 
            className={`glass-card p-8 rounded-2xl border transition-all duration-300 text-center relative group ${
              isDragActive 
                ? 'border-blue-500/70 bg-blue-500/5 glow-blue' 
                : 'border-white/5 bg-zinc-900/30 hover:border-white/10 hover:shadow-xl'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {isLoading ? (
              <div className="py-12 flex flex-col items-center justify-center gap-4">
                <div className="relative w-16 h-16">
                  <div className="absolute inset-0 rounded-full border-4 border-blue-500/10" />
                  <div className="absolute inset-0 rounded-full border-4 border-t-blue-500 border-l-blue-500 animate-spin" />
                </div>
                <div className="text-zinc-200 font-semibold tracking-wide animate-pulse">Analyzing Resume...</div>
                <p className="text-zinc-400 text-xs max-w-[280px]">
                  Extracting sections, scoring quality, mapping skill gaps, and running matches via Gemini AI.
                </p>
              </div>
            ) : (
              <div className="flex flex-col items-center py-6">
                <div className="w-14 h-14 rounded-2xl bg-zinc-800/50 border border-white/5 flex items-center justify-center mb-5 group-hover:scale-110 group-hover:border-blue-500/20 group-hover:bg-blue-500/5 transition-all duration-300">
                  <UploadCloud className="w-7 h-7 text-zinc-400 group-hover:text-blue-400 transition-colors" />
                </div>
                <h3 className="text-lg font-bold text-white mb-2">Upload your resume PDF</h3>
                <p className="text-zinc-400 text-sm mb-6 max-w-[280px]">
                  Drag & drop your PDF resume here, or click to browse local files.
                </p>
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  onChange={handleFileChange}
                  accept=".pdf"
                  className="hidden" 
                />
                <button 
                  onClick={triggerFileInput}
                  className="px-6 py-2.5 rounded-xl bg-blue-500 hover:bg-blue-600 active:scale-95 text-white text-sm font-semibold tracking-wide transition-all duration-200 glow-blue cursor-pointer"
                >
                  Browse Files
                </button>

                {(error || dragError) && (
                  <div className="mt-6 flex items-center gap-2 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-xs text-red-400 text-left w-full">
                    <AlertTriangle className="w-4 h-4 shrink-0" />
                    <span>{error || dragError}</span>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Sample Select Sandbox Grid */}
          <div className="w-full flex flex-col gap-3">
            <div className="flex items-center justify-between text-xs text-zinc-400 px-1 font-semibold tracking-wider uppercase">
              <span>Sandbox mode (1-Click Test)</span>
              <span className="text-[10px] text-blue-400 lowercase tracking-normal flex items-center gap-1 font-normal">
                <HelpCircle className="w-3.5 h-3.5" /> No PDF? Use a sample candidate!
              </span>
            </div>
            
            <div className="grid grid-cols-1 gap-2.5">
              {sampleResumes.map((sample) => (
                <button
                  key={sample.file}
                  onClick={() => handleSelectSample(sample.file)}
                  disabled={isLoading}
                  className="w-full p-3 text-left rounded-xl bg-zinc-900/40 border border-white/5 hover:border-blue-500/30 hover:bg-zinc-800/30 active:scale-[0.99] transition-all duration-200 flex items-start gap-3 cursor-pointer group"
                >
                  <div className="w-8 h-8 rounded-lg bg-zinc-800 border border-white/5 flex items-center justify-center shrink-0 group-hover:bg-blue-500/10 group-hover:border-blue-500/20 text-zinc-400 group-hover:text-blue-400 transition-colors">
                    <FileText className="w-4.5 h-4.5" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-sm font-bold text-white group-hover:text-blue-400 transition-colors">{sample.name}</span>
                    <span className="text-zinc-500 text-xs leading-relaxed mt-0.5">{sample.desc}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full border-t border-white/5 py-6 text-center text-xs text-zinc-500 relative z-10 mt-auto">
        © 2026 CareerPilot. Competition Build. Localhost Environment Mode.
      </footer>
    </div>
  );
}
