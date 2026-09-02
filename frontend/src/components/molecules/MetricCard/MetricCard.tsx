import type { MetricCardProps } from '../../../types/metricCard.types';

const colorStyles = {
  primary: 'bg-primary/10 text-primary border-primary/20',
  secondary: 'bg-secondary/10 text-secondary border-secondary/20',
  accent: 'bg-accent/10 text-accent border-accent/20',
  success: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20',
};

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  icon,
  subtitle,
  color = 'primary',
  className = '',
}) => {
  return (
    <div
      className={`flex flex-1 min-w-60 md:max-w-9/28 items-center justify-between p-4 md:p-6 rounded-2xl bg-bg-alt border border-text/10 shadow-md hover:shadow-md hover:border-primary/30  transition-all duration-300 ${className}`}
    >
      <div className="flex flex-col gap-0.5 md:gap-1">
        <span className="text-xs font-semibold text-text-alt md:uppercase">{title}</span>
        <span className="text-lg md:text-2xl font-extrabold text-text tracking-tight mt-1">{value}</span>
        {subtitle && <span className="text-xs text-text-alt font-medium mt-1">{subtitle}</span>}
      </div>

      {icon && (
        <div className={`p-4 rounded-2xl border flex items-center justify-center shrink-0 ${colorStyles[color]}`}>
          {icon}
        </div>
      )}
    </div>
  );
};

export default MetricCard;
