'use client';

import { Panel, Group, Separator } from 'react-resizable-panels';
import { StatusBar } from './StatusBar';
import { Toolbar } from '../editor/Toolbar';
import { Editor } from '../editor/Editor';
import { Preview } from '../preview/Preview';
import { CoverSettingsDrawer } from '../settings/CoverSettingsDrawer';
import { AutosaveManager } from './AutosaveManager';
import { FileSidebar } from './FileSidebar';

export function MainLayout() {
  return (
    <div className="flex flex-col h-screen bg-[var(--bg-base)] text-[var(--text-main)] font-sans">
      <AutosaveManager />

      {/* Glassmorphism sidebar — rendered as overlay, doesn't affect the panel layout */}
      <FileSidebar />

      <Toolbar />

      <div className="flex-1 min-h-0">
        <Group orientation="horizontal">
          {/* Editor */}
          <Panel defaultSize={50} minSize={30}>
            <div className="h-full overflow-hidden bg-[var(--bg-base)]">
              <Editor />
            </div>
          </Panel>

          <Separator className="w-[1px] bg-[var(--border)] hover:bg-[var(--accent)] hover:w-[2px] transition-all" />

          {/* Preview */}
          <Panel defaultSize={50} minSize={30}>
            <div className="h-full overflow-auto bg-[var(--bg-preview)] flex justify-center">
              <Preview />
            </div>
          </Panel>
        </Group>
      </div>

      <StatusBar />
      <CoverSettingsDrawer />
    </div>
  );
}
