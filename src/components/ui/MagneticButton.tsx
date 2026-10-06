'use client';

import { useRef, useEffect } from 'react';
import gsap from 'gsap';

interface MagneticButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  active?: boolean;
}

export function MagneticButton({ children, active, className = '', ...props }: MagneticButtonProps) {
  const ref = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const handleMouseMove = (e: MouseEvent) => {
      const { clientX, clientY } = e;
      const { height, width, left, top } = el.getBoundingClientRect();
      const middleX = clientX - (left + width / 2);
      const middleY = clientY - (top + height / 2);
      
      gsap.to(el, {
        x: middleX * 0.2,
        y: middleY * 0.2,
        duration: 0.5,
        ease: 'power3.out'
      });
    };

    const handleMouseLeave = () => {
      gsap.to(el, {
        x: 0,
        y: 0,
        duration: 0.7,
        ease: 'elastic.out(1, 0.3)'
      });
    };

    const handleMouseDown = () => {
      gsap.to(el, { scale: 0.92, duration: 0.2, ease: 'power2.out' });
    };

    const handleMouseUp = () => {
      gsap.to(el, { scale: 1, duration: 0.4, ease: 'back.out(1.5)' });
    };

    el.addEventListener('mousemove', handleMouseMove);
    el.addEventListener('mouseleave', handleMouseLeave);
    el.addEventListener('mousedown', handleMouseDown);
    el.addEventListener('mouseup', handleMouseUp);
    el.addEventListener('mouseleave', handleMouseUp); // Ensure scale resets if left while pressing

    return () => {
      el.removeEventListener('mousemove', handleMouseMove);
      el.removeEventListener('mouseleave', handleMouseLeave);
      el.removeEventListener('mousedown', handleMouseDown);
      el.removeEventListener('mouseup', handleMouseUp);
      el.removeEventListener('mouseleave', handleMouseUp);
    };
  }, []);

  return (
    <button
      ref={ref}
      className={`relative p-2 rounded-xl transition-colors shrink-0 outline-none flex items-center justify-center border border-transparent ${
        active
          ? 'bg-[#EEF2FF] text-[#4F46E5] border-[#4F46E5]/20 shadow-sm'
          : 'hover:bg-[#F3F4F6] text-[#737373] hover:text-[#171717]'
      } ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
