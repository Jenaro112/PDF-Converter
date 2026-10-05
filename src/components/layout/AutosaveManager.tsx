'use client';

import { useEffect, useRef } from 'react';
import { useEditorStore } from '@/store/editor-store';

/**
 * Flag to suppress the autosave subscription from firing when
 * we programmatically set documentText from an external file change.
 * This prevents the infinite loop: external edit → SSE → setState → autosave → write file → SSE …
 */
let suppressNextAutosave = false;

export function AutosaveManager() {
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // ─── 1. Autosave: subscribe to store changes ──────────────────────
    const unsub = useEditorStore.subscribe((state, prevState) => {
      // Skip if this change came from an external file reload
      if (suppressNextAutosave) {
        suppressNextAutosave = false;
        return;
      }

      const textChanged = state.documentText !== prevState.documentText;
      const themeChanged = state.activeTheme !== prevState.activeTheme;
      const coverChanged = JSON.stringify(state.coverConfig) !== JSON.stringify(prevState.coverConfig);

      if (textChanged || themeChanged || coverChanged) {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);

        // Debounce 2 s
        timeoutRef.current = setTimeout(async () => {
          try {
            await fetch('/api/autosave', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                fileName: state.fileName,
                documentText: state.documentText,
                activeTheme: state.activeTheme,
                coverConfig: state.coverConfig,
              }),
            });
            useEditorStore.setState({ isDirty: false });
          } catch (error) {
            console.error('Error autoguardando:', error);
          }
        }, 2000);
      }
    });

    // ─── 2. Poll for external file changes every 2 s ──────────────────
    //   We compare the file on disk with what the editor has.
    //   This is simpler and more reliable than SSE.
    let lastKnownContent: string | null = null;

    const pollInterval = setInterval(async () => {
      const state = useEditorStore.getState();
      if (!state.fileName) return; // no file loaded, nothing to watch

      try {
        const res = await fetch(
          `/api/docs/load?file=${encodeURIComponent(state.fileName)}`,
          { cache: 'no-store' }
        );
        if (!res.ok) return;
        const data = await res.json();
        const diskContent: string = data.content;

        // On the first poll just record the baseline
        if (lastKnownContent === null) {
          lastKnownContent = diskContent;
          return;
        }

        // If disk changed AND differs from what the editor has → external edit
        if (diskContent !== lastKnownContent && diskContent !== state.documentText) {
          lastKnownContent = diskContent;
          suppressNextAutosave = true;
          useEditorStore.setState({
            documentText: diskContent,
            contentVersion: state.contentVersion + 1,
            isDirty: false,
          });
        } else {
          lastKnownContent = diskContent;
        }
      } catch {
        // network hiccup, ignore
      }
    }, 2000);

    return () => {
      unsub();
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      clearInterval(pollInterval);
    };
  }, []);

  return null;
}
