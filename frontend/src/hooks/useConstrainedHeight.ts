import { useEffect, RefObject } from 'react';

export function useConstrainedHeight(
  wrapperRef: RefObject<HTMLElement>,
  contentRef: RefObject<HTMLElement>
): void {
  useEffect(() => {
    const content = contentRef.current;
    if (!content) return;

    const updateMaxHeight = () => {
      const contentHeight = content.scrollHeight;
      if (contentHeight > 0) {
        content.style.setProperty('max-height', `${contentHeight}px`, 'important');
        content.style.removeProperty('height');
      }
    };

    const resizeObserver = new ResizeObserver(() => {
      requestAnimationFrame(updateMaxHeight);
    });
    
    resizeObserver.observe(content);
    updateMaxHeight();

    return () => {
      resizeObserver.disconnect();
    };
  }, [wrapperRef, contentRef]);
}

