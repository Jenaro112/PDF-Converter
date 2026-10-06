'use client';

import { Panel, Group, Separator } from 'react-resizable-panels';
import { useRef, useEffect } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { StatusBar } from './StatusBar';
import { GlobalHeader } from './GlobalHeader';
import { Toolbar } from '../editor/Toolbar';
import { Editor } from '../editor/Editor';
import { Preview } from '../preview/Preview';
import { CoverSettingsDrawer } from '../settings/CoverSettingsDrawer';
import { AutosaveManager } from './AutosaveManager';
import { FileSidebar } from './FileSidebar';
import { Dashboard } from './Dashboard';
import { useEditorStore } from '@/store/editor-store';

gsap.registerPlugin(useGSAP);

export function MainLayout() {
  const { isSidebarOpen, viewMode } = useEditorStore();
  const sidebarRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Animate viewMode transition
  useGSAP(() => {
    gsap.fromTo(containerRef.current, 
      { opacity: 0, y: 10 },
      { opacity: 1, y: 0, duration: 0.5, ease: 'power3.out' }
    );
  }, [viewMode]);

  // Animate Sidebar using GSAP
  useGSAP(() => {
    if (!sidebarRef.current) return;
    
    if (isSidebarOpen) {
      gsap.to(sidebarRef.current, {
        width: 260,
        opacity: 1,
        duration: 0.4,
        ease: 'power3.out',
      });
    } else {
      gsap.to(sidebarRef.current, {
        width: 0,
        opacity: 0,
        duration: 0.3,
        ease: 'power2.in',
      });
    }
  }, [isSidebarOpen]);

  if (viewMode === 'dashboard') {
    return (
      <div ref={containerRef} className="flex flex-col h-screen bg-[#FAFAFA] text-[#171717] font-sans overflow-hidden">
        <GlobalHeader />
        <div className="flex-1 min-h-0 relative">
          <Dashboard />
        </div>
      </div>
    );
  }

  return (
    <div ref={containerRef} className="flex flex-col h-screen bg-[#FAFAFA] text-[#171717] font-sans overflow-hidden">
      <AutosaveManager />
      <GlobalHeader />

      <div className="flex-1 min-h-0 flex relative overflow-hidden px-4 pb-4">
        
        {/* File Explorer (Left Sidebar) */}
        <div 
          ref={sidebarRef} 
          className="h-full overflow-hidden shrink-0 mr-4 rounded-xl border border-[#E5E5E5] bg-white shadow-sm"
          style={{ width: isSidebarOpen ? 260 : 0, opacity: isSidebarOpen ? 1 : 0 }}
        >
          <div className="w-[260px] h-full">
            <FileSidebar />
          </div>
        </div>

        {/* Resizable Editor and Preview (Right Area) */}
        <div className="flex-1 h-full min-w-0 bg-white rounded-xl border border-[#E5E5E5] shadow-sm overflow-hidden">
          <Group orientation="horizontal">
            {/* Editor (Center Panel) */}
            <Panel minSize={30}>
              <div className="h-full flex flex-col overflow-hidden bg-white relative">
                <Toolbar />
                <div className="flex-1 overflow-hidden">
                  <Editor />
                </div>
              </div>
            </Panel>

            <Separator className="w-[8px] bg-transparent group flex items-center justify-center relative z-10 transition-colors cursor-col-resize hover:bg-[#4F46E5]/10">
              <div className="w-[1px] h-full transition-colors duration-300 relative bg-[#E5E5E5] group-hover:bg-[#4F46E5]" />
              <div className="absolute h-10 w-[4px] rounded-full scale-y-50 group-hover:scale-y-100 transition-all duration-300 opacity-0 group-hover:opacity-100 bg-[#4F46E5]" />
            </Separator>

            {/* Preview (Right Panel) */}
            <Panel minSize={30}>
              <div className="h-full overflow-auto bg-white flex justify-center">
                <Preview />
              </div>
            </Panel>
            
          </Group>
        </div>
      </div>

      <StatusBar />
      <CoverSettingsDrawer />
    </div>
  );
}
