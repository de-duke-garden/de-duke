import Image from "next/image";

export default function FeatureSection() {
    return (
        <div className="py-20 bg-gray-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

                {/* Recommendation Layout */}
                <div className="flex flex-col md:flex-row items-center justify-between mb-24 gap-12">
                    {/* Text Content */}
                    <div className="md:w-1/2">
                        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
                            Get home recommendations
                        </h2>
                        <p className="text-gray-600 mb-6">
                            Download the app for a more personalized experience.
                        </p>
                        <button className="px-6 py-2 border border-primary text-primary font-semibold rounded-md hover:bg-primary/5 transition-colors">
                            Download App
                        </button>
                    </div>

                    {/* Float UI Illustration Placeholder */}
                    <div className="md:w-1/2 relative h-64 w-full bg-white rounded-xl shadow-xl flex items-center justify-center overflow-hidden">
                        {/* Decorative elements simulating the UI in the prompt */}
                        <div className="absolute top-4 left-4 right-4 bg-white p-3 rounded shadow-sm border border-gray-100 flex items-center space-x-3">
                            <div className="h-8 w-8 rounded-full bg-green-100 flex items-center justify-center text-primary">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
                            </div>
                            <div>
                                <div className="h-2 w-32 bg-gray-200 rounded"></div>
                                <div className="h-2 w-20 bg-gray-100 rounded mt-1"></div>
                            </div>
                        </div>

                        <div className="absolute bottom-4 left-4 right-4 bg-white p-4 rounded-lg shadow-md border border-gray-100">
                            <div className="h-32 w-full bg-gray-200 rounded-lg mb-3 relative overflow-hidden">
                                <Image src="https://images.unsplash.com/photo-1568605114967-8130f3a36994?q=80&w=1000&auto=format&fit=crop" alt="House" fill className="object-cover" />
                            </div>
                            <div className="font-bold text-lg text-gray-900">$695,000</div>
                            <div className="text-xs text-gray-500 flex space-x-2 mt-1">
                                <span>4 bd</span><span>|</span><span>3 ba</span><span>|</span><span>3,102 sqft</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Feature Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {/* Buy Card */}
                    <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center hover:shadow-md transition-shadow">
                        <div className="h-32 w-32 bg-blue-50 rounded-full mb-6 flex items-center justify-center relative overflow-hidden">
                            <Image src="https://illustrations.popsy.co/amber/home-office.svg" alt="Buy a home" width={100} height={100} />
                        </div>
                        <h3 className="text-xl font-bold text-gray-900 mb-3">Buy a home</h3>
                        <p className="text-gray-600 text-sm mb-8 leading-relaxed">
                            Find your perfect property from verified listings. Explore homes that match your style, budget, and location preferences—all in one place.
                        </p>
                        <button className="mt-auto px-6 py-2 border border-green-500 text-green-600 font-medium rounded-md hover:bg-green-50 transition-colors">
                            Find a local agent
                        </button>
                    </div>

                    {/* Sell Card */}
                    <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center hover:shadow-md transition-shadow">
                        <div className="h-32 w-32 bg-orange-50 rounded-full mb-6 flex items-center justify-center relative overflow-hidden">
                            <Image src="https://illustrations.popsy.co/amber/work-from-home.svg" alt="Sell a home" width={100} height={100} />
                        </div>
                        <h3 className="text-xl font-bold text-gray-900 mb-3">Sell a home</h3>
                        <p className="text-gray-600 text-sm mb-8 leading-relaxed">
                            List your property with confidence. Reach serious buyers faster through a trusted platform built to showcase your home’s full potential.
                        </p>
                        <button className="mt-auto px-6 py-2 border border-green-500 text-green-600 font-medium rounded-md hover:bg-green-50 transition-colors">
                            See your options
                        </button>
                    </div>

                    {/* Rent Card */}
                    <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center hover:shadow-md transition-shadow">
                        <div className="h-32 w-32 bg-teal-50 rounded-full mb-6 flex items-center justify-center relative overflow-hidden">
                            <Image src="https://illustrations.popsy.co/amber/digital-nomad.svg" alt="Rent a home" width={100} height={100} />
                        </div>
                        <h3 className="text-xl font-bold text-gray-900 mb-3">Rent a home</h3>
                        <p className="text-gray-600 text-sm mb-8 leading-relaxed">
                            Discover rental options that fit your lifestyle and budget. Browse listings, connect with landlords, and schedule viewings seamlessly.
                        </p>
                        <button className="mt-auto px-6 py-2 border border-green-500 text-green-600 font-medium rounded-md hover:bg-green-50 transition-colors">
                            Find rentals
                        </button>
                    </div>

                </div>
            </div>
        </div>
    );
}
