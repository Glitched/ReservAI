import { Inter } from "next/font/google";
import { useEffect, useState } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [showBlock, setShowBlock] = useState(false);
  useEffect(() => {
    const interval = setInterval(() => {
      setShowBlock((curr) => !curr);
    }, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <main
      className={`flex min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}
    >
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">
          <h1>ReservAI is current in a closed beta.{showBlock && "█"}</h1>
        </div>
      </div>
    </main>
  );
}
