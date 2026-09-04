import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const fileName = searchParams.get('file');

    if (!fileName || fileName.includes('..') || !fileName.endsWith('.md')) {
      return NextResponse.json({ error: 'Nombre de archivo invalido' }, { status: 400 });
    }

    const filePath = path.join(process.cwd(), 'docs', fileName);
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
