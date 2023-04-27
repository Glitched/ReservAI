import Type from "@/components/type";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const headerMsg = "ReservAI is current in a closed beta.\n\nStay tuned.";
  return (
    <main
      className={`flex min-h-screen flex-col items-center justify-between md:p-24 sm:p-12 p-8 ${inter.className}`}
    >
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm flex">
        <div className="bottom-0 left-0 flex items-end justify-center  from-white via-white dark:from-black dark:via-black static h-auto w-auto bg-none">
          <Type msg={headerMsg} />
        </div>
      </div>
    </main>
  );
}
