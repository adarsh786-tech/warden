import { Link } from "react-router-dom";
import { Button } from "../components/ui/Button";
import {
  Shield,
  CheckCircle,
  FileText,
  Lock,
  ArrowRight,
  Zap,
  BarChart3,
  Users,
  Globe,
  Clock,
  TrendingUp,
  Award,
  Building2,
} from "lucide-react";

import {
  SignedIn,
  SignedOut,
  SignInButton,
  UserButton,
} from "@clerk/clerk-react";

const Landing = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b border-border/40 bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
        <div className="container mx-auto flex h-16 items-center justify-between px-6">
          <div className="flex items-center gap-2">
            <Shield className="h-7 w-7 text-primary" />
            <span className="text-xl font-semibold text-foreground">
              ComplianceAI
            </span>
          </div>
          <nav className="hidden md:flex items-center gap-8">
            <a
              href="#features"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Features
            </a>
            <a
              href="#stats"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Results
            </a>
            <a
              href="#how-it-works"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              How it Works
            </a>
            <a
              href="#testimonials"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Testimonials
            </a>
          </nav>
          <header>
            <SignedOut>
              <SignInButton mode="modal" forceRedirectUrl="/dashboard">
                <Button variant="outline" size="sm">
                  Sign In
                </Button>
              </SignInButton>
            </SignedOut>

            <SignedIn>
              <UserButton afterSignOutUrl="/" />
            </SignedIn>
          </header>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-16">
        <div className="absolute inset-0 bg-linear-to-b from-primary/5 via-transparent to-transparent pointer-events-none" />
        <div className="container mx-auto px-6">
          <div className="flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center text-center">
            <div className="animate-fade-in inline-flex items-center gap-2 rounded-full border border-border bg-muted/50 px-4 py-1.5 text-sm text-muted-foreground mb-8">
              <Lock className="h-3.5 w-3.5" />
              Enterprise-grade security Compliance
            </div>

            <h1
              className="animate-fade-in max-w-4xl text-4xl font-semibold tracking-tight text-foreground sm:text-5xl lg:text-6xl"
              style={{ animationDelay: "0.1s" }}
            >
              AI-Powered Compliance
              <span className="block text-primary">Audit Agent</span>
            </h1>

            <p
              className="animate-fade-in mt-6 max-w-2xl text-lg text-muted-foreground leading-relaxed"
              style={{ animationDelay: "0.2s" }}
            >
              Analyze software documentation and repository artifacts against
              security and compliance rules. Trusted by V&V engineers and
              compliance teams worldwide.
            </p>

            <div
              className="animate-fade-in mt-10 flex items-center gap-4"
              style={{ animationDelay: "0.3s" }}
            >
              <Link to="/dashboard">
                <Button
                  size="lg"
                  className="h-12 px-8 text-base font-medium group"
                >
                  Dashboard
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Button>
              </Link>
              <a href="#how-it-works">
                <Button
                  variant="outline"
                  size="lg"
                  className="h-12 px-8 text-base font-medium"
                >
                  Learn More
                </Button>
              </a>
            </div>

            {/* Trusted By */}
            <div
              className="animate-fade-in mt-20 text-center"
              style={{ animationDelay: "0.4s" }}
            >
              <p className="text-sm text-muted-foreground mb-6">
                Trusted by leading enterprises
              </p>
              <div className="flex items-center justify-center gap-12 opacity-50">
                <Building2 className="h-8 w-8" />
                <Globe className="h-8 w-8" />
                <Award className="h-8 w-8" />
                <Building2 className="h-8 w-8" />
                <Globe className="h-8 w-8" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section id="stats" className="py-24 bg-muted/30">
        <div className="container mx-auto px-6">
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { value: "99.2%", label: "Accuracy Rate", icon: TrendingUp },
              { value: "10M+", label: "Artifacts Analyzed", icon: FileText },
              { value: "500+", label: "Enterprise Clients", icon: Users },
              { value: "<2min", label: "Average Audit Time", icon: Clock },
            ].map((stat, index) => (
              <div
                key={stat.label}
                className="animate-fade-in rounded-2xl border border-border bg-card p-8 text-center"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <stat.icon className="h-8 w-8 text-primary mx-auto mb-4" />
                <div className="text-4xl font-semibold text-foreground">
                  {stat.value}
                </div>
                <p className="mt-2 text-muted-foreground">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-semibold text-foreground sm:text-4xl">
              Everything you need for compliance
            </h2>
            <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
              Our AI-powered platform provides comprehensive audit capabilities
              with full traceability and explainability.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {[
              {
                icon: CheckCircle,
                title: "Automated Audits",
                description:
                  "Continuous compliance monitoring with intelligent rule matching against industry standards.",
              },
              {
                icon: FileText,
                title: "Complete Audit Trails",
                description:
                  "Full traceability with evidence, reasoning documentation, and decision history.",
              },
              {
                icon: Shield,
                title: "Enterprise Security",
                description:
                  "Built for security teams with SOC 2 Type II certified infrastructure.",
              },
              {
                icon: Zap,
                title: "Real-time Analysis",
                description:
                  "Instant feedback on compliance status as changes are made to your codebase.",
              },
              {
                icon: BarChart3,
                title: "Risk Scoring",
                description:
                  "Intelligent risk assessment with severity levels and prioritized remediation.",
              },
              {
                icon: Globe,
                title: "Multi-Framework Support",
                description:
                  "Support for SOC 2, ISO 27001, HIPAA, GDPR, and custom compliance frameworks.",
              },
            ].map((feature, index) => (
              <div
                key={feature.title}
                className="animate-fade-in rounded-xl border border-border bg-card p-8 hover:border-primary/50 transition-colors"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <feature.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="mt-6 text-lg font-medium text-foreground">
                  {feature.title}
                </h3>
                <p className="mt-3 text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section id="how-it-works" className="py-24 bg-muted/30">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-semibold text-foreground sm:text-4xl">
              How it works
            </h2>
            <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
              Get from code to compliance in three simple steps
            </p>
          </div>

          <div className="grid gap-12 lg:grid-cols-3">
            {[
              {
                step: "01",
                title: "Connect Your Repository",
                description:
                  "Link your code repository and documentation sources. We support GitHub, GitLab, Bitbucket, and custom integrations.",
              },
              {
                step: "02",
                title: "AI Analyzes Artifacts",
                description:
                  "Our AI agent scans your codebase, documentation, and configurations against compliance rules and security best practices.",
              },
              {
                step: "03",
                title: "Review & Remediate",
                description:
                  "Get detailed findings with evidence, reasoning, and actionable remediation steps. Export audit-ready reports.",
              },
            ].map((item, index) => (
              <div
                key={item.step}
                className="animate-fade-in relative"
                style={{ animationDelay: `${index * 0.15}s` }}
              >
                <div className="text-8xl font-bold text-primary/10 absolute -top-4 -left-2">
                  {item.step}
                </div>
                <div className="relative pt-12">
                  <h3 className="text-xl font-medium text-foreground">
                    {item.title}
                  </h3>
                  <p className="mt-4 text-muted-foreground leading-relaxed">
                    {item.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-24">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-semibold text-foreground sm:text-4xl">
              Trusted by compliance teams
            </h2>
            <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
              See what security and compliance professionals are saying
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {[
              {
                quote:
                  "ComplianceAI reduced our audit preparation time by 80%. The AI reasoning is transparent and auditor-approved.",
                author: "Sarah Chen",
                role: "VP of Security",
                company: "TechCorp Inc.",
              },
              {
                quote:
                  "Finally, a compliance tool that explains its findings. Our auditors love the detailed evidence trails.",
                author: "Michael Torres",
                role: "Compliance Director",
                company: "FinanceHub",
              },
              {
                quote:
                  "The automated continuous monitoring means we catch issues before they become violations. Game changer.",
                author: "Emily Watson",
                role: "CISO",
                company: "HealthData Systems",
              },
            ].map((testimonial, index) => (
              <div
                key={testimonial.author}
                className="animate-fade-in rounded-xl border border-border bg-card p-8"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <p className="text-foreground leading-relaxed italic">
                  "{testimonial.quote}"
                </p>
                <div className="mt-6 flex items-center gap-4">
                  <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
                    <span className="text-primary font-medium">
                      {testimonial.author
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-foreground">
                      {testimonial.author}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {testimonial.role}, {testimonial.company}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-primary/5">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-semibold text-foreground sm:text-4xl">
            Ready to automate your compliance?
          </h2>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Join 500+ enterprises who trust ComplianceAI for their security
            audits.
          </p>
          <div className="mt-10 flex items-center justify-center gap-4">
            <Link to="/dashboard">
              <Button
                size="lg"
                className="h-12 px-8 text-base font-medium group"
              >
                Get Started
                <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Button
              variant="outline"
              size="lg"
              className="h-12 px-8 text-base font-medium"
            >
              Schedule Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-12 bg-muted/30">
        <div className="container mx-auto px-6">
          <div className="grid gap-8 md:grid-cols-4">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Shield className="h-6 w-6 text-primary" />
                <span className="font-semibold text-foreground">
                  ComplianceAI
                </span>
              </div>
              <p className="text-sm text-muted-foreground">
                AI-powered compliance auditing for modern enterprises.
              </p>
            </div>
            <div>
              <h4 className="font-medium text-foreground mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <a
                    href="#features"
                    className="hover:text-foreground transition-colors"
                  >
                    Features
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-foreground transition-colors"
                  >
                    Pricing
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-foreground transition-colors"
                  >
                    Integrations
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-foreground mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <a
                    href="#"
                    className="hover:text-foreground transition-colors"
                  >
                    About
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-foreground transition-colors"
                  >
                    Blog
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-foreground transition-colors"
                  >
                    Careers
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-foreground mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <a
                    href="#"
                    className="hover:text-foreground transition-colors"
                  >
                    Privacy
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-foreground transition-colors"
                  >
                    Terms
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-foreground transition-colors"
                  >
                    Security
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t border-border text-center text-sm text-muted-foreground">
            © 2024 ComplianceAI. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
