'use client';

import { MainToolbar } from '@/components/toolbar/MainToolbar';
import { SplitPane } from '@/components/layout/SplitPane';
import { MarkdownEditor } from '@/components/editor/MarkdownEditor';
import { A4Preview } from '@/components/preview/A4Preview';
import { StatusBar } from '@/components/layout/StatusBar';

export default function Home() {
  return (
    <div className="app-shell">
      <MainToolbar />
      <div className="app-content">
        <SplitPane
          leftPanel={<MarkdownEditor />}
          rightPanel={<A4Preview />}
        />
      </div>
      <StatusBar />
    </div>
  );
}
