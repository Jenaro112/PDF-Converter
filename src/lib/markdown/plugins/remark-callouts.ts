import { visit } from 'unist-util-visit';

export type CalloutType = 'caution' | 'important' | 'warning' | 'note' | 'tip';

export function remarkCallouts() {
  return (tree: any) => {
    visit(tree, 'blockquote', (node: any) => {
      if (!node.children || node.children.length === 0) return;

      const firstChild = node.children[0];
      if (firstChild.type !== 'paragraph' || !firstChild.children || firstChild.children.length === 0) {
        return;
      }

      const firstInline = firstChild.children[0];
      let calloutType: CalloutType | null = null;
      let matchedTag = false;

      // 1. Detectar sintaxis estándar de Callout/Alert: [!TIPO]
      if (firstInline.type === 'text') {
        const tagMatch = firstInline.value.match(
          /^\s*\[!(CAUTION|WARNING|IMPORTANT|NOTE|TIP|DANGER|INFO|ADVERTENCIA|IMPORTANTE|NOTA|AVISO)\](?:\s*:\s*|\s*|\n|$)/i
        );

        if (tagMatch) {
          const rawType = tagMatch[1].toUpperCase();
          if (['CAUTION', 'DANGER', 'ADVERTENCIA'].includes(rawType)) {
            calloutType = 'caution';
          } else if (['IMPORTANT', 'IMPORTANTE'].includes(rawType)) {
            calloutType = 'important';
          } else if (['WARNING', 'AVISO'].includes(rawType)) {
            calloutType = 'warning';
          } else if (['TIP', 'CONSEJO'].includes(rawType)) {
            calloutType = 'tip';
          } else {
            calloutType = 'note';
          }

          matchedTag = true;
          // Eliminar la etiqueta [!TIPO] del texto para que no se muestre literalmente
          firstInline.value = firstInline.value.slice(tagMatch[0].length);
        }
      }

      // 2. Si no tenía etiqueta [!TIPO], detectar por palabras clave o emojis al inicio
      if (!calloutType) {
        const extractStartingText = (n: any): string => {
          if (!n) return '';
          if (n.type === 'text') return n.value;
          if (n.children && n.children[0]) return extractStartingText(n.children[0]);
          return '';
        };

        const startText = extractStartingText(firstChild).trim();

        if (/^(⚠️|🚨|🛑|advertencia|cuidado|peligro|alerta)/i.test(startText)) {
          calloutType = 'caution';
        } else if (/^(📌|❗|❕|importante|regla obligatoria|regla clave|atenci[oó]n)/i.test(startText)) {
          calloutType = 'important';
        } else if (/^(💡|tip|consejo|recomendaci[oó]n|sugerencia)/i.test(startText)) {
          calloutType = 'tip';
        } else if (/^(ℹ️|nota|recordatorio|informaci[oó]n)/i.test(startText)) {
          calloutType = 'note';
        }
      }

      // Si se limpió la etiqueta y el nodo de texto quedó vacío, removerlo
      if (matchedTag && firstInline.type === 'text' && firstInline.value.trim() === '') {
        firstChild.children.shift();
      }

      // Si el primer párrafo quedó completamente vacío, removerlo
      if (firstChild.children.length === 0) {
        node.children.shift();
      }

      if (calloutType) {
        node.data = node.data || {};
        node.data.hProperties = node.data.hProperties || {};
        const existingClass = node.data.hProperties.className || '';
        node.data.hProperties.className = `${existingClass} callout callout-${calloutType}`.trim();
        node.data.hProperties['data-callout'] = calloutType;
      }
    });
  };
}
