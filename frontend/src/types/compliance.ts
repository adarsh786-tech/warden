export type Severity = "critical" | "high" | "medium" | "low";
export type ViolationStatus =
  | "open"
  | "needs_review"
  | "resolved"
  | "dismissed";
export type AuditStatus = "completed" | "in_progress" | "pending" | "failed";
export type RiskLevel = "critical" | "high" | "medium" | "low" | "minimal";

export interface Violation {
  id: string;
  ruleId: string;
  title: string;
  description: string;
  severity: Severity;
  status: ViolationStatus;
  evidence: string;
  reasoning: string;
  remediation: string;
  confidence: number;
  category: string;
  detectedAt: string;
  reflection?: {
    initialFinding: string;
    reflectionNotes: string;
    finalDecision: string;
  };
}

export interface ComplianceMetrics {
  complianceScore: number;
  criticalIssues: number;
  moderateIssues: number;
  missingArtifacts: number;
  totalViolations: number;
  riskLevel: RiskLevel;
}

export interface AuditInfo {
  status: AuditStatus;
  lastRun: string;
  duration: string;
  rulesEvaluated: number;
  artifactsScanned: number;
}
