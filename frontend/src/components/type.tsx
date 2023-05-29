import { Inter } from "next/font/google";
import { useEffect, useState } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Type({
  msg,
  speed,
  callback,
}: {
  msg: string;
  speed?: number;
  callback?: () => void;
}) {
  const [showBlock, setShowBlock] = useState(false);
  const [len, setLen] = useState(0);
  const [hasCalledCallback, setHasCalledCallback] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setShowBlock((curr) => !curr);
    }, 500);
    return () => clearInterval(interval);
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setLen((len) => len + 1);
    }, speed ?? 20);
    return () => clearInterval(interval);
  });

  useEffect(() => {
    // Call callback when we're fully typed.
    if (len > msg.length && !hasCalledCallback) {
      setHasCalledCallback(true);
      if (callback) {
        callback();
      }
    }
    return () => {};
  }, [len]);

  const textToRender = msg.slice(0, len);

  return (
    <h1 className="whitespace-pre-wrap">
      {textToRender}
      {showBlock && "█"}
    </h1>
  );
}
