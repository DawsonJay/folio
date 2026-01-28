import { useEffect, RefObject } from 'react';

export function useConstrainedHeight(
  wrapperRef: RefObject<HTMLElement>,
  contentRef: RefObject<HTMLElement>
): void {
  useEffect(() => {
    const content = contentRef.current;
    const wrapper = wrapperRef.current;
    if (!content || !wrapper) return;

    const updateMaxHeight = () => {
      const wrapperHeight = wrapper.clientHeight;
      const contentHeight = content.scrollHeight;
      if (contentHeight > 0 && wrapperHeight > 0) {
        const maxHeight = Math.min(contentHeight, wrapperHeight);
        content.style.setProperty('max-height', `${maxHeight}px`, 'important');
        content.style.removeProperty('height');
      }
    };

    const resizeObserver = new ResizeObserver(() => {
      requestAnimationFrame(updateMaxHeight);
    });
    
    resizeObserver.observe(content);
    resizeObserver.observe(wrapper);
    updateMaxHeight();

    return () => {
      resizeObserver.disconnect();
    };
  }, [wrapperRef, contentRef]);
}

