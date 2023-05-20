import { Inter } from "next/font/google";
import { useEffect, useState } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Type({ msg, speed }: { msg: string; speed?: number }) {
  const [showBlock, setShowBlock] = useState(false);
  const [len, setLen] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setShowBlock((curr) => !curr);
    }, 500);
    return () => clearInterval(interval);
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setLen((len) => len + 1);
    }, speed ?? 50);
    return () => clearInterval(interval);
  });

  const textToRender = msg.slice(0, len);

  return (
    <h1 className="whitespace-pre-wrap">
      {textToRender}
      {showBlock && "█"}
    </h1>
  );
}
