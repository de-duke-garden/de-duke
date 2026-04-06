import MDViewer from "@/components/about/mdviewer";


export const metadata = {
    title: "Terms of Service - De-Duke Garden Care",
    description: "Read the terms of service for De-Duke Garden Care to understand the rules and guidelines for using our services.",
};


export default function TermsOfService() {
    return (
        <MDViewer filePath="content/about/terms-of-service.md" />
    );
}