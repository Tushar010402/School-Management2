// src/app/(dashboard)/layout.tsx
'use client'

import DashboardLayout from '@/components/layout/DashboardLayout'
import { useAuth } from '@/contexts/AuthContext';  

export default function DashboardLayoutWrapper({
  children,
}: {
  children: React.ReactNode
}) {
  return <DashboardLayout>{children}</DashboardLayout>
}