import MDViewer from "@/components/about/mdviewer";


export const metadata = {
    title: "Digital Lease Agreement - De-Duke Garden Care",
    description: "Learn about the digital lease agreement offered by De-Duke Garden Care, designed to simplify the rental process for both landlords and tenants.",
};


export default function DigitalLeaseAgreement() {
    return (
        <MDViewer filePath="content/about/digital-lease-agreement.md" />
    );
}
