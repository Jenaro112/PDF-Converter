'use client';

import React, { useMemo } from 'react';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkFrontmatter from 'remark-frontmatter';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import remarkRehype from 'remark-rehype';
import rehypeKatex from 'rehype-katex';
import rehypeReact from 'rehype-react';
import * as prod from 'react/jsx-runtime';
import { remarkPastel } from './plugins/remark-pastel';
import { Mermaid } from '@/components/preview/Mermaid';

const production = { Fragment: prod.Fragment, jsx: prod.jsx, jsxs: prod.jsxs };

export function useMarkdownProcessor(text: string) {
  return useMemo(() => {
    try {
      // 1. Configurar el pipeline
      const processor = unified()
        .use(remarkParse)
        .use(remarkFrontmatter, ['yaml', 'toml']) // Ignora el frontmatter para que no se imprima
        .use(remarkBreaks)
        .use(remarkGfm)
        .use(remarkMath) 
        .use(remarkPastel) 
        .use(remarkRehype, { allowDangerousHtml: true })
        .use(rehypeKatex) 
        .use(rehypeReact, { 
          ...production,
          components: {
            mark: (props: any) => {
              const { className, children } = props;
              const colorClass = className || '';
              let bgColor = '#fff3b0'; 
              if (colorClass.includes('rosa')) bgColor = '#f8c8dc';
              if (colorClass.includes('rojo')) bgColor = '#fca5a5';
              if (colorClass.includes('verde')) bgColor = '#bbf7d0';
              if (colorClass.includes('celeste')) bgColor = '#bae6fd';
              if (colorClass.includes('naranja')) bgColor = '#fed7aa';
              if (colorClass.includes('violeta')) bgColor = '#ddd6fe';
              
              return (
                <mark style={{ backgroundColor: bgColor, padding: '0 4px', borderRadius: '2px', color: 'inherit' }}>
                  {children}
                </mark>
              );
            },
            p: (props: any) => {
              const { children } = props;
              const childrenArray = React.Children.toArray(children);
              
              if (childrenArray.length === 1 && React.isValidElement(childrenArray[0])) {
                const child = childrenArray[0] as React.ReactElement<any>;
                if (child.type === 'span' && child.props.className?.includes('math-display')) {
                  return <>{children}</>;
                }
              }
              
              return <p className="mb-4">{children}</p>;
            },
            h1: (props: any) => {
              // Interceptamos el token de salto de página
              const childText = Array.isArray(props.children) ? props.children[0] : props.children;
              if (childText === 'PAGEBREAKTOKEN') {
                return <div className="page-break" />;
              }
              return <h1 {...props} />;
            },
            pre: (props: any) => {
              const childrenArray = React.Children.toArray(props.children);
              
              // Buscamos cualquier hijo que tenga la clase 'language-mermaid'
              const mermaidChild = childrenArray.find(
                (child) => React.isValidElement(child) && 
                           typeof child.props.className === 'string' && 
                           child.props.className.includes('language-mermaid')
              ) as React.ReactElement<any> | undefined;

              if (mermaidChild) {
                // Función recursiva para extraer texto de los hijos de React
                const extractText = (node: any): string => {
                  if (typeof node === 'string' || typeof node === 'number') return String(node);
                  if (Array.isArray(node)) return node.map(extractText).join('');
                  if (React.isValidElement(node)) return extractText((node.props as any).children);
                  return '';
                };
                
                const code = extractText(mermaidChild.props.children);
                return <Mermaid chart={code} />;
              }
              
              return <pre {...props} />;
            }
          }
        } as any);

      // Reemplazo previo para garantizar que \newpage sea un bloque de nivel superior
      const processedText = text.replace(/\\newpage/g, '\n\n# PAGEBREAKTOKEN\n\n');
      
      const file = processor.processSync(processedText);
      return file.result;
    } catch (err) {
      console.error("Error procesando markdown:", err);
      return <div className="text-red-500">Error al procesar el documento.</div>;
    }
  }, [text]);
}
