"use client";

import { useEffect, useState, useRef } from "react";

const stats = [
    { id: 1, name: "Transactions Completed", value: "12K+" },
    { id: 2, name: "Trusted By Agents", value: "500+" },
    { id: 3, name: "Years of Experience", value: "15+" },
    { id: 4, name: "Cities Covered", value: "40+" },
];

export default function StatsSection() {
    const [isVisible, setIsVisible] = useState(false);
    const sectionRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                }
            },
            { threshold: 0.1 }
        );

        if (sectionRef.current) {
            observer.observe(sectionRef.current);
        }

        return () => {
            if (sectionRef.current) {
                observer.unobserve(sectionRef.current);
            }
        };
    }, []);

    return (
        <div ref={sectionRef} className="bg-primary py-12 sm:py-16">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-2xl lg:max-w-none">
                    <div className="text-center">
                        <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl mb-4">
                            Trusted by thousands of families
                        </h2>
                        <p className="text-lg leading-8 text-primary-light">
                            We deliver results with transparency and efficiency across the nation.
                        </p>
                    </div>
                    <dl className="mt-16 grid grid-cols-1 gap-0.5 overflow-hidden rounded-2xl text-center sm:grid-cols-2 lg:grid-cols-4">
                        {stats.map((stat) => (
                            <div key={stat.id} className="flex flex-col bg-white/5 p-8 hover:bg-white/10 transition-colors">
                                <dt className="text-sm font-semibold leading-6 text-gray-200">{stat.name}</dt>
                                <dd className={`order-first text-3xl font-semibold tracking-tight text-white transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
                                    {stat.value}
                                </dd>
                            </div>
                        ))}
                    </dl>
                </div>
            </div>
        </div>
    );
}
