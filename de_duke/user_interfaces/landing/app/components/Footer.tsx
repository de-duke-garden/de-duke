import Link from "next/link";

export default function Footer() {
    return (
        <footer className="bg-white pt-16 pb-8 border-t border-gray-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

                {/* Top Links Section */}
                <div className="text-center mb-12">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">About De-Duke's Recommendations</h3>
                    <p className="text-gray-500 max-w-2xl mx-auto text-sm leading-relaxed mb-8">
                        We simplify your search with smart suggestions tailored to your needs. Based on your preferences and browsing behavior, De-Duke highlights properties you're most likely to love—saving you time and helping you make confident decisions.
                    </p>

                    <div className="flex flex-wrap justify-center gap-8 md:gap-16 border-t border-b border-gray-100 py-6 text-sm text-gray-600 font-medium">
                        <div className="flex items-center cursor-pointer hover:text-primary group">
                            Real Estate
                            <svg className="w-4 h-4 ml-1 group-hover:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                        </div>
                        <div className="flex items-center cursor-pointer hover:text-primary group">
                            Rentals
                            <svg className="w-4 h-4 ml-1 group-hover:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                        </div>
                        <div className="flex items-center cursor-pointer hover:text-primary group">
                            Mortgage Rates
                            <svg className="w-4 h-4 ml-1 group-hover:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                        </div>
                        <div className="flex items-center cursor-pointer hover:text-primary group">
                            Browse Homes
                            <svg className="w-4 h-4 ml-1 group-hover:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                        </div>
                    </div>
                </div>

                {/* Bottom Navigation */}
                <div className="flex flex-wrap justify-center gap-6 mb-8 text-sm text-gray-600 font-medium">
                    <Link href="#" className="hover:text-primary">About</Link>
                    <Link href="#" className="hover:text-primary">Research</Link>
                    <Link href="#" className="hover:text-primary">Help</Link>
                    <Link href="#" className="hover:text-primary">Advertise</Link>
                    <Link href="#" className="hover:text-primary">Fair Housing Guide</Link>
                    <Link href="#" className="hover:text-primary">Advocacy</Link>
                    <Link href="#" className="hover:text-primary">Terms of use</Link>
                    <Link href="#" className="hover:text-primary">Privacy Notice</Link>
                    <Link href="#" className="hover:text-primary">Learn</Link>
                    <Link href="#" className="hover:text-primary">AI</Link>
                    <Link href="#" className="hover:text-primary">Mobile Apps</Link>
                </div>

                {/* Legal Text */}
                <div className="text-center text-[10px] text-gray-400 max-w-4xl mx-auto space-y-2 mb-8">
                    <p>At De-Duke, we're committed to digital accessibility for all.<br />
                        We're actively working to make our platform inclusive and user-friendly for individuals with disabilities. Your feedback helps us improve.<br />
                        If you encounter an accessibility issue or need specific accommodations, please don't hesitate to <a href="#" className="text-primary hover:underline">reach out</a>.</p>
                    <p>De-Duke, Inc. is a licensed real estate brokerage operating across multiple states. Standard data rates apply.</p>
                    <p className="font-semibold text-primary underline cursor-pointer">Contact De-Duke, Inc. Brokerage</p>
                </div>

                {/* App Badges Bottom */}
                <div className="flex justify-center space-x-4 mb-4 grayscale opacity-50 hover:grayscale-0 hover:opacity-100 transition-all duration-300">
                    <div className="h-8 w-24 bg-gray-200 rounded border border-gray-300 flex items-center justify-center text-[8px]">Google Play</div>
                    <div className="h-8 w-24 bg-gray-200 rounded border border-gray-300 flex items-center justify-center text-[8px]">App Store</div>
                </div>

                <div className="text-center text-[10px] text-gray-400">
                    copyright &copy; de-duke.com
                </div>
            </div>
        </footer>
    );
}
