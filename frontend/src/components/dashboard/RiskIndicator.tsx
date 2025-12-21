import { ShieldAlert, ShieldCheck, ShieldX, Shield } from "lucide-react";
import type { RiskLevel } from "../../types/compliance";
import { cn } from "../../lib/utils";

interface RiskIndicatorProps {
  level: RiskLevel;
}

const riskConfig = {
  critical: {
    label: "Critical Risk",
    description: "Immediate action required",
    icon: ShieldX,
    color: "text-severity-critical",
    bgColor: "bg-severity-critical/10",
    borderColor: "border-severity-critical",
  },
  high: {
    label: "High Risk",
    description: "Action needed soon",
    icon: ShieldAlert,
    color: "text-severity-high",
    bgColor: "bg-severity-high/10",
    borderColor: "border-severity-high",
  },
  medium: {
    label: "Medium Risk",
    description: "Review recommended",
    icon: Shield,
    color: "text-severity-medium",
    bgColor: "bg-severity-medium/10",
    borderColor: "border-severity-medium",
  },
  low: {
    label: "Low Risk",
    description: "Minor improvements possible",
    icon: ShieldCheck,
    color: "text-severity-low",
    bgColor: "bg-severity-low/10",
    borderColor: "border-severity-low",
  },
  minimal: {
    label: "Minimal Risk",
    description: "Excellent compliance posture",
    icon: ShieldCheck,
    color: "text-success",
    bgColor: "bg-success/10",
    borderColor: "border-success",
  },
};

const RiskIndicator = ({ level }: RiskIndicatorProps) => {
  const config = riskConfig[level];
  const Icon = config.icon;

  return (
    <div
      className={cn(
        "flex items-center gap-4 rounded-lg border-l-4 bg-card p-5 shadow-sm",
        config.borderColor
      )}
    >
      <div
        className={cn(
          "flex h-12 w-12 items-center justify-center rounded-lg",
          config.bgColor
        )}
      >
        <Icon className={cn("h-6 w-6", config.color)} />
      </div>
      <div>
        <p className="text-sm font-medium text-muted-foreground">
          Overall Risk Level
        </p>
        <p className={cn("text-xl font-semibold", config.color)}>
          {config.label}
        </p>
        <p className="text-xs text-muted-foreground">{config.description}</p>
      </div>
    </div>
  );
};

export default RiskIndicator;
