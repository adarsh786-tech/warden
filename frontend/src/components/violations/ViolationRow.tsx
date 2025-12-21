import { ChevronDown, ChevronRight } from "lucide-react";
import { Badge } from "../../components/ui/Badge";
import type { Violation } from "../../types/compliance";
import { cn } from "../../lib/utils";

interface ViolationRowProps {
  violation: Violation;
  isExpanded: boolean;
  onToggle: () => void;
}

const statusLabels = {
  open: "Open",
  needs_review: "Needs Review",
  resolved: "Resolved",
  dismissed: "Dismissed",
};

const statusStyles = {
  open: "bg-severity-critical/10 text-severity-critical",
  needs_review: "bg-warning/10 text-warning",
  resolved: "bg-success/10 text-success",
  dismissed: "bg-muted text-muted-foreground",
};

const ViolationRow = ({
  violation,
  isExpanded,
  onToggle,
}: ViolationRowProps) => {
  return (
    <div className="border-b border-border last:border-b-0">
      <button
        onClick={onToggle}
        className="flex w-full items-center gap-4 px-4 py-4 text-left transition-colors hover:bg-muted/50"
      >
        <div className="flex h-6 w-6 items-center justify-center text-muted-foreground">
          {isExpanded ? (
            <ChevronDown className="h-4 w-4" />
          ) : (
            <ChevronRight className="h-4 w-4" />
          )}
        </div>

        <div className="w-24 shrink-0">
          <code className="rounded bg-muted px-2 py-1 text-xs font-medium text-muted-foreground">
            {violation.ruleId}
          </code>
        </div>

        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium text-foreground">
            {violation.title}
          </p>
          <p className="truncate text-xs text-muted-foreground">
            {violation.category}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Badge variant={violation.severity}>{violation.severity}</Badge>
          <div
            className={cn(
              "rounded-full px-2.5 py-0.5 text-xs font-medium",
              statusStyles[violation.status]
            )}
          >
            {statusLabels[violation.status]}
          </div>
        </div>
      </button>

      {isExpanded && (
        <div className="animate-fade-in border-t border-border bg-muted/30 px-14 py-5">
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Evidence Section */}
            <div className="space-y-2">
              <h4 className="text-sm font-semibold text-foreground">
                Evidence
              </h4>
              <div className="rounded-lg border border-border bg-card p-4">
                <p className="font-mono text-xs leading-relaxed text-muted-foreground">
                  {violation.evidence}
                </p>
              </div>
            </div>

            {/* Agent Reasoning Section */}
            <div className="space-y-2">
              <h4 className="text-sm font-semibold text-foreground">
                Agent Reasoning
              </h4>
              <div className="rounded-lg border border-border bg-card p-4">
                <p className="text-sm leading-relaxed text-muted-foreground">
                  {violation.reasoning}
                </p>
              </div>
            </div>

            {/* Remediation Section */}
            <div className="space-y-2">
              <h4 className="text-sm font-semibold text-foreground">
                Suggested Remediation
              </h4>
              <div className="rounded-lg border border-border bg-card p-4">
                <pre className="whitespace-pre-wrap text-sm leading-relaxed text-muted-foreground">
                  {violation.remediation}
                </pre>
              </div>
            </div>

            {/* Confidence & Metadata */}
            <div className="space-y-2">
              <h4 className="text-sm font-semibold text-foreground">
                Metadata
              </h4>
              <div className="rounded-lg border border-border bg-card p-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-muted-foreground">Confidence</p>
                    <div className="mt-1 flex items-center gap-2">
                      <div className="h-2 flex-1 rounded-full bg-secondary">
                        <div
                          className="h-2 rounded-full bg-primary"
                          style={{ width: `${violation.confidence}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium text-foreground">
                        {violation.confidence}%
                      </span>
                    </div>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Detected</p>
                    <p className="mt-1 text-sm font-medium text-foreground">
                      {new Date(violation.detectedAt).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Reflection Section (if available) */}
            {violation.reflection && (
              <div className="space-y-2 lg:col-span-2">
                <h4 className="text-sm font-semibold text-foreground">
                  Audit Trail & Reflection
                </h4>
                <div className="rounded-lg border border-border bg-card p-4">
                  <div className="space-y-4">
                    <div>
                      <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                        Initial Finding
                      </p>
                      <p className="mt-1 text-sm text-muted-foreground">
                        {violation.reflection.initialFinding}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                        Reflection Notes
                      </p>
                      <p className="mt-1 text-sm text-muted-foreground">
                        {violation.reflection.reflectionNotes}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                        Final Decision
                      </p>
                      <p className="mt-1 text-sm font-medium text-foreground">
                        {violation.reflection.finalDecision}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ViolationRow;
