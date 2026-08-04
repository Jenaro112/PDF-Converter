'use client';

import React, { useState, useEffect, useRef, ReactNode } from 'react';
import '../../styles/splitpane.css';

interface SplitPaneProps {
  leftPanel: ReactNode;
  rightPanel: ReactNode;
}

export function SplitPane({ leftPanel, rightPanel }: SplitPaneProps) {
  const [splitRatio, setSplitRatio] = useState<number>(45);
  const [isDragging, setIsDragging] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const savedRatio = localStorage.getItem('splitRatio');
    if (savedRatio) {
      setSplitRatio(parseFloat(savedRatio));
    }
  }, []);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging || !containerRef.current) return;
      const containerRect = containerRef.current.getBoundingClientRect();
      const newRatio = ((e.clientX - containerRect.left) / containerRect.width) * 100;
      if (newRatio > 10 && newRatio < 90) {
        setSplitRatio(newRatio);
      }
    };

    const handleMouseUp = () => {
      if (isDragging) {
        setIsDragging(false);
        localStorage.setItem('splitRatio', splitRatio.toString());
      }
    };

    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, splitRatio]);

  const handleDoubleClick = () => {
    setSplitRatio(45);
    localStorage.setItem('splitRatio', '45');
  };

  return (
    <div className="split-pane-container" ref={containerRef}>
      <div className="split-pane-left" style={{ width: `${splitRatio}%` }}>
        {leftPanel}
      </div>
      <div
        className="split-pane-divider"
        onMouseDown={() => setIsDragging(true)}
        onDoubleClick={handleDoubleClick}
      >
        <div className="divider-handle"></div>
      </div>
      <div className="split-pane-right" style={{ width: `${100 - splitRatio}%` }}>
        {rightPanel}
      </div>
      {isDragging && <div className="split-pane-overlay" />}
    </div>
  );
}
