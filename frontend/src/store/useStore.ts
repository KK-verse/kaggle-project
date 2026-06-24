import { create } from 'zustand';

export interface ResumeData {
  id: number;
  filename: string;
  filepath: string;
  name: string | null;
  email: string | null;
  phone: string | null;
  skills: string[];
  education: Array<{ school: string; degree: string; year: string; gpa: string | null }>;
  projects: Array<{ title: string; description: string; technologies: string[] }>;
  experience: Array<{ company: string; role: string; duration: string; achievements: string[] }>;
  certifications: string[];
  achievements: string[];
  ats_score: number;
  quality_score: number;
  strengths: string[];
  weaknesses: string[];
  missing_keywords: string[];
  suggestions: string[];
  created_at: string;
}

export interface CareerScoreData {
  id: number;
  resume_id: number;
  readiness_score: number;
  explanation: string;
  action_plan: string[];
  created_at: string;
}

export interface JobMatchData {
  id: number;
  resume_id: number;
  job_id: string;
  role: string;
  company: string;
  compatibility_score: number;
  explanation: string;
  matched_skills: string[];
  missing_skills: string[];
  how_to_improve: string;
}

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  work_type: string;
  role_type: string;
  salary_range: string;
  fresher_friendly: boolean;
  women_hiring_program: boolean;
  diversity_hiring: boolean;
  required_skills: string[];
  description: string;
}

export interface RoadmapData {
  id: number;
  resume_id: number;
  target_role: string;
  roadmap_data: {
    month_1: {
      title: string;
      learning_goals: string[];
      milestones: string[];
      resources: string[];
      practice_tasks: string[];
      mini_project: { title: string; description: string };
    };
    month_2: {
      title: string;
      learning_goals: string[];
      milestones: string[];
      resources: string[];
      practice_tasks: string[];
      mini_project: { title: string; description: string };
    };
    month_3: {
      title: string;
      learning_goals: string[];
      milestones: string[];
      resources: string[];
      practice_tasks: string[];
      mini_project: { title: string; description: string };
    };
    month_4: {
      title: string;
      learning_goals: string[];
      milestones: string[];
      resources: string[];
      practice_tasks: string[];
      mini_project: { title: string; description: string };
    };
  };
}

export interface OptimizedResumeData {
  id: number;
  resume_id: number;
  job_id: string | null;
  target_role: string;
  company: string;
  match_score_before: number;
  match_score_after: number;
  pdf_url: string;
  optimized_text: {
    name: string;
    email: string;
    phone: string;
    summary: string;
    skills: string[];
    education: any[];
    experience: any[];
    projects: any[];
    certifications: string[];
    achievements: string[];
  };
}

interface CareerPilotState {
  activeResumeId: number | null;
  resumeData: ResumeData | null;
  careerScore: CareerScoreData | null;
  jobMatches: JobMatchData[];
  jobsList: Job[];
  activeRoadmap: RoadmapData | null;
  optimizedResume: OptimizedResumeData | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setActiveResumeId: (id: number | null) => void;
  uploadResume: (file: File) => Promise<number | null>;
  useSampleResume: (filename: string) => Promise<number | null>;
  fetchResumeDetails: (id: number) => Promise<void>;
  fetchCareerScore: (id: number) => Promise<void>;
  fetchJobMatches: (id: number) => Promise<void>;
  fetchJobsList: (filters?: {
    search?: string;
    location?: string;
    work_type?: string;
    role_type?: string;
    fresher_friendly?: boolean;
    women_hiring?: boolean;
    diversity_hiring?: boolean;
  }) => Promise<void>;
  generateRoadmap: (resumeId: number, targetRole: string) => Promise<void>;
  fetchRoadmap: (resumeId: number, targetRole: string) => Promise<boolean>;
  optimizeResume: (
    resumeId: number,
    jobId: string | null,
    targetRole: string,
    company: string,
    jobDescription: string
  ) => Promise<void>;
  resetStore: () => void;
}

const API_BASE_URL = 'http://localhost:8000';

