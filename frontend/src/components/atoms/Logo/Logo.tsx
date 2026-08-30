import React from 'react'
import logo from '../../../assets/logo/jobhub-logo.png'

const Logo = () => {
  return (
    <div className="flex items-center justify-between gap-1 md:gap-4">
      <img src={logo} alt="JobHub Logo" className="h-8 w-8" />
      <h1 className="text-2xl text-primary font-bold">Job<span className="text-secondary">Hub</span></h1>
    </div>
  )
}

export default Logo
