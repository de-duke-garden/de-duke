"use client";

import Image from "next/image";
import Link from "next/link";
import { useRef } from "react";

export default function Navbar() {
    const navbarToggleTarget = useRef<HTMLInputElement>(null);

    const handleMobileMenu = () => {
        if (navbarToggleTarget.current) {
            navbarToggleTarget.current.checked = !navbarToggleTarget.current.checked;
        }
    };

    return (
        <nav className="bg-white border-b border-gray-100 sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    {/* Logo */}
                    <div className="shrink-0 flex items-center justify-center">
                        <Link href="/" className="flex flex-col items-center group">
                            {/* <svg
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                className="h-8 w-8 text-primary group-hover:scale-110 transition-transform"
                            >
                                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                                <polyline points="9 22 9 12 15 12 15 22" />
                            </svg>
                            <span className="text-xs font-bold text-primary tracking-wide">DE-DUKE</span> */}

                            <Image src="/de-duke.png" alt="DE-DUKE" width={48} height={48} />
                        </Link>
                    </div>

                    <input type="checkbox" id="navbar-toggle-target" className="hidden peer" ref={navbarToggleTarget} />
                    {/* Mobile menu button */}
                    <div className="flex items-center md:hidden">
                        <button
                            onClick={handleMobileMenu}
                            className="text-gray-500 hover:text-gray-700 focus:outline-none p-2"
                        >
                            <svg
                                className="h-6 w-6"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M4 6h16M4 12h16M4 18h16"
                                />
                            </svg>
                        </button>
                    </div>

                    {/* Right Navigation */}
                    <div className="hidden peer-checked:flex flex-col absolute w-full left-0 z-10 top-full p-2 md:p-0 md:w-fit md:static md:flex md:flex-row md:items-center md:space-x-8 bg-white border-b border-gray-100 md:bg-transparent md:border-b-0">
                        <Link href="#" className="block px-3 py-2 rounded-md text-base font-medium hover:bg-gray-50 md:px-2 md:py-1 md:text-gray-900 md:hover:text-primary md:text-sm">
                            Buy
                        </Link>
                        <Link href="#" className="block px-3 py-2 rounded-md text-base font-medium hover:bg-gray-50 md:px-2 md:py-1 md:text-gray-900 md:hover:text-primary md:text-sm">
                            Sell
                        </Link>
                        <Link href="#" className="block px-3 py-2 rounded-md text-base font-medium hover:bg-gray-50 md:px-2 md:py-1 md:text-gray-900 md:hover:text-primary md:text-sm">
                            Rent
                        </Link>
                        <Link href="#" className="block px-3 py-2 rounded-md text-base font-medium hover:bg-gray-50 md:px-2 md:py-1 md:text-gray-900 md:hover:text-primary md:text-sm">
                            Help
                        </Link>
                        <button className="block px-3 py-2 w-fit rounded-md text-base font-medium hover:bg-gray-50 md:px-2 md:py-1 md:text-gray-900 md:hover:text-primary md:text-sm underline underline-offset-8 decoration-primary decoration-2">
                            Download
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {/* {isOpen && (
                <div className="md:hidden bg-white border-b border-gray-100">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        <Link href="#" className="block px-3 py-2 rounded-md text-base font-medium text-gray-900 hover:bg-gray-50 hover:text-primary">Buy</Link>
                        <Link href="#" className="block px-3 py-2 rounded-md text-base font-medium text-gray-900 hover:bg-gray-50 hover:text-primary">Sell</Link>
                        <Link href="#" className="block px-3 py-2 rounded-md text-base font-medium text-gray-900 hover:bg-gray-50 hover:text-primary">Rent</Link>
                        <Link href="#" className="block px-3 py-2 rounded-md text-base font-medium text-gray-900 hover:bg-gray-50 hover:text-primary">Help</Link>
                        <Link href="#" className="block px-3 py-2 rounded-md text-base font-medium text-gray-900 hover:bg-gray-50 hover:text-primary">Download</Link>
                    </div>
                </div>
            )} */}
        </nav>
    );
}
