import type { ReactNode } from 'react';

export interface SidebarNavItem {
  label: string;
  icon?: ReactNode;
  activeOn?: string;
  action: () => void;
}

export interface SidebarProps {
  open: boolean;
  items: SidebarNavItem[];
  activePath: string;
  onNavigate?: (path: string) => void;
  className?: string;
}
