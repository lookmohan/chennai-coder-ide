import type { ReactNode } from "react";

import { AdminLayoutShell } from "@/components/admin/admin-layout";

export default function AdminLayout({ children }: { children: ReactNode }) {
  return <AdminLayoutShell>{children}</AdminLayoutShell>;
}
