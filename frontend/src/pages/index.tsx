import Type from "@/components/type";
import { Button } from "@/components/ui/button";
import { Inter } from "next/font/google";

import { useEffect, useState } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [showButton, setShowButton] = useState(false);
  const [url, setUrl] = useState("#");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/auth/google/authorize");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();
        setUrl(jsonData["authorization_url"]);
      } catch (error) {
        console.error("There was an error!", error);
      }
    };
    fetchData();
  }, []);

  const headerMsg = "ReservAI is currently in a closed beta.\n\nStay tuned.";
  return (
    <main
      className={`flex min-h-screen flex-col justify-between md:p-24 sm:p-12 p-8 ${inter.className}`}
    >
      <div className="z-10 w-full max-w-5xl justify-between font-mono text-sm flex">
        <div className="bottom-0 left-0 flex flex-col justify-center  from-white via-white dark:from-black dark:via-black static h-auto w-auto bg-none">
          <Type
            speed={1}
            msg={headerMsg}
            callback={() => setShowButton(true)}
          />
          <br />
          {showButton && <Button>Sign in</Button>}
        </div>
      </div>
    </main>
  );
}
