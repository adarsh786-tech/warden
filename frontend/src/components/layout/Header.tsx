import { CheckCircle2, Clock, AlertCircle, Loader2 } from "lucide-react";
import { Badge } from "../../components/ui/Badge";
import type { AuditStatus } from "../../types/compliance";
import { cn } from "../../lib/utils";

interface HeaderProps {
  title: string;
  auditStatus: AuditStatus;
  lastRun?: string;
}

const statusConfig = {
  completed: {
    label: "Completed",
    icon: CheckCircle2,
    variant: "success" as const,
  },
  in_progress: {
    label: "In Progress",
    icon: Loader2,
    variant: "info" as const,
  },
  pending: {
    label: "Pending",
    icon: Clock,
    variant: "warning" as const,
  },
  failed: {
    label: "Failed",
    icon: AlertCircle,
    variant: "critical" as const,
  },
};

const Header = ({ title, auditStatus, lastRun }: HeaderProps) => {
  const status = statusConfig[auditStatus];
  const StatusIcon = status.icon;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
      <div className="flex h-16 items-center justify-between px-6">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-semibold text-foreground">{title}</h1>
        </div>

        <div className="flex items-center gap-4">
          {lastRun && (
            <span className="text-sm text-muted-foreground">
              Last audit run: {formatDate(lastRun)}
            </span>
          )}
          <Badge variant={status.variant} className="gap-1.5">
            <StatusIcon
              className={cn(
                "h-3.5 w-3.5",
                auditStatus === "in_progress" && "animate-spin"
              )}
            />
            Audit: {status.label}
          </Badge>
        </div>
      </div>
    </header>
  );
};

export default Header;
