import { useState } from "react";
import ViolationRow from "./ViolationRow";
import type { Violation } from "../../types/compliance";

interface ViolationsTableProps {
  violations: Violation[];
}

const ViolationsTable = ({ violations }: ViolationsTableProps) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const handleToggle = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <div className="rounded-lg border border-border bg-card shadow-sm">
      <div className="border-b border-border px-4 py-3">
        <div className="flex items-center gap-4">
          <div className="w-6" />
          <div className="w-24 text-xs font-medium uppercase tracking-wider text-muted-foreground">
            Rule ID
          </div>
          <div className="flex-1 text-xs font-medium uppercase tracking-wider text-muted-foreground">
            Issue
          </div>
          <div className="w-32 text-right text-xs font-medium uppercase tracking-wider text-muted-foreground">
            Severity / Status
          </div>
        </div>
      </div>

      <div className="divide-y divide-border">
        {violations.map((violation) => (
          <ViolationRow
            key={violation.id}
            violation={violation}
            isExpanded={expandedId === violation.id}
            onToggle={() => handleToggle(violation.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default ViolationsTable;
