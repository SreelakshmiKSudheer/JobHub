import React from 'react'
import type { NavbarProps } from '../../../types/navbar.types'
import NavItem from '../../atoms/NavItem/NavItem'

const Navbar = ({
  items,
  activePath = "/",
}: NavbarProps) => {
  return (
    <nav aria-label="Main navigation">
      <ul className="flex flex-col items-start gap-6 md:flex-row md:items-center md:gap-8">
        {items.map((item) => (
          <li key={item.href} className="w-full md:w-auto">
            <NavItem
              label={item.label}
              href={item.href}
              active={item.href === activePath}
              onClick={() => {}}
            />
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navbar