export const useStore = create<CareerPilotState>((set) => ({
  activeResumeId: null,
  resumeData: null,
  careerScore: null,
  jobMatches: [],
  jobsList: [],
  activeRoadmap: null,
  optimizedResume: null,
  isLoading: false,
  error: null,

  setActiveResumeId: (id) => set({ activeResumeId: id }),

  uploadResume: async (file: File) => {
    set({ isLoading: true, error: null });
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/resumes/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to upload and parse resume.');
      }

      const data: ResumeData = await response.json();
      set({ 
        activeResumeId: data.id, 
        resumeData: data,
        optimizedResume: null,
        activeRoadmap: null
      });

      // Fetch career score & job matches in parallel
      await Promise.all([
        useStore.getState().fetchCareerScore(data.id),
        useStore.getState().fetchJobMatches(data.id),
      ]);

      set({ isLoading: false });
      return data.id;
    } catch (err: any) {
      set({ error: err.message || 'An error occurred during upload', isLoading: false });
      return null;
    }
  },

  useSampleResume: async (filename: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE_URL}/api/resumes/use-sample`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to process sample resume.');
      }

      const data: ResumeData = await response.json();
      set({ 
        activeResumeId: data.id, 
        resumeData: data,
        optimizedResume: null,
        activeRoadmap: null
      });

      // Fetch career score & job matches in parallel
      await Promise.all([
        useStore.getState().fetchCareerScore(data.id),
        useStore.getState().fetchJobMatches(data.id),
      ]);

      set({ isLoading: false });
      return data.id;
    } catch (err: any) {
      set({ error: err.message || 'An error occurred', isLoading: false });
      return null;
    }
  },

  fetchResumeDetails: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE_URL}/api/resumes/${id}`);
      if (!response.ok) throw new Error('Failed to fetch resume details.');
      const data = await response.json();
      set({ resumeData: data, activeResumeId: id, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  fetchCareerScore: async (id: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/career-score/${id}`);
      if (!response.ok) throw new Error('Failed to fetch career score.');
      const data = await response.json();
      set({ careerScore: data });
    } catch (err: any) {
      console.error('Error fetching career score:', err.message);
    }
  },

  fetchJobMatches: async (id: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/jobs/matches/${id}`);
      if (!response.ok) throw new Error('Failed to fetch job matches.');
      const data = await response.json();
      set({ jobMatches: data });
    } catch (err: any) {
      console.error('Error fetching job matches:', err.message);
    }
  },

  fetchJobsList: async (filters) => {
    set({ isLoading: true, error: null });
    try {
      const queryParams = new URLSearchParams();
      if (filters) {
        if (filters.search) queryParams.append('search', filters.search);
        if (filters.location) queryParams.append('location', filters.location);
        if (filters.work_type) queryParams.append('work_type', filters.work_type);
        if (filters.role_type) queryParams.append('role_type', filters.role_type);
        if (filters.fresher_friendly !== undefined) queryParams.append('fresher_friendly', String(filters.fresher_friendly));
        if (filters.women_hiring !== undefined) queryParams.append('women_hiring', String(filters.women_hiring));
        if (filters.diversity_hiring !== undefined) queryParams.append('diversity_hiring', String(filters.diversity_hiring));
      }

      const response = await fetch(`${API_BASE_URL}/api/jobs?${queryParams.toString()}`);
      if (!response.ok) throw new Error('Failed to fetch jobs.');
      const data = await response.json();
      set({ jobsList: data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  generateRoadmap: async (resumeId: number, targetRole: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE_URL}/api/roadmaps`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_id: resumeId, target_role: targetRole }),
      });
      if (!response.ok) throw new Error('Failed to generate learning roadmap.');
      const data = await response.json();
      set({ activeRoadmap: data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  fetchRoadmap: async (resumeId: number, targetRole: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/roadmaps/${resumeId}/${encodeURIComponent(targetRole)}`);
      if (response.ok) {
        const data = await response.json();
        set({ activeRoadmap: data });
        return true;
      }
      return false;
    } catch (err) {
      return false;
    }
  },

  optimizeResume: async (resumeId, jobId, targetRole, company, jobDescription) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE_URL}/api/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: resumeId,
          job_id: jobId,
          target_role: targetRole,
          company: company,
          job_description: jobDescription,
        }),
      });
      if (!response.ok) throw new Error('Failed to optimize resume.');
      const data = await response.json();
      set({ optimizedResume: data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  resetStore: () => set({
    activeResumeId: null,
    resumeData: null,
    careerScore: null,
    jobMatches: [],
    jobsList: [],
    activeRoadmap: null,
    optimizedResume: null,
    isLoading: false,
    error: null,
  }),
}));
