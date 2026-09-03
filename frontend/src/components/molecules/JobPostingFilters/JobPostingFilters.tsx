import Input from '../../atoms/Input/Input';
import { Search } from 'lucide-react';
import type { Department, Designation } from '../../../types/job.types';

interface JobPostingFiltersProps {
  searchQuery: string;
  statusFilter: string;
  departmentFilter: string;
  designationFilter: string;
  dueDateFilter: string;

  departments: Department[];
  designations: Designation[];

  onSearchChange: (value: string) => void;
  onStatusChange: (value: string) => void;
  onDepartmentChange: (value: string) => void;
  onDesignationChange: (value: string) => void;
  onDueDateChange: (value: string) => void;
}

const JobPostingFilters = ({
  searchQuery,
  statusFilter,
  departmentFilter,
  designationFilter,
  dueDateFilter,
  departments,
  designations,
  onSearchChange,
  onStatusChange,
  onDepartmentChange,
  onDesignationChange,
  onDueDateChange,
}: JobPostingFiltersProps) => {
  return (
    <div className="flex flex-col gap-4 p-4 rounded-2xl bg-bg-alt border border-text/10 shadow-sm">
      <div className="w-full">
        <Input
          type="text"
          placeholder="Search by job title or keywords..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          icon={<Search size={16} />}
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-semibold text-text-alt uppercase">
            Status
          </label>

          <select
            value={statusFilter}
            onChange={(e) => onStatusChange(e.target.value)}
            className="rounded-xl border border-text/15 bg-bg-alt px-3 py-2 text-sm text-text outline-none focus:border-primary"
          >
            <option value="ALL">All Statuses</option>
            <option value="draft">Draft</option>
            <option value="open">Open</option>
            <option value="closed">Closed</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-semibold text-text-alt uppercase">
            Department
          </label>

          <select
            value={departmentFilter}
            onChange={(e) => onDepartmentChange(e.target.value)}
            className="rounded-xl border border-text/15 bg-bg-alt px-3 py-2 text-sm text-text outline-none focus:border-primary"
          >
            <option value="">All Departments</option>

            {departments.map((department) => (
              <option key={department.id} value={department.id}>
                {department.name}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-semibold text-text-alt uppercase">
            Designation
          </label>

          <select
            value={designationFilter}
            onChange={(e) => onDesignationChange(e.target.value)}
            className="rounded-xl border border-text/15 bg-bg-alt px-3 py-2 text-sm text-text outline-none focus:border-primary"
          >
            <option value="">All Designations</option>

            {designations.map((designation) => (
              <option key={designation.id} value={designation.id}>
                {designation.name}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-semibold text-text-alt uppercase">
            Due Before
          </label>

          <input
            type="date"
            value={dueDateFilter}
            onChange={(e) => onDueDateChange(e.target.value)}
            className="rounded-xl border border-text/15 bg-bg-alt px-3 py-2 text-sm text-text outline-none focus:border-primary"
          />
        </div>
      </div>
    </div>
  );
};

export default JobPostingFilters;