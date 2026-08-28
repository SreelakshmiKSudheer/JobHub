import React from 'react'
import type { HeaderProps } from '../../../types/header.types'

const Header = ({ left, center, right }: HeaderProps) => {
  return (
    <header className="w-full py-2 px-10 h-15 bg-bg border border-b border-primary/50">
      {
      left && !center && !right && 
        <div className="flex items-center justify-start h-full">
          <div className="flex-shrink-0 gap-5">
            {left}
          </div>
        </div>
      }
      {
      !left && center && !right && 
        <div className="flex items-center justify-center h-full">
          <div className="flex-shrink-0">
            {center}
          </div>
        </div>
      }
      {
      !left && !center && right && 
        <div className="flex items-center justify-center h-full">
          <div className="flex-shrink-0">
            {right}
          </div>
        </div>
      }
      {left && right && 
       <div className="flex items-center justify-between h-full">
        <div className="flex-shrink-0">
          {left}
        </div>
        <div className="flex-shrink-0">
          {center}
        </div>
        <div className="flex-shrink-0">
          {right}
        </div>
      </div>}
    </header>
  )
}

export default Header
