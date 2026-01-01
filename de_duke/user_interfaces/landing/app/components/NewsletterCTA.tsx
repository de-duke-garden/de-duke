export default function NewsletterCTA() {
    return (
        <div className="bg-white py-16 sm:py-24">
            <div className="mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div className="relative isolate overflow-hidden bg-gray-900 px-6 py-24 shadow-2xl sm:rounded-3xl sm:px-24 xl:py-32">
                    <div className="mx-auto max-w-2xl text-center">
                        <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                            Stay ahead of the market.
                        </h2>
                        <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-300">
                            Get the latest property alerts, market trends, and exclusive offers delivered straight to your inbox.
                        </p>
                        <div className="mt-10 flex max-w-md gap-x-4 mx-auto">
                            <label htmlFor="email-address" className="sr-only">
                                Email address
                            </label>
                            <input
                                id="email-address"
                                name="email"
                                type="email"
                                autoComplete="email"
                                required
                                className="min-w-0 flex-auto rounded-md border-0 bg-white/5 px-3.5 py-2 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-white sm:text-sm sm:leading-6 placeholder:text-gray-400"
                                placeholder="Enter your email"
                            />
                            <button
                                type="submit"
                                className="flex-none rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white transition-colors"
                            >
                                Subscribe
                            </button>
                        </div>
                        <p className="mt-4 text-xs leading-5 text-gray-400">
                            We care about your data. Read our <a href="#" className="font-semibold text-white hover:underline">privacy policy</a>.
                        </p>
                    </div>
                    <svg
                        viewBox="0 0 1024 1024"
                        className="absolute left-1/2 top-1/2 -z-10 h-[64rem] w-[64rem] -translate-x-1/2 [mask-image:radial-gradient(closest-side,white,transparent)]"
                        aria-hidden="true"
                    >
                        <circle cx={512} cy={512} r={512} fill="url(#gradient)" fillOpacity="0.7" />
                        <defs>
                            <radialGradient id="gradient">
                                <stop stopColor="#2e7d32" />
                                <stop offset={1} stopColor="#2e7d32" />
                            </radialGradient>
                        </defs>
                    </svg>
                </div>
            </div>
        </div>
    );
}
