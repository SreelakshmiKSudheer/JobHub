import { useState, useRef, useEffect } from 'react';
import { useMediaQuery } from 'react-responsive';
import { Outlet, useLocation, useNavigate } from 'react-router';
import Header from '../../components/organisms/Header/Header';
import Footer from '../../components/organisms/Footer/Footer';
import Sidebar from '../../components/organisms/Sidebar/Sidebar';
import Logo from '../../components/atoms/Logo/Logo';
import Button from '../../components/atoms/Button/Button';
import { useAuth } from '../../contexts/AuthContext';
import { User, LogOut, LayoutDashboard, Briefcase, FileText, Menu } from 'lucide-react';
import type { SidebarNavItem } from '../../types/sidebar.types';

const AdminLayout = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const isMobile = useMediaQuery({ maxWidth: 767 });

  const [SidebarOpen, setSidebarOpen] = useState(!isMobile);
  const toggleSidebar = () => setSidebarOpen(!SidebarOpen);

  const [prevIsMobile, setPrevIsMobile] = useState(isMobile);
  if (prevIsMobile !== isMobile) {
    setPrevIsMobile(isMobile);
    setSidebarOpen(!isMobile);
  }

  const sidebarItems: SidebarNavItem[] = [
    { label: 'Dashboard', activeOn: '/admin', action: () => navigate('/admin'), icon: <LayoutDashboard size={18} /> },
    { label: 'Job Postings', activeOn: '/admin/job-postings', action: () => navigate('/admin/job-postings'), icon: <Briefcase size={18} /> },
    { label: 'Job Templates', activeOn: '/admin/job-roles', action: () => navigate('/admin/job-roles'), icon: <FileText size={18} /> },
  ];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsUserMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = async () => {
    setIsUserMenuOpen(false);
    await logout();
    navigate('/login', { replace: true });
  };

  return (
    <div className="min-h-screen w-full bg-bg flex flex-col">
      {/* Admin Header */}
      <Header
        left={<div className="flex shrink-0 justify-around items-center h-full">
          <Button 
          onClick={() => toggleSidebar()}
          variant="none"
          color="primary"
          size="sm"
          icon={<Menu />}
          className="md:hidden rounded-full"
          />
          <Logo /></div>}
        right={
          <div className="relative" ref={dropdownRef}>
            <Button
              type="button"
              onClick={() => setIsUserMenuOpen((prev) => !prev)}
              variant="none"
              color="primary"
              className="rounded-full p-2.5 shadow-sm hover:shadow"
              icon={<User size={20} className="text-primary" />}
              aria-label="Admin Profile Menu"
            />

            {isUserMenuOpen && (
              <div className="absolute right-0 mt-2 w-56 rounded-2xl bg-bg-alt border border-text/10 shadow-xl py-2 z-50 animate-fadeIn">

                <div className="p-1">
                  <Button 
                    text="Logout"
                    icon={<LogOut size={16} />}
                    size="sm"
                    variant="none"
                    color="danger"
                    className="w-full justify-start rounded-md"
                    onClick={handleLogout}
                  />
                </div>
              </div>
            )}
          </div>
        }
      />
      <div className="flex-1 w-full flex flex-row">
        
          <Sidebar open={SidebarOpen} items={sidebarItems} activePath={location.pathname} />

        <main className="flex-1 w-full overflow-hidden px-5 py-5 md:px-10 md:py-8">
          <Outlet />
        </main>
      </div>

      <Footer />
    </div>
  );
};

export default AdminLayout;
