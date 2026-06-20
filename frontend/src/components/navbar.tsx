"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const navLink = (href: string) =>
    `text-sm transition-colors ${
      pathname === href
        ? "text-white"
        : "text-zinc-500 hover:text-white"
    }`;

  return (
    <header className="sticky top-0 z-50 border-b border-zinc-900 bg-[#080808]/80 backdrop-blur-xl">
      <nav className="max-w-6xl mx-auto px-8 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link
          href="/"
          className="flex items-center gap-3"
        >
          <img
            src="/favicon.png"
            alt="TavDev"
            className="w-10 h-10 object-contain"
          />

          <span className="font-bold tracking-tight text-white">
            TavDev Monitor
          </span>
        </Link>

        {/* Center Navigation */}
        <div className="flex items-center gap-8">
          <Link
            href="/test"
            className={navLink("/test")}
          >
            Test API
          </Link>

          <Link
            href="/leaderboard"
            className={navLink("/leaderboard")}
          >
            Leaderboard
          </Link>
        </div>

        {/* CTA */}
        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="text-sm text-zinc-500 hover:text-white transition-colors"
          >
            Login
          </Link>

          <Link
            href="/register"
            className="px-4 py-2 rounded-lg bg-white text-black text-sm font-semibold hover:bg-zinc-200 transition-colors"
          >
            Get Started
          </Link>
        </div>
      </nav>
    </header>
  );
}