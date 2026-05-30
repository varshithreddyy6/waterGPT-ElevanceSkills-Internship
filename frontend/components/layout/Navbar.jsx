import Link from "next/link";

import { NAV_LINKS } from "@/lib/constants";

export default function Navbar({ active = "home", line = false }) {
  return (
    <>
      {/* Desktop Navbar */}
      <nav className={`navbar ${line ? "line" : ""}`}>
        <Link href="/" className="logo">
          waterGPT
        </Link>

        <div className="navlinks">
          {NAV_LINKS.map(([href, label, key]) => (
            <Link
              key={key}
              href={href}
              className={active === key ? "active" : ""}
            >
              {label}
            </Link>
          ))}
        </div>
      </nav>

      {/* Mobile Navbar */}
      <nav className="mobile-nav">
        <Link href="/" className="mobile-icon" aria-label="Home">
          ⌂
        </Link>

        <Link href="/" className="mobile-logo">
          waterGPT
        </Link>

        <Link href="/chat" className="mobile-icon" aria-label="Chat">
          ⌕
        </Link>
      </nav>

      {/* Mobile Horizontal Links */}
      <div className="mobile-all-links">
        {NAV_LINKS.map(([href, label, key]) => (
          <Link
            key={key}
            href={href}
            className={active === key ? "active" : ""}
          >
            {label}
          </Link>
        ))}
      </div>
    </>
  );
}