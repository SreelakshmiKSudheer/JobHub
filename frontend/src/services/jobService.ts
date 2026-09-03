import { apiClient } from './apiClient';
import type { ApiResponse } from './apiClient';
import type { Department, Designation, JobPosting, JobPostingFilterParams } from '../types/job.types';

export const jobService = {
  getJobPostings: async (
  params?: JobPostingFilterParams
): Promise<{ data: JobPosting[]; total: number }> => {
  const query = new URLSearchParams();

  if (params?.q) {
    query.append('q', params.q);
  }

  if (params?.department_id) {
    query.append('department_id', params.department_id);
  }

  if (params?.designation_id) {
    query.append('designation_id', params.designation_id);
  }

  if (params?.skill_id) {
    query.append('skill_id', params.skill_id);
  }

  if (params?.due_before) {
    const fullDateTime = params.due_before.includes('T') 
        ? params.due_before 
        : `${params.due_before}T00:00:00.000Z`;
      
      // Note: Backend documentation uses 'due_before', so mapping it here
      query.append('due_before', fullDateTime);
  }

  if (params?.status) {
    query.append('status', params.status);
  }

  if (params?.sort_by) {
    query.append('sort_by', params.sort_by);
  }

  if (params?.page) {
    query.append('page', params.page.toString());
  }

  if (params?.page_size) {
    query.append('page_size', params.page_size.toString());
  }

  const queryString = query.toString()
    ? `?${query.toString()}`
    : '';

  const res = await apiClient<{
    data: JobPosting[];
    total: number;
  }>(`/job-postings${queryString}`);

  return res.data;
},

  getJobPostingApplications: async (jobPostingId: string): Promise<any[]> => {
    const res: ApiResponse<any[]> = await apiClient<any[]>(`/job-postings/${jobPostingId}/applications`);
    return res.data;
  },

  updateJobPostingStatus: async (jobPostingId: string, status: 'draft' | 'open' | 'closed' | 'completed'): Promise<JobPosting> => {
    const res: ApiResponse<JobPosting> = await apiClient<JobPosting>(`/job-postings/${jobPostingId}`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
    return res.data;
  },

  deleteJobPosting: async (jobPostingId: string): Promise<void> => {
    await apiClient(`/job-postings/${jobPostingId}`, { method: 'DELETE' });
  },

  getJobPostingById: async (id: string): Promise<JobPosting> => {
    const res: ApiResponse<JobPosting> = await apiClient<JobPosting>(`/job-postings/${id}`);
    return res.data;
  },

  getDepartments: async (): Promise<Department[]> => {
    const res: ApiResponse<Department[]> = await apiClient<Department[]>('/departments');
    return res.data;
  },

  getDesignations: async (): Promise<Designation[]> => {
    const res: ApiResponse<Designation[]> = await apiClient<Designation[]>('/designations');
    return res.data;
  },
};
