import { useEffect, useRef } from 'react';
import './../styles/pages/_landing-page.scss';

export default function LandingPage() {
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      contentRef.current?.classList.add('loaded');
    }, 10);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="landing-page">
      <nav></nav>
      <div ref={contentRef} className="content"></div>
    </div>
  );
}
