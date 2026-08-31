import React from 'react'
import type { HeaderProps } from '../../../types/header.types'

const Header = ({ left, center, right, bottom }: HeaderProps) => {
  return (
    <header className="sticky inset-x-0 top-0 z-30 w-full bg-bg border-b border-primary/50 backdrop-blur-md">
      {/* Main Header Bar */}
      <div className="mx-auto flex h-16 w-full items-center justify-between px-4 md:px-10">
        {left && (
          <div className="flex shrink-0 items-center justify-start h-full">
            {left}
          </div>
        )}
        
        {center && (
          <div className="flex flex-1 items-center justify-center h-full">
            {center}
          </div>
        )}
        
        {right && (
          <div className="flex shrink-0 items-center justify-end h-full">
            {right}
          </div>
        )}
      </div>

      {/* Dropdown / Mobile Menu Slot */}
      {bottom && bottom}
    </header>
  )
}

export default Header