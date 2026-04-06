import MDViewer from "@/components/about/mdviewer";


export const metadata = {
    title: "Payment Terms - De-Duke Garden Care",
    description: "Understand the payment terms and conditions for using De-Duke Garden Care's services, including billing cycles, accepted payment methods, and refund policies.",
};


export default function PaymentTerms() {
    return (
        <MDViewer filePath="content/about/payment-terms.md" />
    );
}
