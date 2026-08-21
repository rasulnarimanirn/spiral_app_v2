import "./globals.css";

export const metadata = {
  title: "Spiral Pipe App",
  description: "Professional spiral pipe production calculator",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="fa" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
