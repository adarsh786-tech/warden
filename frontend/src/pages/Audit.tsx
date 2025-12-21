import { Clock, CheckCircle2, PlayCircle, FileSearch } from "lucide-react";
import DashboardLayout from "../components/layout/DashboardLayout";
import Header from "../components/layout/Header";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { mockAuditInfo } from "../data/mockData";

const auditHistory = [
  {
    id: "audit-001",
    name: "Full Compliance Scan",
    status: "completed",
    startedAt: "2024-01-15T14:28:00Z",
    completedAt: "2024-01-15T14:32:00Z",
    duration: "4m 23s",
    rulesEvaluated: 156,
    artifactsScanned: 42,
    violationsFound: 13,
  },
  {
    id: "audit-002",
    name: "Security Rules Only",
    status: "completed",
    startedAt: "2024-01-14T10:00:00Z",
    completedAt: "2024-01-14T10:03:00Z",
    duration: "2m 45s",
    rulesEvaluated: 48,
    artifactsScanned: 42,
    violationsFound: 6,
  },
  {
    id: "audit-003",
    name: "Documentation Check",
    status: "completed",
    startedAt: "2024-01-12T16:30:00Z",
    completedAt: "2024-01-12T16:31:00Z",
    duration: "1m 12s",
    rulesEvaluated: 24,
    artifactsScanned: 15,
    violationsFound: 2,
  },
];

const Audits = () => {
  return (
    <DashboardLayout>
      <Header
        title="Audits"
        auditStatus={mockAuditInfo.status}
        lastRun={mockAuditInfo.lastRun}
      />

      <div className="p-6">
        {/* Actions */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">
              Audit History
            </h2>
            <p className="text-sm text-muted-foreground">
              View past audits and their results
            </p>
          </div>
          <Button className="gap-2">
            <PlayCircle className="h-4 w-4" />
            Run New Audit
          </Button>
        </div>

        {/* Audit List */}
        <div className="space-y-4">
          {auditHistory.map((audit) => (
            <div
              key={audit.id}
              className="rounded-lg border border-border bg-card p-5 shadow-sm transition-shadow hover:shadow-md"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                    <FileSearch className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">
                      {audit.name}
                    </h3>
                    <div className="mt-1 flex items-center gap-3 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3.5 w-3.5" />
                        {new Date(audit.startedAt).toLocaleDateString("en-US", {
                          month: "short",
                          day: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </span>
                      <span>•</span>
                      <span>Duration: {audit.duration}</span>
                    </div>
                  </div>
                </div>

                <Badge variant="success" className="gap-1.5">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  Completed
                </Badge>
              </div>

              <div className="mt-4 grid grid-cols-3 gap-4 rounded-lg bg-muted/50 p-4">
                <div className="text-center">
                  <p className="text-2xl font-semibold text-foreground">
                    {audit.rulesEvaluated}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Rules Evaluated
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-semibold text-foreground">
                    {audit.artifactsScanned}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Artifacts Scanned
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-semibold text-severity-critical">
                    {audit.violationsFound}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Violations Found
                  </p>
                </div>
              </div>

              <div className="mt-4 flex justify-end gap-2">
                <Button variant="outline" size="sm">
                  View Details
                </Button>
                <Button variant="outline" size="sm">
                  Download Report
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Audits;
