import type { ReactNode } from "react";
import { cn } from "../../lib/utils";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: ReactNode;
  trend?: "up" | "down" | "neutral";
  variant?: "default" | "success" | "warning" | "critical";
}

const variantStyles = {
  default: "border-border",
  success: "border-l-4 border-l-success border-t-0 border-r-0 border-b-0",
  warning: "border-l-4 border-l-warning border-t-0 border-r-0 border-b-0",
  critical:
    "border-l-4 border-l-severity-critical border-t-0 border-r-0 border-b-0",
};

const iconVariantStyles = {
  default: "bg-secondary text-secondary-foreground",
  success: "bg-success/10 text-success",
  warning: "bg-warning/10 text-warning",
  critical: "bg-severity-critical/10 text-severity-critical",
};

const MetricCard = ({
  title,
  value,
  subtitle,
  icon,
  variant = "default",
}: MetricCardProps) => {
  return (
    <div
      className={cn(
        "rounded-lg border bg-card p-5 shadow-sm transition-shadow hover:shadow-md",
        variantStyles[variant]
      )}
    >
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <p className="text-3xl font-semibold tracking-tight text-card-foreground">
            {value}
          </p>
          {subtitle && (
            <p className="text-xs text-muted-foreground">{subtitle}</p>
          )}
        </div>
        <div
          className={cn(
            "flex h-10 w-10 items-center justify-center rounded-lg",
            iconVariantStyles[variant]
          )}
        >
          {icon}
        </div>
      </div>
    </div>
  );
};

export default MetricCard;
