export function Heading({ children }: { children: React.ReactNode }) {
    return (
        <h1 className="text-2xl font-semibold tracking-tight text-gray-900 mb-6">
            {children}
        </h1>
    );
}

export function Subheading({ children }: { children: React.ReactNode }) {
    return (
        <h2 className="text-base font-semibold text-gray-800 mt-8 mb-3">
            {children}
        </h2>
    );
}

/** Numbered top-level section title, e.g. "1. What Is Personal Information?" */
export function SectionHeading({ children }: { children: React.ReactNode }) {
    return (
        <h2 className="text-[0.9375rem] font-semibold text-gray-900 mt-8 mb-2">
            {children}
        </h2>
    );
}

/** Sub-numbered heading, e.g. "3.1 Information Needed to Use the Platform:" */
export function SubsectionHeading({ children }: { children: React.ReactNode }) {
    return (
        <h3 className="text-[0.9375rem] font-medium text-gray-800 mt-5 mb-2">
            {children}
        </h3>
    );
}

export function Paragraph({ children }: { children: React.ReactNode }) {
    return (
        <p className="text-[0.9375rem] text-gray-600 leading-relaxed mb-4">
            {children}
        </p>
    );
}

/** Small muted meta line, e.g. "Effective Date: 01/04/2026" */
export function Caption({ children }: { children: React.ReactNode }) {
    return (
        <p className="text-sm text-gray-400 mb-6">
            {children}
        </p>
    );
}

/** Wrapper for lettered sub-lists (a) b) c) …) */
export function LetterList({ children }: { children: React.ReactNode }) {
    return (
        <ol className="list-none space-y-2 mb-4 pl-1">
            {children}
        </ol>
    );
}

/** Single item inside a LetterList */
export function LetterItem({
    label,
    children,
}: {
    label: string;
    children: React.ReactNode;
}) {
    return (
        <li className="flex gap-2 text-[0.9375rem] text-gray-600 leading-relaxed">
            <span className="shrink-0 font-medium text-gray-700">{label}</span>
            <span>{children}</span>
        </li>
    );
}

/** Contact / address block at the end of a document */
export function ContactBlock({ children }: { children: React.ReactNode }) {
    return (
        <address className="not-italic mt-2 mb-4 pl-4 border-l-2 border-gray-200 text-[0.9375rem] text-gray-600 leading-relaxed space-y-1">
            {children}
        </address>
    );
}