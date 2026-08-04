'use client';

import { useEffect, useRef, useCallback } from 'react';
import { EditorState } from '@codemirror/state';
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter, drawSelection, rectangularSelection } from '@codemirror/view';
import { markdown, markdownLanguage } from '@codemirror/lang-markdown';
import { languages } from '@codemirror/language-data';
import { defaultKeymap, history, historyKeymap, indentWithTab } from '@codemirror/commands';
import { syntaxHighlighting, defaultHighlightStyle, bracketMatching, indentOnInput } from '@codemirror/language';
import { searchKeymap, highlightSelectionMatches } from '@codemirror/search';
import { useEditorStore } from '@/store/editor-store';
import '@/styles/editor.css';

/**
 * MarkdownEditor — CodeMirror 6 based Markdown editor.
 * Updates the Zustand store on every change.
 */
export function MarkdownEditor() {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewRef = useRef<EditorView | null>(null);
  const setMarkdown = useEditorStore((s) => s.setMarkdown);
  const initialMarkdown = useRef(useEditorStore.getState().markdown);

  const onUpdate = useCallback(
    (update: { state: EditorState; docChanged: boolean }) => {
      if (update.docChanged) {
        setMarkdown(update.state.doc.toString());
      }
    },
    [setMarkdown]
  );

  useEffect(() => {
    if (!containerRef.current) return;

    const state = EditorState.create({
      doc: initialMarkdown.current,
      extensions: [
        lineNumbers(),
        highlightActiveLine(),
        highlightActiveLineGutter(),
        drawSelection(),
        rectangularSelection(),
        indentOnInput(),
        bracketMatching(),
        history(),
        highlightSelectionMatches(),
        syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
        markdown({ base: markdownLanguage, codeLanguages: languages }),
        keymap.of([
          ...defaultKeymap,
          ...historyKeymap,
          ...searchKeymap,
          indentWithTab,
        ]),
        EditorView.updateListener.of(onUpdate),
        EditorView.lineWrapping,
        EditorView.theme({
          '&': {
            height: '100%',
            fontSize: '13.5px',
          },
          '.cm-scroller': {
            fontFamily: "'JetBrains Mono', Consolas, 'Courier New', monospace",
            overflow: 'auto',
          },
          '.cm-content': {
            padding: '16px 0',
            caretColor: '#6366f1',
          },
          '.cm-cursor': {
            borderLeftColor: '#6366f1',
            borderLeftWidth: '2px',
          },
          '&.cm-focused .cm-cursor': {
            borderLeftColor: '#818cf8',
          },
          '.cm-gutters': {
            backgroundColor: '#12121e',
            color: '#4a4a6a',
            border: 'none',
            paddingRight: '8px',
          },
          '.cm-activeLineGutter': {
            backgroundColor: '#1a1a30',
            color: '#8888aa',
          },
          '.cm-activeLine': {
            backgroundColor: 'rgba(99, 102, 241, 0.06)',
          },
          '.cm-selectionBackground': {
            backgroundColor: 'rgba(99, 102, 241, 0.2) !important',
          },
          '&.cm-focused .cm-selectionBackground': {
            backgroundColor: 'rgba(99, 102, 241, 0.3) !important',
          },
          '.cm-line': {
            padding: '0 16px',
          },
          '.cm-matchingBracket': {
            backgroundColor: 'rgba(99, 102, 241, 0.25)',
            outline: '1px solid rgba(99, 102, 241, 0.5)',
          },
          '.cm-searchMatch': {
            backgroundColor: 'rgba(250, 204, 21, 0.3)',
            outline: '1px solid rgba(250, 204, 21, 0.5)',
          },
          '.cm-searchMatch-selected': {
            backgroundColor: 'rgba(250, 204, 21, 0.5)',
          },
        }),
      ],
    });

    const view = new EditorView({
      state,
      parent: containerRef.current,
    });

    viewRef.current = view;

    return () => {
      view.destroy();
      viewRef.current = null;
    };
  }, [onUpdate]);

  // Sync external markdown changes (e.g. file import) into the editor
  useEffect(() => {
    const unsub = useEditorStore.subscribe((state, prevState) => {
      if (viewRef.current && state.markdown !== prevState.markdown) {
        const currentDoc = viewRef.current.state.doc.toString();
        if (state.markdown !== currentDoc) {
          viewRef.current.dispatch({
            changes: {
              from: 0,
              to: currentDoc.length,
              insert: state.markdown,
            },
          });
        }
      }
    });
    return unsub;
  }, []);

  return (
    <div className="editor-wrapper" ref={containerRef} />
  );
}
