import { useState } from "react";
import { Filter } from "lucide-react";
import DashboardLayout from "../components/layout/DashboardLayout";
import Header from "../components/layout/Header";
import ViolationsTable from "../components/violations/ViolationsTable";
import { Badge } from "../components/ui/Badge";
import { mockAuditInfo, mockViolations } from "../data/mockData";
import { cn } from "../lib/utils";
import type { Severity, ViolationStatus } from "../types/compliance";

type FilterType = "all" | Severity | ViolationStatus;

const filters: { value: FilterType; label: string }[] = [
  { value: "all", label: "All" },
  { value: "critical", label: "Critical" },
  { value: "high", label: "High" },
  { value: "medium", label: "Medium" },
  { value: "low", label: "Low" },
  { value: "open", label: "Open" },
  { value: "needs_review", label: "Needs Review" },
  { value: "resolved", label: "Resolved" },
];

const Violations = () => {
  const [activeFilter, setActiveFilter] = useState<FilterType>("all");

  const filteredViolations = mockViolations.filter((v) => {
    if (activeFilter === "all") return true;
    return v.severity === activeFilter || v.status === activeFilter;
  });

  return (
    <DashboardLayout>
      <Header
        title="Violations"
        auditStatus={mockAuditInfo.status}
        lastRun={mockAuditInfo.lastRun}
      />

      <div className="p-6">
        {/* Filters */}
        <div className="mb-6 flex items-center gap-3">
          <Filter className="h-4 w-4 text-muted-foreground" />
          <div className="flex flex-wrap gap-2">
            {filters.map((filter) => (
              <button
                key={filter.value}
                onClick={() => setActiveFilter(filter.value)}
                className={cn(
                  "rounded-lg border px-3 py-1.5 text-sm font-medium transition-colors",
                  activeFilter === filter.value
                    ? "border-primary bg-primary text-primary-foreground"
                    : "border-border bg-card text-muted-foreground hover:border-primary/50 hover:text-foreground"
                )}
              >
                {filter.label}
              </button>
            ))}
          </div>
        </div>

        {/* Summary */}
        <div className="mb-4 flex items-center gap-4">
          <p className="text-sm text-muted-foreground">
            Showing{" "}
            <span className="font-medium text-foreground">
              {filteredViolations.length}
            </span>{" "}
            of{" "}
            <span className="font-medium text-foreground">
              {mockViolations.length}
            </span>{" "}
            violations
          </p>
          <div className="flex gap-2">
            <Badge variant="critical">
              {mockViolations.filter((v) => v.severity === "critical").length}{" "}
              Critical
            </Badge>
            <Badge variant="high">
              {mockViolations.filter((v) => v.severity === "high").length} High
            </Badge>
            <Badge variant="medium">
              {mockViolations.filter((v) => v.severity === "medium").length}{" "}
              Medium
            </Badge>
            <Badge variant="low">
              {mockViolations.filter((v) => v.severity === "low").length} Low
            </Badge>
          </div>
        </div>

        {/* Table */}
        <ViolationsTable violations={filteredViolations} />
      </div>
    </DashboardLayout>
  );
};

export default Violations;
