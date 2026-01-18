import type { ReactNode } from "react";
import Sidebar from "./Sidebar";

interface DashboardLayoutProps {
  children: ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  return (
    <div className="min-h-screen bg-gray-400">
      <Sidebar />
      <main className="pl-64">{children}</main>
    </div>
  );
};

export default DashboardLayout;
