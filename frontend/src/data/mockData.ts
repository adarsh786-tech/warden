import type {
  Violation,
  ComplianceMetrics,
  AuditInfo,
} from "../types/compliance";

export const mockMetrics: ComplianceMetrics = {
  complianceScore: 78,
  criticalIssues: 3,
  moderateIssues: 8,
  missingArtifacts: 2,
  totalViolations: 13,
  riskLevel: "medium",
};

export const mockAuditInfo: AuditInfo = {
  status: "completed",
  lastRun: "2024-01-15T14:32:00Z",
  duration: "4m 23s",
  rulesEvaluated: 156,
  artifactsScanned: 42,
};

export const mockViolations: Violation[] = [
  {
    id: "v-001",
    ruleId: "SEC-007",
    title: "Missing encryption at rest for sensitive data storage",
    description:
      "The application stores sensitive user data without implementing encryption at rest, violating data protection requirements.",
    severity: "critical",
    status: "open",
    category: "Data Protection",
    evidence:
      '"userData is stored in plaintext format in the local database without any encryption mechanism applied." - Found in database.config.ts, line 47',
    reasoning:
      "The agent identified that the database configuration explicitly disables encryption (encryption: false) for the user_data collection. This configuration combined with the storage of PII fields (email, phone, address) creates a critical compliance gap.",
    remediation:
      "1. Enable AES-256 encryption for the user_data collection\n2. Implement key rotation policy\n3. Update database.config.ts to set encryption: true\n4. Audit existing data and re-encrypt if necessary",
    confidence: 94,
    detectedAt: "2024-01-15T14:28:00Z",
    reflection: {
      initialFinding:
        "Detected unencrypted storage configuration for user data collection.",
      reflectionNotes:
        "Cross-referenced with compliance rule SEC-007 which mandates encryption at rest for all PII. Verified that the stored fields (email, phone, address) qualify as PII under GDPR and CCPA definitions.",
      finalDecision:
        "Confirmed as Critical violation. Unencrypted PII storage poses significant regulatory and security risk.",
    },
  },
  {
    id: "v-002",
    ruleId: "AUTH-012",
    title: "Inadequate session timeout configuration",
    description:
      "User sessions remain active indefinitely without automatic timeout, creating security vulnerabilities.",
    severity: "high",
    status: "needs_review",
    category: "Authentication",
    evidence:
      '"sessionTimeout: -1" found in auth.config.js - indicates sessions never expire automatically.',
    reasoning:
      "The authentication configuration sets session timeout to -1, which disables automatic session expiration. This violates security best practices and compliance requirements for session management.",
    remediation:
      "1. Set sessionTimeout to 30 minutes (1800000ms) for standard users\n2. Implement idle timeout of 15 minutes\n3. Add session refresh mechanism for active users",
    confidence: 98,
    detectedAt: "2024-01-15T14:25:00Z",
  },
  {
    id: "v-003",
    ruleId: "LOG-003",
    title: "Insufficient audit logging for administrative actions",
    description:
      "Administrative actions are not being logged with required detail level for compliance audit trails.",
    severity: "high",
    status: "open",
    category: "Audit Logging",
    evidence:
      "Admin controller functions lack @AuditLog decorators. Only 3 of 12 admin endpoints have logging enabled.",
    reasoning:
      "The agent scanned all admin controller files and found that audit logging decorators are inconsistently applied. Critical operations like user deletion and permission changes have no audit trail.",
    remediation:
      "1. Add @AuditLog decorator to all admin controller methods\n2. Include user context, timestamp, and action details\n3. Ensure logs are written to immutable storage",
    confidence: 91,
    detectedAt: "2024-01-15T14:26:00Z",
  },
  {
    id: "v-004",
    ruleId: "SEC-015",
    title: "API keys exposed in client-side code",
    description:
      "Sensitive API keys are bundled into the client-side JavaScript, making them accessible to end users.",
    severity: "critical",
    status: "open",
    category: "Secrets Management",
    evidence:
      "STRIPE_SECRET_KEY found in bundle.js after build process. Variable referenced in payment.service.ts line 23.",
    reasoning:
      "Build analysis revealed that environment variables prefixed with NEXT_PUBLIC_ include a secret key that should remain server-side only. This exposes the payment provider credentials.",
    remediation:
      "1. Move STRIPE_SECRET_KEY to server-side only environment\n2. Create API route for payment processing\n3. Audit all NEXT_PUBLIC_ variables for sensitive data\n4. Rotate compromised API keys immediately",
    confidence: 99,
    detectedAt: "2024-01-15T14:24:00Z",
  },
  {
    id: "v-005",
    ruleId: "DOC-001",
    title: "Missing security architecture documentation",
    description:
      "Required security architecture documentation is not present in the repository.",
    severity: "medium",
    status: "needs_review",
    category: "Documentation",
    evidence:
      "Expected file docs/security-architecture.md not found. No alternative documentation detected in /docs or /security folders.",
    reasoning:
      "Compliance requirements mandate documented security architecture including data flow diagrams, encryption specifications, and access control matrix. None of these artifacts were found.",
    remediation:
      "1. Create docs/security-architecture.md\n2. Include data flow diagrams\n3. Document encryption standards in use\n4. Add access control matrix for all user roles",
    confidence: 100,
    detectedAt: "2024-01-15T14:30:00Z",
  },
  {
    id: "v-006",
    ruleId: "DEP-008",
    title: "Outdated dependency with known vulnerability",
    description:
      "The lodash package version 4.17.15 has a known prototype pollution vulnerability (CVE-2020-8203).",
    severity: "medium",
    status: "open",
    category: "Dependencies",
    evidence:
      'package.json specifies "lodash": "4.17.15". Known vulnerable to CVE-2020-8203 (CVSS 7.4).',
    reasoning:
      "Dependency analysis identified lodash at version 4.17.15 which is affected by a high-severity prototype pollution vulnerability. The current version is significantly behind the patched release.",
    remediation:
      "1. Update lodash to version 4.17.21 or later\n2. Run npm audit to verify fix\n3. Test application functionality after update",
    confidence: 100,
    detectedAt: "2024-01-15T14:29:00Z",
  },
  {
    id: "v-007",
    ruleId: "ACC-002",
    title: "Missing role-based access control on API endpoints",
    description:
      "Several API endpoints lack proper RBAC implementation, allowing unauthorized access to protected resources.",
    severity: "high",
    status: "open",
    category: "Access Control",
    evidence:
      "/api/admin/users endpoint accessible without admin role check. Middleware chain missing @RequireRole decorator.",
    reasoning:
      "Analysis of route handlers revealed that admin-prefixed routes do not consistently enforce role requirements. The /users endpoint can be accessed by any authenticated user.",
    remediation:
      '1. Add @RequireRole("admin") decorator to all /api/admin/* routes\n2. Implement middleware to validate roles before handler execution\n3. Add integration tests for role enforcement',
    confidence: 96,
    detectedAt: "2024-01-15T14:27:00Z",
  },
  {
    id: "v-008",
    ruleId: "PRIV-004",
    title: "Privacy policy link missing from registration flow",
    description:
      "User registration does not include required privacy policy acknowledgment.",
    severity: "low",
    status: "resolved",
    category: "Privacy",
    evidence:
      "Registration form component (RegisterForm.tsx) lacks privacy policy checkbox or link.",
    reasoning:
      "GDPR and CCPA require explicit user consent and acknowledgment of privacy policy during data collection. The registration form collects PII without this required disclosure.",
    remediation:
      "1. Add privacy policy link to registration form\n2. Implement checkbox for explicit consent\n3. Store consent timestamp in user record",
    confidence: 100,
    detectedAt: "2024-01-15T14:31:00Z",
  },
];
