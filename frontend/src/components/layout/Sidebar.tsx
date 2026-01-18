import { NavLink, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  FileSearch,
  AlertTriangle,
  FileText,
  Settings,
  Shield,
  HomeIcon,
} from "lucide-react";
import { cn } from "../../lib/utils";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Audits", href: "/audits", icon: FileSearch },
  { name: "Violations", href: "/violations", icon: AlertTriangle },
  { name: "Reports", href: "/reports", icon: FileText },
  { name: "Settings", href: "/settings", icon: Settings },
  { name: "Home", href: "/", icon: HomeIcon },
];

const Sidebar = () => {
  const location = useLocation();

  return (
    <aside className="fixed inset-y-0 left-0 z-50 flex w-64 flex-col bg-sidebar">
      {/* Logo */}
      <div className="flex h-16 items-center gap-3 border-b border-sidebar-border px-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-sidebar-primary">
          <Shield className="h-5 w-5 text-sidebar-primary-foreground" />
        </div>
        <div className="flex flex-col">
          <span className="text-sm font-semibold text-sidebar-accent-foreground">
            ComplianceAI
          </span>
          <span className="text-xs text-sidebar-muted">Audit Agent</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <NavLink
              key={item.name}
              to={item.href}
              className={cn(
                "group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                isActive
                  ? "bg-sidebar-accent text-sidebar-accent-foreground"
                  : "text-sidebar-foreground hover:bg-sidebar-accent/50 hover:text-sidebar-accent-foreground"
              )}
            >
              <item.icon
                className={cn(
                  "h-5 w-5 shrink-0",
                  isActive
                    ? "text-sidebar-primary"
                    : "text-sidebar-muted group-hover:text-sidebar-foreground"
                )}
              />
              {item.name}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-sidebar-border p-4">
        <div className="rounded-lg bg-sidebar-accent/50 px-3 py-2">
          <p className="text-xs text-sidebar-muted">Version 1.2.4</p>
          <p className="text-xs text-sidebar-muted">Last sync: 2 min ago</p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
