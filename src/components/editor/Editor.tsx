'use client';

import { useEffect, useRef } from 'react';
import { EditorView, basicSetup } from 'codemirror';
import { markdown } from '@codemirror/lang-markdown';
import { EditorState } from '@codemirror/state';
import { useEditorStore } from '@/store/editor-store';
import type { FormatType } from '@/store/editor-store';
import { pasteImagePlugin } from './extensions/paste-image';

// Maps a FormatType to [prefix, suffix] markers.
// If selection is empty the cursor is placed between them.
const FORMAT_MARKERS: Record<FormatType, [string, string]> = {
  'bold':          ['**', '**'],
  'italic':        ['*',  '*'],
  'highlight':     ['==', '=='],
  'strikethrough': ['~~', '~~'],
  'code-inline':   ['`',  '`'],
  'latex-inline':  ['$',  '$'],
};

function applyFormat(view: EditorView, type: FormatType) {
  const [pre, suf] = FORMAT_MARKERS[type];
  const { from, to } = view.state.selection.main;
  const selected = view.state.sliceDoc(from, to);

  // Toggle off if already wrapped
  if (selected.startsWith(pre) && selected.endsWith(suf)) {
    const inner = selected.slice(pre.length, selected.length - suf.length);
    view.dispatch({
      changes: { from, to, insert: inner },
      selection: { anchor: from, head: from + inner.length },
    });
    return;
  }

  const insert = pre + selected + suf;
  view.dispatch({
    changes: { from, to, insert },
    // If no selection, place cursor between markers
    selection: selected
      ? { anchor: from, head: from + insert.length }
      : { anchor: from + pre.length },
  });
  view.focus();
}

export function Editor() {
  const editorRef = useRef<HTMLDivElement>(null);
  const {
    documentText,
    contentVersion,
    setText,
    snippetToInsert,
    setSnippetToInsert,
    setEditorScrollPercent,
    formatAction,
    setFormatAction,
  } = useEditorStore();

  const viewRef        = useRef<EditorView | null>(null);
  const isInitialized  = useRef(false);
  const appliedVersion = useRef(0);

  // ── Initialize CodeMirror once ───────────────────────────────────────────
  useEffect(() => {
    if (!editorRef.current || isInitialized.current) return;

    const state = EditorState.create({
      doc: documentText,
      extensions: [
        basicSetup,
        markdown(),
        pasteImagePlugin,
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            setText(update.state.doc.toString());
          }
        }),
        EditorView.domEventHandlers({
          scroll: (e) => {
            const target = e.target as HTMLElement | null;
            if (target && target.classList.contains('cm-scroller')) {
              const { scrollTop, scrollHeight, clientHeight } = target;
              const maxScroll = scrollHeight - clientHeight;
              const percent   = maxScroll > 0 ? scrollTop / maxScroll : 0;
              setEditorScrollPercent(percent);
            }
          },
        }),
        EditorView.theme({
          '&': {
            backgroundColor: 'transparent',
            color: '#171717',
            height: '100%',
          },
          '.cm-scroller': {
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            fontSize: '14.5px',
            lineHeight: '1.7',
            padding: '24px 32px',
          },
          '.cm-gutters': {
            backgroundColor: 'transparent',
            color: '#A3A3A3',
            border: 'none',
          },
          '.cm-activeLineGutter': {
            backgroundColor: 'transparent',
            color: '#4F46E5',
            fontWeight: 'bold',
          },
          '.cm-activeLine': {
            backgroundColor: 'rgba(79, 70, 229, 0.04)',
          },
        }),
      ],
    });

    const view = new EditorView({ state, parent: editorRef.current });
    viewRef.current        = view;
    isInitialized.current  = true;
    appliedVersion.current = 0;

    return () => {
      view.destroy();
      isInitialized.current = false;
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── Replace content when a file is loaded externally ────────────────────
  useEffect(() => {
    const view = viewRef.current;
    if (!view || contentVersion === 0 || contentVersion === appliedVersion.current) return;
    appliedVersion.current = contentVersion;
    view.dispatch({
      changes: { from: 0, to: view.state.doc.length, insert: documentText },
      selection: { anchor: 0 },
    });
    view.scrollDOM.scrollTop = 0;
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [contentVersion]);

  // ── Apply inline format from Toolbar ────────────────────────────────────
  useEffect(() => {
    if (!formatAction || !viewRef.current) return;
    applyFormat(viewRef.current, formatAction);
    setFormatAction(null);
  }, [formatAction, setFormatAction]);

  // ── Inject block snippets ────────────────────────────────────────────────
  useEffect(() => {
    if (!snippetToInsert || !viewRef.current) return;
    const view = viewRef.current;
    const { from, to } = view.state.selection.main;
    view.dispatch({
      changes: { from, to, insert: snippetToInsert },
      selection: { anchor: from + snippetToInsert.length },
    });
    view.focus();
    setSnippetToInsert(null);
  }, [snippetToInsert, setSnippetToInsert]);

  return (
    <div
      ref={editorRef}
      className="h-full w-full overflow-hidden outline-none"
    />
  );
}
