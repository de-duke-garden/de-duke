import Image from "next/image";

export default function Hero() {
    return (
        <div className="relative bg-gray-900 overflow-hidden min-h-[85vh] flex items-center">
            {/* Background Image with Parallax-like feel */}
            <div className="absolute inset-0 z-0">
                <Image
                    src="/hero-bg.avif"
                    alt="Modern Real Estate"
                    fill
                    priority
                    className="object-cover opacity-80"
                />
                {/* Advanced Gradient Overlay for maximum text readability */}
                <div className="absolute inset-0 bg-gradient-to-r from-gray-900/95 via-gray-900/70 to-transparent" />
                <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent" />
            </div>

            {/* Content Container */}
            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full pb-28 sm:pb-20 pt-20">
                <div className="max-w-2xl animate-fade-in-up">
                    {/* Brand Kicker */}
                    <div className="inline-block px-4 py-1.5 mb-6 rounded-full bg-white/10 backdrop-blur-md border border-white/20">
                        <span className="text-primary font-bold tracking-wide uppercase text-sm">De-Duke</span>
                    </div>

                    {/* Main Headline */}
                    <h1 className="text-5xl md:text-7xl font-extrabold text-white tracking-tight leading-[1.1] mb-6 drop-shadow-sm">
                        Smart. Trust. <br className="hidden md:block" />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">
                            Real Estate.
                        </span> <br />
                        Connectivity.
                    </h1>

                    {/* Subheadline */}
                    <p className="text-lg md:text-xl text-gray-300 mb-10 leading-relaxed max-w-lg">
                        Experience the future of property management and real estate investment.
                        Seamlessly connect, invest, and grow with De-Duke.
                    </p>

                    {/* App Store Buttons */}
                    <div className="flex flex-col sm:flex-row gap-4">
                        {/* Google Play Button */}
                        <button className="group bg-black/40 hover:bg-black/60 backdrop-blur-sm border border-white/30 hover:border-white/60 text-white px-6 py-3 rounded-xl flex items-center space-x-3 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg hover:shadow-primary/20">
                            <svg className="w-8 h-8" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M3.609 1.814L13.792 12 1.5 24.19C.536 23.273 0 21.6 0 18.06V5.987C0 3.012.83 1.814 3.609 1.814z" fill="#2196F3" />
                                <path d="M13.792 12L19.49 6.302 4.673 1.57c-.99-.313-1.636.195-1.064.767l10.183 9.663z" fill="#4CAF50" />
                                <path d="M19.49 6.302l2.94 2.94c.828.828.828 2.17 0 3.003l-2.934 2.934-5.704-5.18 5.7-4.697z" fill="#FFC107" />
                                <path d="M13.792 12l-5.704 5.176 10.177 9.667c.577.545 1.155.12 1.81-.53l-6.283-14.313z" fill="#F44336" />
                            </svg>
                            <div className="flex flex-col items-start leading-none">
                                <span className="text-[10px] uppercase tracking-wide opacity-80">Get it on</span>
                                <span className="text-lg font-semibold">Google Play</span>
                            </div>
                        </button>

                        {/* App Store Button */}
                        <button className="group bg-black/40 hover:bg-black/60 backdrop-blur-sm border border-white/30 hover:border-white/60 text-white px-6 py-3 rounded-xl flex items-center space-x-3 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg hover:shadow-white/10">
                            <svg className="w-8 h-8" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.68-.83 1.14-1.99 1.01-3.15-1.07.06-2.37.72-3.13 1.61-.7.83-1.28 2.07-1.12 3.14 1.19.1 2.4-.73 3.24-1.6z" />
                            </svg>
                            <div className="flex flex-col items-start leading-none">
                                <span className="text-[10px] uppercase tracking-wide opacity-80">Download on the</span>
                                <span className="text-lg font-semibold">App Store</span>
                            </div>
                        </button>
                    </div>
                </div>
            </div>

            {/* Decorative Element mimicking a scroll indicator */}
            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center animate-bounce opacity-50">
                <span className="text-xs text-white/60 mb-2 uppercase tracking-widest">Scroll</span>
                <div className="w-[1px] h-8 bg-gradient-to-b from-white to-transparent"></div>
            </div>
        </div>
    );
}
