import AboutNavigation from "./navigation";

export default function AboutLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <div className="min-h-screen bg-white">
            <div className="max-w-5xl mx-auto relative">
                <div className="flex flex-col md:flex-row gap-0 md:gap-12">
                    <AboutNavigation />
                    <div className="flex-1 min-w-0 border-l border-gray-100 px-6 py-6 pt-0 md:py-12 sm:px-10">
                        {children}
                    </div>
                </div>
            </div>
        </div>
    );
}
