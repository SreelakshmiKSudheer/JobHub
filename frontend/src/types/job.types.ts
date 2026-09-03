export interface Department {
  id: string;
  name: string;
  code: string;
}

export interface Designation {
  id: string;
  name: string;
  code: string;
  department_id: string;
}

export interface JobPosting {
  id: string;
  title: string;
  description: string;
  department_id: string;
  designation_id: string;
  location?: string | null;
  employment_type: 'full_time' | 'part_time' | 'contract' | 'internship';
  experience_years: number;
  skills: Array<Record<string, string | number>>;
  salary?: number | null;
  deadline: string;
  deadline_reminder_at?: string | null;
  status: 'draft' | 'open' | 'closed' | 'completed';
  created_by?: string | null;
}

export interface JobPostingFilterParams {
  q?: string;
  department_id?: string;
  designation_id?: string;
  skill_id?: string;
  due_before?: string;
  status?: 'draft' | 'open' | 'closed' | 'completed';
  sort_by?: 'deadline_asc' | 'deadline_desc';
  page?: number;
  page_size?: number;
}
