'use client';

import { useEffect, useRef } from 'react';
import { useEditorStore } from '@/store/editor-store';

export function AutosaveManager() {
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // Suscribirse a cambios en el texto, tema o portada
    const unsub = useEditorStore.subscribe((state, prevState) => {
      const textChanged = state.documentText !== prevState.documentText;
      const themeChanged = state.activeTheme !== prevState.activeTheme;
      const coverChanged = JSON.stringify(state.coverConfig) !== JSON.stringify(prevState.coverConfig);

      if (textChanged || themeChanged || coverChanged) {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        
        // Debounce de 2 segundos antes de guardar
        timeoutRef.current = setTimeout(async () => {
          try {
            await fetch('/api/autosave', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                documentText: state.documentText,
                activeTheme: state.activeTheme,
                coverConfig: state.coverConfig
              })
            });
            // Marcar como guardado
            useEditorStore.setState({ isDirty: false });
          } catch (error) {
            console.error('Error autoguardando:', error);
          }
        }, 2000);
      }
    });

    return () => {
      unsub();
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  return null;
}
