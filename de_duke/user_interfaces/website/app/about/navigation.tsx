"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const navigationLinks = [
    { name: "Product Information", href: "/about/product-information" },
    { name: "Privacy Policy", href: "/about/privacy-policy" },
    { name: "Payment Terms", href: "/about/payment-terms" },
    { name: "Digital Lease Agreement", href: "/about/digital-lease-agreement" },
    { name: "Terms of Service", href: "/about/terms-of-service" },
];

export default function AboutNavigation() {
    const [isOpen, setIsOpen] = useState(false);
    const pathname = usePathname();

    return (
        <aside className="w-full md:w-52 md:box-content shrink-0 sticky top-0 self-start px-6 py-6 md:py-12 sm:px-10 bg-white">
            {/* Mobile toggle */}
            <button
                onClick={() => setIsOpen((prev) => !prev)}
                aria-expanded={isOpen}
                className="md:hidden flex items-center gap-2 text-sm font-medium text-gray-700"
            >
                <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={1.75}
                    viewBox="0 0 24 24"
                >
                    {isOpen ? (
                        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    ) : (
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                    )}
                </svg>
                <span>{isOpen ? "Close" : "Menu"}</span>
            </button>

            {/* Nav links */}
            <nav className={`${isOpen ? "block" : "hidden"} md:block`}>
                <p className="text-xs font-semibold uppercase tracking-widest text-gray-400 mb-3 mt-4 md:mt-0 px-3">
                    About
                </p>
                {navigationLinks.map((link) => {
                    const isActive = pathname === link.href;
                    return (
                        <Link
                            key={link.name}
                            href={link.href}
                            onClick={() => setIsOpen(false)}
                            className={`block py-2 px-3 rounded-md text-sm transition-colors ${
                                isActive
                                    ? "bg-gray-100 text-gray-900 font-medium"
                                    : "text-gray-500 hover:text-gray-900 hover:bg-gray-50"
                            }`}
                        >
                            {link.name}
                        </Link>
                    );
                })}
            </nav>
        </aside>
    );
}