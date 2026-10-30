
import { Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/authHooks";
import { showToast } from "../utils/toast";

import {
  SidebarProvider,
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarInset,
  SidebarTrigger,
} from "@/components/ui/sidebar";

import { Separator } from "@/components/ui/separator";
import {
  LayoutDashboard,
  FileText,
  BriefcaseBusiness,
  GitCompareArrows,
  ClipboardList,
  MessageSquare,
  LogOut,
  Sparkles,
} from "lucide-react";

const navigation = [
  { title: "Dashboard", url: "/dashboard", icon: LayoutDashboard },
  { title: "My Resumes", url: "/resumes", icon: FileText },
  { title: "Jobs", url: "/jobs", icon: BriefcaseBusiness },
  { title: "Job Matching", url: "/matching", icon: GitCompareArrows },
  { title: "Applications", url: "/applications", icon: ClipboardList },
  { title: "AI Career Chat", url: "/conversations", icon: MessageSquare },
];

export default function DashboardLayout() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    showToast.success("Logged out successfully");
    navigate("/login", { replace: true });
  }

  return (
    <SidebarProvider>
      <Sidebar>
        <SidebarHeader className="border-b px-4 py-4">
          <div className="flex items-center gap-2">
            <div className="rounded-lg bg-primary p-2 text-primary-foreground">
              <Sparkles className="size-5" />
            </div>
            <div>
              <p className="font-semibold">Career Copilot</p>
              <p className="text-xs text-muted-foreground">
                Your AI career assistant
              </p>
            </div>
          </div>
        </SidebarHeader>

        <SidebarContent className="p-2">
          <SidebarMenu>
            {navigation.map((item) => (
              <SidebarMenuItem key={item.url}>
                <SidebarMenuButton
                  tooltip={item.title}
                  onClick={() => navigate(item.url)}
                >
                  <item.icon />
                  <span>{item.title}</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarContent>

        <div className="mt-auto border-t p-2">
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton onClick={handleLogout}>
                <LogOut />
                <span>Log out</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </div>
      </Sidebar>

      <SidebarInset>
        <header className="flex h-14 items-center gap-3 border-b px-4">
          <SidebarTrigger />
          <Separator orientation="vertical" className="h-5" />
          <span className="font-medium">AI Career Copilot</span>
        </header>

        <main className="flex-1 bg-muted/30 p-4 md:p-6">
          <Outlet />
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}
