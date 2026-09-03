import Button from '../../atoms/Button/Button';
import { Calendar, Briefcase, Award, CheckCircle } from 'lucide-react';
import type { JobPostingCardProps } from '../../../types/jobPostingCard.types';

const JobPostingCard: React.FC<JobPostingCardProps> = ({
  job,
  departmentName = 'General',
  designationName = 'Engineering',
  onApply,
  onView,
  hasApplied = false,
  isApplying = false,
  className = '',
}) => {
  const formattedDeadline = new Date(job.deadline).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <div
      className={`flex flex-col justify-between p-6 rounded-2xl bg-bg-alt border border-text/10 shadow-sm hover:shadow-lg hover:border-primary/40 transition-all duration-300 ${className}`}
    >
      <div className="flex flex-col gap-3">
        {/* Header Badges */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-primary/10 text-primary border border-primary/20">
            {departmentName}
          </span>
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-text/5 text-text-alt border border-text/10">
            {designationName}
          </span>
        </div>

        {/* Job Title */}
        <h3
          onClick={() => onView?.(job.id)}
          className="text-lg font-bold text-text hover:text-primary transition-colors cursor-pointer line-clamp-1"
        >
          {job.title}
        </h3>

        {/* Job Meta (Experience & Deadline) */}
        <div className="flex flex-wrap items-center gap-4 text-xs text-text-alt font-medium">
          <div className="flex items-center gap-1.5">
            <Award size={14} className="text-primary" />
            <span>{job.experience_years} Yrs Exp</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Briefcase size={14} className="text-secondary" />
            <span className="capitalize">{job.employment_type.replace('_', ' ')}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Calendar size={14} className="text-red-500" />
            <span>Due: {formattedDeadline}</span>
          </div>
        </div>

        {/* Description */}
        <p className="text-sm text-text-alt line-clamp-2 mt-1 leading-relaxed">{job.description}</p>
      </div>

      {/* Footer Action */}
      <div className="mt-6 pt-4 border-t border-text/10 flex items-center justify-between gap-3">
        <button
          type="button"
          onClick={() => onView?.(job.id)}
          className="text-xs font-semibold text-text-alt hover:text-primary transition-colors"
        >
          Details
        </button>

        {hasApplied ? (
          <div className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-500/10 text-emerald-600 text-xs font-semibold border border-emerald-500/20">
            <CheckCircle size={14} />
            <span>Applied</span>
          </div>
        ) : (
          <Button
            text="Apply Now"
            variant="filled"
            color="primary"
            size="sm"
            loading={isApplying}
            onClick={() => onApply?.(job.id)}
            className="rounded-xl px-5 font-semibold text-xs shadow-sm hover:shadow"
          />
        )}
      </div>
    </div>
  );
};

export default JobPostingCard;
