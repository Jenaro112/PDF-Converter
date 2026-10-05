'use client';

import { Panel, Group, Separator } from 'react-resizable-panels';
import { motion, AnimatePresence } from 'framer-motion';
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

export function MainLayout() {
  const { isSidebarOpen, viewMode } = useEditorStore();

  if (viewMode === 'dashboard') {
    return (
      <div className="flex flex-col h-screen bg-[var(--bg-base)] text-[var(--text-main)] font-sans overflow-hidden">
        <GlobalHeader />
        <div className="flex-1 min-h-0 relative">
          <Dashboard />
        </div>
      </div>
    );
  }

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5, ease: [0.32, 0.72, 0, 1] }}
      className="flex flex-col h-screen bg-[var(--bg-base)] text-[var(--text-main)] font-sans overflow-hidden"
    >
      <AutosaveManager />
      <GlobalHeader />

      <div className="flex-1 min-h-0 flex relative">
        
        {/* File Explorer (Left Sidebar - Flex layout) */}
        <AnimatePresence initial={false}>
          {isSidebarOpen && (
            <motion.div 
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 260, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              transition={{ duration: 0.3, ease: 'easeInOut' }}
              className="h-full overflow-hidden shrink-0 border-r border-[var(--border)]"
            >
              <div className="w-[260px] h-full">
                <FileSidebar />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Resizable Editor and Preview (Right Area) */}
        <div className="flex-1 h-full min-w-0">
          <Group orientation="horizontal">
            {/* Editor (Center Panel) */}
            <Panel minSize={30}>
              <div className="h-full flex flex-col overflow-hidden bg-[var(--bg-surface)] relative">
                <Toolbar />
                <div className="flex-1 overflow-hidden">
                  <Editor />
                </div>
              </div>
            </Panel>

            <Separator className="w-[4px] bg-transparent group flex items-center justify-center relative z-10 transition-colors cursor-col-resize hover:bg-[var(--accent)]/10">
              <div className="w-[1px] h-full transition-colors duration-300 relative bg-[var(--border)] group-hover:bg-[var(--accent)]" />
              <div className="absolute h-8 w-[4px] bg-[var(--accent)] rounded-full scale-y-50 group-hover:scale-y-100 transition-all duration-300 opacity-0 group-hover:opacity-100" />
            </Separator>

            {/* Preview (Right Panel) */}
            <Panel minSize={30}>
              <div className="h-full overflow-auto bg-[var(--bg-preview)] flex justify-center">
                <Preview />
              </div>
            </Panel>
            
          </Group>
        </div>
      </div>

      <StatusBar />
      <CoverSettingsDrawer />
    </motion.div>
  );
}
