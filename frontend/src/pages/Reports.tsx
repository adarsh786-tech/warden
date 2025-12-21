import { FileText, Download, Calendar } from "lucide-react";
import DashboardLayout from "../components/layout/DashboardLayout";
import Header from "../components/layout/Header";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { mockAuditInfo, mockMetrics, mockViolations } from "../data/mockData";

const Reports = () => {
  const criticalViolations = mockViolations.filter(
    (v) => v.severity === "critical"
  );
  const highViolations = mockViolations.filter((v) => v.severity === "high");
  const otherViolations = mockViolations.filter(
    (v) => v.severity !== "critical" && v.severity !== "high"
  );

  return (
    <DashboardLayout>
      <Header
        title="Compliance Report"
        auditStatus={mockAuditInfo.status}
        lastRun={mockAuditInfo.lastRun}
      />

      <div className="p-6">
        {/* Report Header */}
        <div className="mb-8 rounded-lg border border-border bg-card p-6 shadow-sm">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <FileText className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-foreground">
                  Compliance Audit Report
                </h2>
                <div className="mt-1 flex items-center gap-3 text-sm text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    {new Date(mockAuditInfo.lastRun).toLocaleDateString(
                      "en-US",
                      {
                        month: "long",
                        day: "numeric",
                        year: "numeric",
                      }
                    )}
                  </span>
                  <span>•</span>
                  <span>Duration: {mockAuditInfo.duration}</span>
                </div>
              </div>
            </div>

            <div className="flex gap-2">
              <Button variant="outline" className="gap-2">
                <Download className="h-4 w-4" />
                Export PDF
              </Button>
              <Button variant="outline" className="gap-2">
                <Download className="h-4 w-4" />
                Export JSON
              </Button>
            </div>
          </div>
        </div>

        {/* Executive Summary */}
        <section className="mb-8">
          <h3 className="mb-4 text-lg font-semibold text-foreground">
            Executive Summary
          </h3>
          <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
            <div className="mb-6 grid grid-cols-2 gap-6 md:grid-cols-4">
              <div className="text-center">
                <p className="text-3xl font-bold text-foreground">
                  {mockMetrics.complianceScore}%
                </p>
                <p className="text-sm text-muted-foreground">
                  Compliance Score
                </p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-severity-critical">
                  {mockMetrics.criticalIssues}
                </p>
                <p className="text-sm text-muted-foreground">Critical Issues</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-foreground">
                  {mockAuditInfo.rulesEvaluated}
                </p>
                <p className="text-sm text-muted-foreground">Rules Evaluated</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-foreground">
                  {mockAuditInfo.artifactsScanned}
                </p>
                <p className="text-sm text-muted-foreground">
                  Artifacts Scanned
                </p>
              </div>
            </div>
            <p className="text-sm leading-relaxed text-muted-foreground">
              This audit identified {mockMetrics.totalViolations} compliance
              violations across {mockAuditInfo.artifactsScanned} software
              artifacts. The overall risk level is assessed as{" "}
              <span className="font-medium text-warning">Medium</span>,
              primarily due to
              {mockMetrics.criticalIssues} critical findings related to data
              protection and secrets management. Immediate remediation is
              recommended for all critical and high-severity issues.
            </p>
          </div>
        </section>

        {/* Findings by Severity */}
        <section className="mb-8">
          <h3 className="mb-4 text-lg font-semibold text-foreground">
            Findings by Severity
          </h3>

          {/* Critical Findings */}
          {criticalViolations.length > 0 && (
            <div className="mb-4 rounded-lg border border-severity-critical/20 bg-severity-critical/5 p-4">
              <h4 className="mb-3 flex items-center gap-2 font-semibold text-severity-critical">
                <Badge variant="critical">Critical</Badge>
                {criticalViolations.length} Finding
                {criticalViolations.length !== 1 ? "s" : ""}
              </h4>
              <div className="space-y-3">
                {criticalViolations.map((v) => (
                  <div
                    key={v.id}
                    className="rounded-md border border-border bg-card p-3"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <code className="text-xs text-muted-foreground">
                          {v.ruleId}
                        </code>
                        <p className="font-medium text-foreground">{v.title}</p>
                      </div>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      {v.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* High Findings */}
          {highViolations.length > 0 && (
            <div className="mb-4 rounded-lg border border-severity-high/20 bg-severity-high/5 p-4">
              <h4 className="mb-3 flex items-center gap-2 font-semibold text-severity-high">
                <Badge variant="high">High</Badge>
                {highViolations.length} Finding
                {highViolations.length !== 1 ? "s" : ""}
              </h4>
              <div className="space-y-3">
                {highViolations.map((v) => (
                  <div
                    key={v.id}
                    className="rounded-md border border-border bg-card p-3"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <code className="text-xs text-muted-foreground">
                          {v.ruleId}
                        </code>
                        <p className="font-medium text-foreground">{v.title}</p>
                      </div>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      {v.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Other Findings */}
          {otherViolations.length > 0 && (
            <div className="rounded-lg border border-border bg-card p-4">
              <h4 className="mb-3 flex items-center gap-2 font-semibold text-foreground">
                Other Findings
                <span className="text-sm font-normal text-muted-foreground">
                  ({otherViolations.length} items)
                </span>
              </h4>
              <div className="space-y-2">
                {otherViolations.map((v) => (
                  <div
                    key={v.id}
                    className="flex items-center justify-between rounded-md border border-border p-3"
                  >
                    <div className="flex items-center gap-3">
                      <Badge variant={v.severity}>{v.severity}</Badge>
                      <div>
                        <code className="mr-2 text-xs text-muted-foreground">
                          {v.ruleId}
                        </code>
                        <span className="text-sm text-foreground">
                          {v.title}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      </div>
    </DashboardLayout>
  );
};

export default Reports;
