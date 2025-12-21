import { cn } from "../../lib/utils";

interface ComplianceScoreProps {
  score: number;
}

const ComplianceScore = ({ score }: ComplianceScoreProps) => {
  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-success";
    if (score >= 70) return "text-warning";
    return "text-severity-critical";
  };

  const getScoreRingColor = (score: number) => {
    if (score >= 90) return "stroke-success";
    if (score >= 70) return "stroke-warning";
    return "stroke-severity-critical";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 90) return "Excellent";
    if (score >= 80) return "Good";
    if (score >= 70) return "Fair";
    if (score >= 60) return "Needs Attention";
    return "Critical";
  };

  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
      <h3 className="mb-4 text-sm font-medium text-muted-foreground">
        Compliance Score
      </h3>

      <div className="flex items-center gap-6">
        <div className="relative h-32 w-32">
          <svg className="h-32 w-32 -rotate-90 transform">
            <circle
              cx="64"
              cy="64"
              r="45"
              fill="none"
              strokeWidth="10"
              className="stroke-secondary"
            />
            <circle
              cx="64"
              cy="64"
              r="45"
              fill="none"
              strokeWidth="10"
              strokeLinecap="round"
              className={cn(
                "transition-all duration-500",
                getScoreRingColor(score)
              )}
              style={{
                strokeDasharray: circumference,
                strokeDashoffset,
              }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className={cn("text-3xl font-bold", getScoreColor(score))}>
              {score}%
            </span>
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <span className={cn("text-lg font-semibold", getScoreColor(score))}>
            {getScoreLabel(score)}
          </span>
          <p className="text-sm text-muted-foreground">
            Based on {156} rules evaluated across {42} artifacts
          </p>
        </div>
      </div>
    </div>
  );
};

export default ComplianceScore;
