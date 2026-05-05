import "./globals.css";

export const metadata = {
  title: "ClientIQ | Inbound Call Intelligence",
  description:
    "A premium AI voice experience that turns inbound business calls into structured client intelligence and dashboard-ready insight."
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
