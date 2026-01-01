import Image from "next/image";

export default function Hero() {
    return (
        <div className="relative bg-gray-900 overflow-hidden min-h-[600px] flex items-center justify-center">
            {/* Background Image Overlay */}
            <div className="absolute inset-0 z-0">
                <Image
                    src="https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?q=80&w=3270&auto=format&fit=crop"
                    alt="Home background"
                    fill
                    priority
                    className="object-cover opacity-60"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-gray-900/50 to-transparent" />
            </div>

            {/* Content */}
            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
                <div className="max-w-2xl">
                    <h1 className="text-4xl md:text-6xl font-extrabold text-white tracking-tight leading-tight mb-8">
                        Smart. Trust.<br />
                        Real Estate.<br />
                        Connectivity.
                    </h1>

                    {/* Search Bar */}
                    <div className="relative max-w-lg mb-12">
                        <input
                            type="text"
                            placeholder="Enter an address, neighborhood, city or..."
                            className="w-full px-6 py-4 rounded-full text-gray-900 bg-white shadow-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-lg"
                        />
                        <div className="absolute right-3 top-3">
                            <button className="bg-transparent p-2 text-gray-400 hover:text-primary transition-colors">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    className="h-6 w-6"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>

                    {/* App Store Buttons */}
                    <div className="flex space-x-4">
                        {/* Google Play Placeholder */}
                        <button className="bg-white/90 hover:bg-white text-black px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors">
                            <span className="text-xs font-bold leading-none flex flex-col items-start">
                                <span className="text-[10px] uppercase font-light">Get it on</span>
                                <span>Google Play</span>
                            </span>
                        </button>

                        {/* App Store Placeholder */}
                        <button className="bg-white/90 hover:bg-white text-black px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors">
                            <span className="text-xs font-bold leading-none flex flex-col items-start">
                                <span className="text-[10px] uppercase font-light">Download on the</span>
                                <span>App Store</span>
                            </span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
