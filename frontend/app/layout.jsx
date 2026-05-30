import "./globals.css";

export const metadata = {
  title: "waterGPT",
  description:
    "A multi-modal, multilingual RAG chatbot for medical and scientific question answering.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}