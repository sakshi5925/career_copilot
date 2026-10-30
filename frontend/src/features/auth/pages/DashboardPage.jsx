import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import {
  FileText,
  BriefcaseBusiness,
  ClipboardList,
  Sparkles,
} from "lucide-react";

const stats = [
  {
    title: "My Resumes",
    value: "Manage",
    description: "Upload and analyze resume versions",
    icon: FileText,
  },
  {
    title: "Jobs",
    value: "Explore",
    description: "Organize your target opportunities",
    icon: BriefcaseBusiness,
  },
  {
    title: "Applications",
    value: "Track",
    description: "Keep your application progress updated",
    icon: ClipboardList,
  },
  {
    title: "AI Career Chat",
    value: "Ask AI",
    description: "Get answers grounded in your resume",
    icon: Sparkles,
  },
];

export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Welcome to Career Copilot
        </h1>
        <p className="mt-2 text-muted-foreground">
          Manage your resumes, find opportunities, and plan your next career move.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className="size-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{stat.value}</p>
              <p className="mt-1 text-xs text-muted-foreground">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
