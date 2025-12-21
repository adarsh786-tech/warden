import {
  AlertTriangle,
  AlertCircle,
  FileQuestion,
  BarChart3,
} from "lucide-react";
import DashboardLayout from "../components/layout/DashboardLayout";
import Header from "../components/layout/Header";
import MetricCard from "../components/dashboard/MetricCard";
import ComplianceScore from "../components/dashboard/ComplianceScore";
import RiskIndicator from "../components/dashboard/RiskIndicator";
import ViolationsTable from "../components/violations/ViolationsTable";
import { mockMetrics, mockAuditInfo, mockViolations } from "../data/mockData";

const Index = () => {
  // Filter to show only open/needs_review violations
  const activeViolations = mockViolations.filter(
    (v) => v.status === "open" || v.status === "needs_review"
  );

  return (
    <DashboardLayout>
      <Header
        title="Compliance Overview"
        auditStatus={mockAuditInfo.status}
        lastRun={mockAuditInfo.lastRun}
      />

      <div className="p-6">
        {/* Top Metrics Grid */}
        <div className="mb-6 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            title="Critical Issues"
            value={mockMetrics.criticalIssues}
            subtitle="Require immediate attention"
            icon={<AlertTriangle className="h-5 w-5" />}
            variant="critical"
          />
          <MetricCard
            title="Moderate Issues"
            value={mockMetrics.moderateIssues}
            subtitle="Review recommended"
            icon={<AlertCircle className="h-5 w-5" />}
            variant="warning"
          />
          <MetricCard
            title="Missing Artifacts"
            value={mockMetrics.missingArtifacts}
            subtitle="Documentation gaps"
            icon={<FileQuestion className="h-5 w-5" />}
            variant="default"
          />
          <MetricCard
            title="Total Violations"
            value={mockMetrics.totalViolations}
            subtitle="Across all categories"
            icon={<BarChart3 className="h-5 w-5" />}
            variant="default"
          />
        </div>

        {/* Score and Risk Row */}
        <div className="mb-8 grid gap-4 lg:grid-cols-2">
          <ComplianceScore score={mockMetrics.complianceScore} />
          <RiskIndicator level={mockMetrics.riskLevel} />
        </div>

        {/* Violations Section */}
        <section>
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-foreground">
                Active Violations
              </h2>
              <p className="text-sm text-muted-foreground">
                {activeViolations.length} issues requiring attention
              </p>
            </div>
          </div>

          <ViolationsTable violations={activeViolations} />
        </section>
      </div>
    </DashboardLayout>
  );
};

export default Index;
