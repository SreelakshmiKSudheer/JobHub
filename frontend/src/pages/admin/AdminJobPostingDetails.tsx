import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router";
import { apiClient } from "../../services/apiClient";
import type { JobPosting } from "../../types/job.types";
import Button from "../../components/atoms/Button/Button";
import { jobService } from "../../services/jobService";
import ConfirmationModal from "../../components/molecules/ConfirmationModal/ConfirmationModal";
import {
  Trash2,
  ArrowLeft,
  Users,
  Calendar,
  Briefcase,
  MapPin,
} from "lucide-react";

const AdminJobPostingDetails = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [job, setJob] = useState<JobPosting | null>(null);
  const [applications, setApplications] = useState<any[]>([]); // Adjust type based on your app
  const [loading, setLoading] = useState(true);

  const [modalConfig, setModalConfig] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    confirmText?: string;
    variant?: "primary" | "danger";
    onConfirm: () => Promise<void>;
  }>({
    isOpen: false,
    title: "",
    message: "",
    onConfirm: async () => {},
  });
  const [modalLoading, setModalLoading] = useState(false);

  const fetchJobDetails = async () => {
    if (!id) return;
    setLoading(true);
    try {
      const jobRes = await jobService.getJobPostingById(id);
      
      setJob(jobRes?.data ? jobRes.data : jobRes);

      const appsRes = await jobService.getJobPostingApplications(id);

      const extractedApps = appsRes?.data ? appsRes.data : appsRes;
      
      console.log("Extracted applications array:", extractedApps);

      setApplications(Array.isArray(extractedApps) ? extractedApps : []);
      
    } catch (err: any) {
      console.error("Failed to fetch job details:", err);
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    fetchJobDetails();
  }, [id]);

  const triggerDeleteDraftConfirmation = () => {
    if (!job) return;
    setModalConfig({
      isOpen: true,
      title: "Delete Draft Job Posting",
      message: `Are you sure you want to delete draft posting "${job.title}"? This action cannot be undone.`,
      confirmText: "Delete Draft",
      variant: "danger",
      onConfirm: async () => {
        setModalLoading(true);
        try {
          await jobService.deleteJobPosting(id);
          navigate("/admin/job-postings", { replace: true });
        } catch (err: any) {
          alert(err.message || "Failed to delete draft posting");
        } finally {
          setModalLoading(false);
          setModalConfig((prev) => ({ ...prev, isOpen: false }));
        }
      },
    });
  };

  const triggerStatusChangeConfirmation = (newStatus: string) => {
    if (!job) return;
    setModalConfig({
      isOpen: true,
      title: "Update Posting Status",
      message: `Are you sure you want to change posting status to ${newStatus.toUpperCase()}?`,
      confirmText: "Update Status",
      variant: "primary",
      onConfirm: async () => {
        setModalLoading(true);
        try {
          await jobService.updateJobPostingStatus(id, newStatus as 'draft' | 'open' | 'closed' | 'completed');
          await fetchJobDetails(); // Refresh UI
        } catch (err: any) {
          alert(err.message || "Failed to update posting status");
        } finally {
          setModalLoading(false);
          setModalConfig((prev) => ({ ...prev, isOpen: false }));
        }
      },
    });
  };

  if (loading) {
    return (
      <div className="w-full h-[60vh] flex flex-col items-center justify-center gap-3">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-primary border-t-transparent" />
        <p className="text-sm font-medium text-text-alt">
          Loading Job Details...
        </p>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="w-full text-center p-10 text-text-alt bg-bg-alt rounded-2xl border border-text/10">
        Job Posting not found.
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col gap-6 max-w-5xl mx-auto">
      {/* Top Bar: Back & Actions */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <button
          onClick={() => navigate("/admin/job-postings")}
          className="flex items-center gap-2 text-sm font-semibold text-text-alt hover:text-primary transition-colors"
        >
          <ArrowLeft size={16} /> Back to Job Postings
        </button>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-bg-alt border border-text/10 px-3 py-1.5 rounded-xl">
            <span className="text-xs font-semibold text-text-alt">Status:</span>
            <select
              value={job.status}
              onChange={(e) => triggerStatusChangeConfirmation(e.target.value)}
              className="bg-transparent text-sm font-bold text-primary outline-none cursor-pointer uppercase"
            >
              <option value="draft">DRAFT</option>
              <option value="open">OPEN</option>
              <option value="closed">CLOSED</option>
              <option value="completed">COMPLETED</option>
            </select>
          </div>

          {job.status === "draft" && (
            <Button
              text="Delete Draft"
              variant="outline"
              color="secondary"
              size="sm"
              icon={<Trash2 size={16} />}
              className="border-red-500/30 text-red-500 hover:bg-red-500/10"
              onClick={triggerDeleteDraftConfirmation}
            />
          )}
        </div>
      </div>

      {/* Job Info Card */}
      <div className="bg-bg-alt border border-text/10 rounded-3xl p-6 md:p-8 shadow-sm flex flex-col gap-6">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-text">
            {job.title}
          </h1>
          <div className="flex flex-wrap items-center gap-4 mt-3">
            <span className="flex items-center gap-1.5 text-sm text-text-alt">
              <Briefcase size={16} />{" "}
              {job.employment_type?.replace("_", " ").toUpperCase() ||
                "FULL TIME"}
            </span>
            <span className="flex items-center gap-1.5 text-sm text-text-alt">
              <Calendar size={16} /> Deadline:{" "}
              {new Date(job.deadline).toLocaleDateString()}
            </span>
            <span className="flex items-center gap-1.5 text-sm text-text-alt">
              <MapPin size={16} /> {job.experience_years} Years Exp.
            </span>
          </div>
        </div>

        <div>
          <h3 className="text-sm font-bold text-text uppercase mb-2">
            Job Description
          </h3>
          <p className="text-sm text-text whitespace-pre-wrap leading-relaxed border-l-2 border-primary/20 pl-4 py-1">
            {job.description || "No description provided."}
          </p>
        </div>
      </div>

      {/* Candidates Section */}
      <div className="bg-bg-alt border border-text/10 rounded-3xl p-6 md:p-8 shadow-sm flex flex-col gap-4 mt-4">
        <div className="flex items-center justify-between border-b border-text/10 pb-4">
          <div className="flex items-center gap-2">
            <Users size={20} className="text-primary" />
            <h2 className="text-xl font-bold text-text">
              Applicants ({applications.length})
            </h2>
          </div>
        </div>

        {applications.length === 0 ? (
          <div className="text-center py-10 text-sm text-text-alt">
            No applications received for this job posting yet.
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {/* Map over actual candidate applications here */}
            {applications.map((app, index) => (
              <div
                key={index}
                className="p-4 rounded-xl border border-text/10 hover:border-primary/30 transition-colors flex justify-between items-center"
              >
                <div>
                  <h4 className="font-bold text-text">
                    {app.candidate_name || `Candidate #${index + 1}`}
                  </h4>
                  <p className="text-xs text-text-alt mt-1">
                    Applied:{" "}
                    {new Date(
                      app.applied_at || Date.now(),
                    ).toLocaleDateString()}
                  </p>
                </div>
                <Button
                  text="Review Application"
                  variant="outline"
                  color="primary"
                  size="sm"
                  onClick={() => {
                    /* Navigate to app review */
                  }}
                />
              </div>
            ))}
          </div>
        )}
      </div>

      <ConfirmationModal
        isOpen={modalConfig.isOpen}
        title={modalConfig.title}
        message={modalConfig.message}
        confirmText={modalConfig.confirmText}
        variant={modalConfig.variant}
        loading={modalLoading}
        onConfirm={modalConfig.onConfirm}
        onCancel={() => setModalConfig((prev) => ({ ...prev, isOpen: false }))}
      />
    </div>
  );
};

export default AdminJobPostingDetails;
