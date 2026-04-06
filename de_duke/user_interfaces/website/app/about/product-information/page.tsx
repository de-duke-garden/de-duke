import MDViewer from "@/components/about/mdviewer";


export const metadata = {
    title: "Product Information - De-Duke Garden Care",
    description: "Discover detailed product information about De-Duke Garden Care's services, including features, benefits, and how our solutions can help you maintain a beautiful garden.",
};


export default function ProductInformation() {
    return (
        <MDViewer filePath="content/about/product-information.md" />
    );
}