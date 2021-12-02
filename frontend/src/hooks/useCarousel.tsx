import { useEffect, useRef, useState } from "react";
import item from "../interfaces/items";

interface timeoutRef {
  current?: number;
}

export function useCarousel(items: item[], interval: number) {
  const timeoutRef: timeoutRef = useRef();
  const [shouldAnimate, setShouldAnimate] = useState(true);
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const next = (current + 1) % items.length;
    if (shouldAnimate) {
      timeoutRef.current = window.setTimeout(() => setCurrent(next), interval);
    }
    return () => clearTimeout(timeoutRef.current);
  }, [current, items.length, interval, shouldAnimate]);

  return { current, setShouldAnimate, timeoutRef };
}
