import type { navItemProps } from './navitem.types'

export type NavbarProps = {
  items: navItemProps[];
  activePath?: string;
}