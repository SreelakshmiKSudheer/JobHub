import { Link } from 'react-router';
import type { SidebarProps } from '../../../types/sidebar.types';
import Button from '../../atoms/Button/Button';

const Sidebar: React.FC<SidebarProps> = ({ open, items, className = '' }) => {
  return (
    <aside
      className={`${
        open ? 'flex flex-col' : 'hidden'
      } md:flex w-70 md:w-[20%] shrink-0 sticky left-0 top-15 h-[calc(100vh-68px)] bg-bg-alt border-r border-text/10 p-2 md:px-4  md:py-4 flex-col gap-2 shadow-sm ${className}`}
    >

      <nav className="flex flex-col gap-2 p-3 md:p-2">
          {items.map((item) => {

            const isActive =
              item.activeOn && location.pathname.startsWith(item.activeOn);

            return (
              <Button
                key={item.label}
                fullWidth
                color="primary"
                icon={item.icon}
                iconPosition="left"
                text={item.label}
                variant={isActive ? "filled" : "none"}
                size="lg"
                title={item.label}
                className="justify-start rounded-xl"
                onClick={() => {
                  item.action();
                }}
              />
            );
          })}
        </nav>
    </aside>
  );
};

export default Sidebar;
