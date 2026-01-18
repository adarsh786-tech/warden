import { Toaster } from "./components/ui/Toaster";
import { Toaster as Sonner } from "./components/ui/Sonner";
import { TooltipProvider } from "./components/ui/ToolTip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import Index from "./pages/Index";
import Audits from "./pages/Audit";
import Violations from "./pages/Violations";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";

import "./App.css";
import { Protect, RedirectToSignIn } from "@clerk/clerk-react";

const queryClient = new QueryClient();

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            {/* Public Route */}
            <Route path="/" element={<Landing />} />

            {/* 2. Protected Routes */}
            <Route
              path="/dashboard"
              element={
                <Protect fallback={<RedirectToSignIn />}>
                  <Index />
                </Protect>
              }
            />
            <Route
              path="/audits"
              element={
                <Protect fallback={<RedirectToSignIn />}>
                  <Audits />
                </Protect>
              }
            />
            <Route
              path="/violations"
              element={
                <Protect fallback={<RedirectToSignIn />}>
                  <Violations />
                </Protect>
              }
            />
            <Route
              path="/reports"
              element={
                <Protect fallback={<RedirectToSignIn />}>
                  <Reports />
                </Protect>
              }
            />
            <Route
              path="/settings"
              element={
                <Protect fallback={<RedirectToSignIn />}>
                  <Settings />
                </Protect>
              }
            />

            {/* Catch-all */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
