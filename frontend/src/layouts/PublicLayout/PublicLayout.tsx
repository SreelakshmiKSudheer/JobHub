import React from 'react'
import Header from '../../components/organisms/Header/Header'
import Footer from '../../components/organisms/Footer/Footer'
import { Outlet } from 'react-router'

const PublicLayout = () => {
  return (
    <div className="flex min-h-screen w-full flex-col bg-bg">
      <Header />
      <main className="flex flex-1 w-full flex-col">
        <Outlet />
      </main>
      <Footer />      
    </div>
  )
}

export default PublicLayout
