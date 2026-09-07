import { EditorView } from '@codemirror/view';

export const pasteImagePlugin = EditorView.domEventHandlers({
  paste(event, view) {
    const clipboardData = event.clipboardData;
    if (!clipboardData) return false;

    // Buscar si hay una imagen en el portapapeles
    const items = Array.from(clipboardData.items);
    const imageItem = items.find(item => item.type.startsWith('image/'));

    if (!imageItem) return false; // No es imagen, dejar que CodeMirror maneje el pegado normal

    const file = imageItem.getAsFile();
    if (!file) return false;

    event.preventDefault(); // Prevenir el pegado normal

    // 1. Insertar texto temporal en la posición del cursor
    const placeholder = `*(Subiendo imagen...)*`;
    const pos = view.state.selection.main.head;
    
    view.dispatch({
      changes: { from: pos, insert: placeholder },
      selection: { anchor: pos + placeholder.length }
    });

    // 2. Preparar el archivo para subir
    const formData = new FormData();
    formData.append('file', file);

    // 3. Subir vía API
    fetch('/api/upload-image', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      if (data.url) {
        // 4. Reemplazar el placeholder por la URL final
        const currentDoc = view.state.doc.toString();
        const placeholderStart = currentDoc.indexOf(placeholder);
        
        if (placeholderStart !== -1) {
          view.dispatch({
            changes: {
              from: placeholderStart,
              to: placeholderStart + placeholder.length,
              insert: `![Imagen](${data.url})`
            }
          });
        }
      }
    })
    .catch(err => {
      console.error('Error al subir imagen:', err);
      // Revertir placeholder si falla
      const currentDoc = view.state.doc.toString();
      const placeholderStart = currentDoc.indexOf(placeholder);
      if (placeholderStart !== -1) {
        view.dispatch({
          changes: {
            from: placeholderStart,
            to: placeholderStart + placeholder.length,
            insert: `*(Error al subir imagen)*`
          }
        });
      }
    });

    return true; // Evento manejado
  }
});
