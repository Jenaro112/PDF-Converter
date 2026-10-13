import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const fileName = searchParams.get('file');

    if (!fileName || fileName.trim() === '' || fileName === 'null' || fileName === 'undefined' || fileName.includes('..')) {
      return NextResponse.json({ error: 'Nombre de archivo invalido' }, { status: 400 });
    }

    const cleanName = fileName.trim();
    const safeName = cleanName.endsWith('.md') ? cleanName : `${cleanName}.md`;

    const filePath = path.join(process.cwd(), 'docs', safeName);
    if (!fs.existsSync(filePath)) {
      return NextResponse.json({ error: 'Archivo no encontrado' }, { status: 404 });
    }

    const raw = fs.readFileSync(filePath, 'utf-8');
    const { content, data } = matter(raw);

    return NextResponse.json({
      content,
      frontmatter: data,
    });
  } catch (error) {
    console.error('Error loading doc:', error);
    return NextResponse.json({ error: 'No se pudo cargar el archivo' }, { status: 500 });
  }
}
