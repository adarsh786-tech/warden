import DashboardLayout from "../components/layout/DashboardLayout";
import Header from "../components/layout/Header";
import { Switch } from "../components/ui/Switch";
import { Label } from "../components/ui/Label";
import { Button } from "../components/ui/Button";
import { mockAuditInfo } from "../data/mockData";

const Settings = () => {
  return (
    <DashboardLayout>
      <Header
        title="Settings"
        auditStatus={mockAuditInfo.status}
        lastRun={mockAuditInfo.lastRun}
      />

      <div className="p-6">
        <div className="max-w-2xl space-y-8">
          {/* Audit Configuration */}
          <section>
            <h2 className="mb-4 text-lg font-semibold text-foreground">
              Audit Configuration
            </h2>
            <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <Label htmlFor="auto-audit" className="text-foreground">
                      Automatic Audits
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Run compliance audits automatically on repository changes
                    </p>
                  </div>
                  <Switch id="auto-audit" defaultChecked />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <Label htmlFor="deep-scan" className="text-foreground">
                      Deep Scan Mode
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Include transitive dependencies in security analysis
                    </p>
                  </div>
                  <Switch id="deep-scan" defaultChecked />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <Label htmlFor="reflection" className="text-foreground">
                      Agent Reflection
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Enable multi-step reasoning for complex findings
                    </p>
                  </div>
                  <Switch id="reflection" defaultChecked />
                </div>
              </div>
            </div>
          </section>

          {/* Notification Settings */}
          <section>
            <h2 className="mb-4 text-lg font-semibold text-foreground">
              Notifications
            </h2>
            <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <Label htmlFor="email-critical" className="text-foreground">
                      Critical Issue Alerts
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Receive email notifications for critical violations
                    </p>
                  </div>
                  <Switch id="email-critical" defaultChecked />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <Label htmlFor="weekly-digest" className="text-foreground">
                      Weekly Digest
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Receive a weekly summary of compliance status
                    </p>
                  </div>
                  <Switch id="weekly-digest" />
                </div>
              </div>
            </div>
          </section>

          {/* Danger Zone */}
          <section>
            <h2 className="mb-4 text-lg font-semibold text-foreground">
              Data Management
            </h2>
            <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-foreground">Clear Audit History</Label>
                  <p className="text-sm text-muted-foreground">
                    Remove all past audit records and findings
                  </p>
                </div>
                <Button variant="destructive" size="sm">
                  Clear History
                </Button>
              </div>
            </div>
          </section>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Settings;
