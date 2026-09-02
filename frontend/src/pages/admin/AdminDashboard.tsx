import { useEffect, useState, useMemo } from "react";
import { useNavigate } from "react-router";
import MetricCard from "../../components/molecules/MetricCard/MetricCard";
import Button from "../../components/atoms/Button/Button";
import { jobService } from "../../services/jobService";
import { templateService } from "../../services/templateService";
import type {
  JobPosting,
  Department,
  Designation,
} from "../../types/job.types";
import type { JobTemplate } from "../../types/template.types";
import {
  Briefcase,
  FileText,
  Calendar,
  RefreshCw,
  ArrowRight,
} from "lucide-react";
import { Typography } from "../../components/atoms/Typography/Typography";
import JobPostingViewCard from "../../components/organisms/JobPostingViewCard/JobPostingViewCard";
import JobTemplateCard from "../../components/organisms/JobTemplateCard/JobTemplateCard";

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [templates, setTemplates] = useState<JobTemplate[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [designations, setDesignations] = useState<Designation[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [
        jobsResponse,
        templateResponse,
        departmentResponse,
        designationResponse,
      ] = await Promise.all([
        jobService.getJobPostings({ limit: 20 }),
        templateService.getJobTemplates(),
        jobService.getDepartments(),
        jobService.getDesignations(),
      ]);

      setJobs(jobsResponse.data || []);
      setTemplates(templateResponse || []);
      setDepartments(departmentResponse || []);
      setDesignations(designationResponse || []);
    } catch (err: any) {
      console.error("Failed to load admin dashboard:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const deptMap = useMemo(() => {
    const map = new Map<string, string>();
    departments.forEach((d) => map.set(d.id, d.name));
    return map;
  }, [departments]);

  const desigMap = useMemo(() => {
    const map = new Map<string, string>();
    designations.forEach((d) => map.set(d.id, d.name));
    return map;
  }, [designations]);

  // Metric computations
  const draftCount = jobs.filter((j) => j.status === "draft").length;
  const openCount = jobs.filter((j) => j.status === "open").length;

  const closingThisWeekCount = jobs.filter((j) => {
    if (j.status !== "open" || !j.deadline) return false;
    const deadline = new Date(j.deadline).getTime();
    const now = Date.now();
    const sevenDays = 7 * 24 * 60 * 60 * 1000;
    return deadline >= now && deadline <= now + sevenDays;
  }).length;

  const metricData = [
    {
      title: "Draft Job Postings",
      value: draftCount,
      subtitle: "Postings requiring publication",
      color: "accent",
      icon: <FileText size={24} />,
    },
    {
      title: "Open Job Postings",
      value: openCount,
      subtitle: "Currently active for applications",
      color: "primary",
      icon: <Briefcase size={24} />,
    },
    {
      title: "Closing This Week",
      value: closingThisWeekCount,
      subtitle: "Deadlines within 7 days",
      color: "secondary",
      icon: <Calendar size={24} />,
    },
  ];

  if (loading) {
    return (
      <div className="w-full h-96 flex flex-col items-center justify-center gap-3">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-primary border-t-transparent" />
        <p className="text-sm font-medium text-text-alt">
          Loading Admin Dashboard...
        </p>
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col gap-8">
      {/* Title Bar */}
      <div className="flex items-center justify-between">
        <div>
          <Typography
            variant="pageheading"
            ashtml="h1"
            className="text-primary"
          >
            Admin Dashboard
          </Typography>
          <Typography
            variant="caption"
            ashtml="p"
            className="text-text-alt mt-0.5"
          >
            Manage job postings, templates, and applications.
          </Typography>
        </div>
        <Button
          text="Refresh"
          variant="outline"
          color="secondary"
          size="sm"
          onClick={fetchData}
          icon={<RefreshCw size={14} />}
          className="rounded-xl text-xs"
        />
      </div>

      {/* Metrics Section */}
      <div className="w-full flex flex-wrap gap-2 md:gap-4 items-stretch justify-between">
        {metricData.map((metric) => (
          <MetricCard
            title={metric.title}
            value={metric.value}
            subtitle={metric.subtitle}
            color={metric.color}
            icon={metric.icon}
          />
        ))}
      </div>

      {/* 2. Job Postings Section */}
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <Typography variant="subheading" className="text-primary">
            Recent Job Postings
          </Typography>
          <Button
            text="View All"
            icon={<ArrowRight size={16} />}
            iconPosition="right"
            variant="none"
            color="primary"
            size="md"
            className="font-semibold rounded-full"
            onClick={() => navigate("/admin/job-postings")}
          />
        </div>

        {jobs.length === 0 ? (
          <div className="p-8 rounded-2xl bg-bg-alt border border-text/10 text-center text-text-alt">
            No job postings created yet.
          </div>
        ) : (
          <div className="w-full flex flex-wrap items-stretch justify-between gap-2 md:gap-4">
            {jobs.slice(0, 3).map((job) => (
              <JobPostingViewCard
                key={job.id}
                id={job.id}
                status={job.status}
                department={deptMap.get(job.department_id) || "General"}
                title={job.title}
                designation={desigMap.get(job.designation_id) || "Specialist"}
                deadline={job.deadline ? new Date(job.deadline) : new Date()}
                description={job.description || "No description provided."}
              />
            ))}
          </div>
        )}

      </div>

      {/* 3. Job Templates Section */}
      <div className="flex flex-col gap-4 mt-2">
        <div className="flex items-center justify-between">
          <Typography variant="subheading" className="text-primary">
            Job Templates
          </Typography>
          <Button
            text="View All"
            icon={<ArrowRight size={16} />}
            iconPosition="right"
            variant="none"
            color="primary"
            size="md"
            className="font-semibold rounded-full"
            onClick={() => navigate("/admin/job-roles")}
          />
        </div>


        {templates.length === 0 ? (
          <div className="p-8 rounded-2xl bg-bg-alt border border-text/10 text-center text-text-alt">
            No job templates created yet.
          </div>
        ) : (
          <div className="flex flex-wrap items-stretch justify-between gap-2 md:gap-4">
            {templates.slice(0, 3).map((tmpl) => (
              <JobTemplateCard
                key={tmpl.id}
                id={tmpl.id}
                name={tmpl.name}
                title={tmpl.title}
                designation={desigMap.get(tmpl.designation_id) || "Specialist"}
                description={tmpl.description || "No description provided."}
              />
            ))}
            
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
