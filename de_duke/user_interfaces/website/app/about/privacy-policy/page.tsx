import MDViewer from "@/components/about/mdviewer";


export const metadata = {
    title: "Privacy Policy - De-Duke Garden Care",
    description: "Read the privacy policy of De-Duke Garden Care to understand how we handle your data and protect your privacy.",
};


export default function PrivacyPolicy() {
    return (
        <MDViewer filePath="content/about/privacy-policy.md" />
    );
}
