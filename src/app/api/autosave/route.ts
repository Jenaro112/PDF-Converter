import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export async function POST(req: Request) {
  try {
    const { documentText, coverConfig, activeTheme } = await req.json();
    
    // Carpeta docs en la raíz del proyecto
    const docsDir = path.join(process.cwd(), 'docs');
    if (!fs.existsSync(docsDir)) {
      fs.mkdirSync(docsDir, { recursive: true });
    }
    
    // Archivo de sesión actual
    const filePath = path.join(docsDir, 'session.md');
    
    // Usamos gray-matter para guardar la configuración como metadatos YAML
    const fileContent = matter.stringify(documentText, {
      coverConfig,
      activeTheme
    });
    
    fs.writeFileSync(filePath, fileContent, 'utf-8');
    
    return NextResponse.json({ success: true, path: filePath });
  } catch (error) {
    console.error('Autosave error:', error);
    return NextResponse.json({ error: 'Fallo el autoguardado' }, { status: 500 });
  }
}
