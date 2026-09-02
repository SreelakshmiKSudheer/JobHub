import React from "react";
import Button from "../../atoms/Button/Button";
import { MoveRight } from "lucide-react";
import { useNavigate } from "react-router";

type JobPostingViewCardProps = {
  id: string;
  status: string;
  department: string;
  title: string;
  designation: string;
  deadline: Date;
  description: string;
};

const JobPostingViewCard = ({
  id,
  status,
  department,
  title,
  designation,
  deadline,
  description,
}: JobPostingViewCardProps) => {
    const calculateDaysLeft = (deadline: Date): number => {
      const currentDate = new Date();
      const deadlineDate = new Date(deadline);
      const timeDiff = deadlineDate.getTime() - currentDate.getTime();
      const daysLeft = Math.ceil(timeDiff / (1000 * 3600 * 24));
      return daysLeft;
    }
    const daysLeft = calculateDaysLeft(deadline);

    const navigate = useNavigate();
  return (
    <div className="flex flex-col w-full md:max-w-9/28 justify-between p-6 rounded-2xl bg-bg-alt border border-text/10 shadow-md hover:shadow-lg hover:scale-105 transition-all">
      <div className="flex flex-col gap-1">
        <div className="flex items-center justify-between">
          <span className="px-3 py-1 rounded-full text-xs font-bold bg-primary/10 text-primary border border-primary/20">
            {status}
          </span>
          <span className="text-xs font-semibold text-text-alt">
            {department || "General"}
          </span>
        </div>

        <h3 className="text-md md:text-lg mt-2 font-bold text-primary line-clamp-1">
          {title}
        </h3>

        <div className="flex items-center gap-3 text-xs md:text-sm text-text">
          <span>{designation || "Specialist"}</span>
          <span>•</span>
          <span>{daysLeft} Days Left</span>
        </div>
        <div>
          <p className="text-xs md:text-sm text-text-alt mt-2 line-clamp-2">
            {description}
          </p>
        </div>
        {/* <hr className="bg-text/10 text-text/5 mt-3"></hr> */}
        <div className="flex mt-2 items-center justify-end">
          <Button
            text="View Details"
            variant="none"
            color="primary"
            size="xs"
            iconPosition="right"
            icon={<MoveRight size={16} />}
            textClassName="font-semibold"
            className="rounded-lg md:px-3 md:py-2 md:text-sm"
            onClick={() => {navigate(`/admin/job-postings/${id}`)}}
          />
        </div>
      </div>
    </div>
  );
};

export default JobPostingViewCard;
