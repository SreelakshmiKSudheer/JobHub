import type { navItemProps } from '../../../types/navitem.types'

const NavItem = ({ label, href, active, onClick }: navItemProps) => {
  return (
    <a
      href={href}
      onClick={onClick}
      className={`
        relative
        py-2
        text-sm
        font-bold
        uppercase
        tracking-[0.12em]
        transition-colors
        duration-300
        ${
          active
            ? "text-primary"
            : "text-text hover:text-primary"
        }
        
        after:absolute
        after:bottom-0
        after:left-0
        after:h-px
        after:bg-primary
        after:transition-all
        after:duration-300
        
        ${
          active
            ? "after:w-full"
            : "after:w-0 hover:after:w-full"
        }
      `}
    >
      {label}
    </a>
  )
}

export default NavItem
