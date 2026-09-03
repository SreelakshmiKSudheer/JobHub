import type { JobPosting } from './job.types';

export interface JobPostingCardProps {
  job: JobPosting;
  departmentName?: string;
  designationName?: string;
  onApply?: (jobId: string) => void;
  onView?: (jobId: string) => void;
  hasApplied?: boolean;
  isApplying?: boolean;
  className?: string;
}
