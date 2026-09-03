import { useEffect, useState } from "react";
import { X } from "lucide-react";

import Button from "../../atoms/Button/Button";
import FormField from "../../molecules/FormField/FormField";

import type { Department, Designation } from "../../../types/job.types";
import type { JobTemplate } from "../../../types/template.types";

interface CreateJobPostingModalProps {
  isOpen: boolean;
  templates: JobTemplate[];
  departments: Department[];
  designations: Designation[];

  onClose: () => void;

  onSubmit: (data: CreateJobPostingData) => Promise<void>;
}

export interface CreateJobPostingData {
  template_id?: string;

  title: string;
  description: string;
  department_id: string;
  designation_id: string;
  employment_type: "full_time" | "part_time";
  experience_years: number;
  skills: Array<Record<string, number | string>>;
  deadline: string;
  status: "draft" | "open";
  location?: string;
  salary?: number;
  deadline_reminder_at?: string;
}

const CreateJobPostingModal = ({
  isOpen,
  templates,
  departments,
  designations,
  onClose,
  onSubmit,
}: CreateJobPostingModalProps) => {
  const [selectedTemplateId, setSelectedTemplateId] = useState("");

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [departmentId, setDepartmentId] = useState("");
  const [designationId, setDesignationId] = useState("");
  const [employmentType, setEmploymentType] = useState<
    "full_time" | "part_time"
  >("full_time");
  const [experienceYears, setExperienceYears] = useState(0);
  const [deadline, setDeadline] = useState("");
  const [status, setStatus] = useState<"draft" | "open">("draft");
  const [location, setLocation] = useState("");
  const [salary, setSalary] = useState("");
  const [deadlineReminderAt, setDeadlineReminderAt] = useState("");

  const [error, setError] = useState("");

  useEffect(() => {
    if (!isOpen) return;

    setSelectedTemplateId("");
    setTitle("");
    setDescription("");
    setDepartmentId(departments[0]?.id ?? "");
    setDesignationId("");
    setEmploymentType("full_time");
    setExperienceYears(0);
    setDeadline("");
    setStatus("draft");
    setLocation("");
    setSalary("");
    setDeadlineReminderAt("");
    setError("");
  }, [isOpen, departments]);

  if (!isOpen) {
    return null;
  }

  const handleTemplateChange = (templateId: string) => {
    setSelectedTemplateId(templateId);

    if (!templateId) {
      return;
    }

    const template = templates.find((item) => item.id === templateId);

    if (!template) {
      return;
    }

    setTitle(template.title);
    setDescription(template.description ?? "");
    setDesignationId(template.designation_id);

    if (
      template.employment_type === "full_time" ||
      template.employment_type === "part_time"
    ) {
      setEmploymentType(template.employment_type);
    }

    setExperienceYears(template.experience_years ?? 0);

    setSalary(
      template.salary !== null && template.salary !== undefined
        ? String(template.salary)
        : "",
    );
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");

    if (!title.trim()) {
      setError("Job title is required.");
      return;
    }

    if (!description.trim()) {
      setError("Job description is required.");
      return;
    }

    if (!departmentId) {
      setError("Department is required.");
      return;
    }

    if (!designationId) {
      setError("Designation is required.");
      return;
    }

    if (!deadline) {
      setError("Deadline is required.");
      return;
    }

    if (status === "open" && !deadline) {
      setError("An open posting must have a deadline.");
      return;
    }

    await onSubmit({
      title: title.trim(),
      description: description.trim(),
      department_id: departmentId,
      designation_id: designationId,
      employment_type: employmentType,
      experience_years: Number(experienceYears),
      skills: [],
      deadline: new Date(deadline).toISOString(),
      status,
      ...(location.trim() && {
        location: location.trim(),
      }),
      ...(salary && {
        salary: Number(salary),
      }),
      ...(deadlineReminderAt && {
        deadline_reminder_at: new Date(deadlineReminderAt).toISOString(),
      }),
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4 py-6">
      <div
        className="w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-3xl bg-bg-alt shadow-2xl"
        role="dialog"
        aria-modal="true"
        aria-labelledby="create-job-posting-title"
      >
        {/* Header */}
        <div className="sticky top-0 z-10 flex items-center justify-between border-b border-text/10 bg-bg-alt px-6 py-5">
          <div>
            <h2
              id="create-job-posting-title"
              className="text-xl font-bold text-text"
            >
              Create Job Posting
            </h2>

            <p className="mt-1 text-sm text-text-alt">
              Create a new internal job opportunity.
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="rounded-xl p-2 text-text-alt transition hover:bg-text/5 hover:text-text"
            aria-label="Close"
          >
            <X size={20} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-5 p-6">
          {/* Template */}
          {templates.length > 0 && (
            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="job-template"
                className="text-xs font-semibold uppercase tracking-wide text-text-alt"
              >
                Job Template
              </label>

              <select
                id="job-template"
                value={selectedTemplateId}
                onChange={(event) => handleTemplateChange(event.target.value)}
                className="w-full rounded-xl border border-text/15 bg-bg-alt px-4 py-3.5 text-sm text-text outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
              >
                <option value="">Create without template</option>

                {templates.map((template) => (
                  <option key={template.id} value={template.id}>
                    {template.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Title */}
          <FormField
            label="Job Title *"
            name="title"
            placeholder="e.g. Senior Software Engineer"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />

          {/* Description */}
          <div className="flex flex-col gap-1.5">
            <label
              htmlFor="job-description"
              className="text-xs font-semibold uppercase tracking-wide text-text-alt"
            >
              Description *
            </label>

            <textarea
              id="job-description"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Describe the role and responsibilities..."
              rows={5}
              className="w-full resize-y rounded-xl border border-text/15 bg-bg-alt px-4 py-3.5 text-sm text-text placeholder:text-text-alt/50 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
            />
          </div>

          {/* Department + Designation */}
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="job-department"
                className="text-xs font-semibold uppercase tracking-wide text-text-alt"
              >
                Department *
              </label>

              <select
                id="job-department"
                value={departmentId}
                onChange={(event) => setDepartmentId(event.target.value)}
                className="w-full rounded-xl border border-text/15 bg-bg-alt px-4 py-3.5 text-sm text-text outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
              >
                <option value="">Select department</option>

                {departments.map((department) => (
                  <option key={department.id} value={department.id}>
                    {department.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="job-designation"
                className="text-xs font-semibold uppercase tracking-wide text-text-alt"
              >
                Designation *
              </label>

              <select
                id="job-designation"
                value={designationId}
                onChange={(event) => setDesignationId(event.target.value)}
                className="w-full rounded-xl border border-text/15 bg-bg-alt px-4 py-3.5 text-sm text-text outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
              >
                <option value="">Select designation</option>

                {designations.map((designation) => (
                  <option key={designation.id} value={designation.id}>
                    {designation.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Employment + Experience */}
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="employment-type"
                className="text-xs font-semibold uppercase tracking-wide text-text-alt"
              >
                Employment Type *
              </label>

              <select
                id="employment-type"
                value={employmentType}
                onChange={(event) =>
                  setEmploymentType(
                    event.target.value as "full_time" | "part_time",
                  )
                }
                className="w-full rounded-xl border border-text/15 bg-bg-alt px-4 py-3.5 text-sm text-text outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
              >
                <option value="full_time">Full Time</option>
                <option value="part_time">Part Time</option>
              </select>
            </div>

            <FormField
              label="Experience (Years) *"
              name="experience_years"
              type="number"
              min="0"
              step="0.1"
              value={experienceYears}
              onChange={(event) =>
                setExperienceYears(Number(event.target.value))
              }
            />
          </div>

          {/* Location + Salary */}
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
            <FormField
              label="Location"
              name="location"
              placeholder="e.g. Bengaluru"
              value={location}
              onChange={(event) => setLocation(event.target.value)}
            />

            <FormField
              label="Salary"
              name="salary"
              type="number"
              min="0"
              step="0.01"
              placeholder="Optional"
              value={salary}
              onChange={(event) => setSalary(event.target.value)}
            />
          </div>

          {/* Deadline + Status */}
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
            <FormField
              label="Deadline *"
              name="deadline"
              type="datetime-local"
              value={deadline}
              onChange={(event) => setDeadline(event.target.value)}
            />

            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="job-status"
                className="text-xs font-semibold uppercase tracking-wide text-text-alt"
              >
                Initial Status
              </label>

              <select
                id="job-status"
                value={status}
                onChange={(event) =>
                  setStatus(event.target.value as "draft" | "open")
                }
                className="w-full rounded-xl border border-text/15 bg-bg-alt px-4 py-3.5 text-sm text-text outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
              >
                <option value="draft">Draft</option>
                <option value="open">Open</option>
              </select>
            </div>
          </div>

          {/* Reminder */}
          <FormField
            label="Deadline Reminder *"
            name="deadline_reminder_at"
            type="datetime-local"
            value={deadlineReminderAt}
            onChange={(event) => setDeadlineReminderAt(event.target.value)}
            helperText="Optional. Set when you want to be reminded about this posting."
          />

          {/* Error */}
          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
              {error}
            </div>
          )}

          {/* Footer */}
          <div className="flex flex-col-reverse gap-3 border-t border-text/10 pt-5 sm:flex-row sm:justify-end">
            <Button
              text="Cancel"
              type="button"
              variant="outline"
              color="secondary"
              onClick={onClose}
              className="rounded-lg"
            />

            <Button text="Create Posting" type="submit" color="primary" className="rounded-lg" />
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateJobPostingModal;
