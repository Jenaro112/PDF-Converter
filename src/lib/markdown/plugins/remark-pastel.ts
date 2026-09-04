import { visit } from 'unist-util-visit';

export function remarkPastel() {
  return (tree: any) => {
    visit(tree, 'text', (node: any, index: number | undefined, parent: any) => {
      const text = node.value;
      
      // Busca ==texto== o ==texto==(color)
      const regex = /==((?:(?!==).)+?)==(?:\(([^)]+)\))?/g;
      
      if (!regex.test(text) || typeof index !== 'number') return;
      
      const newChildren = [];
      let lastIndex = 0;
      regex.lastIndex = 0;
      
      let match;
      while ((match = regex.exec(text)) !== null) {
        // Texto anterior al match
        if (match.index > lastIndex) {
          newChildren.push({ type: 'text', value: text.slice(lastIndex, match.index) });
        }
        
        const content = match[1];
        const color = match[2] || 'amarillo'; // Por defecto amarillo si no especifica color
        
        // Creamos un nodo 'mark' (que rehype convertirá a la etiqueta <mark>)
        newChildren.push({
          type: 'element',
          data: {
            hName: 'mark',
            hProperties: { 
              className: `pastel-highlight color-${color.toLowerCase()}`,
              // Aquí mapearemos los colores pastel directamente en CSS
            }
          },
          children: [{ type: 'text', value: content }]
        });
        
        lastIndex = regex.lastIndex;
      }
      
      // Texto restante después del último match
      if (lastIndex < text.length) {
        newChildren.push({ type: 'text', value: text.slice(lastIndex) });
      }
      
      // Reemplazamos el nodo de texto original por nuestros múltiples nodos
      parent.children.splice(index, 1, ...newChildren);
    });
  };
}
