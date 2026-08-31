import React, { useState } from "react";
import Header from "../../components/organisms/Header/Header";
import Footer from "../../components/organisms/Footer/Footer";
import { Outlet } from "react-router";
import Logo from "../../components/atoms/Logo/Logo";
import Button from "../../components/atoms/Button/Button";
import Navbar from "../../components/molecules/Navbar/Navbar";
import { Menu, X } from "lucide-react";

const PublicLayout = () => {
  const navItems = [
    { label: "Home", href: "#home" },
    { label: "Features", href: "#features" },
    { label: "About", href: "#about" },
  ];

  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleMenuToggle = () => setIsMenuOpen((prev) => !prev);
  const handleMenuClose = () => setIsMenuOpen(false);

  return (
    <div className="flex min-h-screen w-full flex-col bg-bg">
      <Header
        left={<Logo />}
        center={
          <div className="hidden md:block">
            <Navbar items={navItems} activePath="#home" />
          </div>
        }
        right={
          <div className="flex items-center gap-4">
            <div className="hidden md:block">
              <Button
                text="Get Started"
                variant="filled"
                className="rounded-3xl"
                textClassName="text-white"
              />
            </div>
            {/* Mobile Menu Toggle */}
            <button
              type="button"
              aria-label={isMenuOpen ? "Close navigation" : "Open navigation"}
              aria-expanded={isMenuOpen}
              onClick={handleMenuToggle}
              className="text-text transition-colors duration-300 hover:text-primary md:hidden"
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        }
        bottom={
          <div
            className={`overflow-hidden border-t border-text/10 bg-bg transition-all duration-300 md:hidden ${
              isMenuOpen ? "max-h-screen opacity-100" : "max-h-0 opacity-0"
            }`}
          >
            <div className="px-6 py-8 sm:px-8" onClick={handleMenuClose}>
              <Navbar items={navItems} activePath="/" />
              <div className="mt-8">
                <Button
                  text="Get Started"
                  variant="filled"
                  className="w-full rounded-3xl"
                  textClassName="text-white"
                />
              </div>
            </div>
          </div>
        }
      />
      <main className="flex flex-1 w-full flex-col px-5 md:px-20 py-5 md:py-10">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default PublicLayout;