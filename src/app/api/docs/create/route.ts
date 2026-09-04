import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export async function POST(req: Request) {
  try {
    const { fileName, content, activeTheme, coverConfig } = await req.json();

    const sanitize = (n: string) =>
      n.replace(/[^a-zA-Z0-9._\- ]/g, '').trim();

    const rawName = sanitize(fileName ?? 'nuevo-documento');
    const safeName = rawName.endsWith('.md') ? rawName : rawName + '.md';

    if (!safeName) {
      return NextResponse.json({ error: 'Nombre invalido' }, { status: 400 });
    }

    const docsDir = path.join(process.cwd(), 'docs');
    if (!fs.existsSync(docsDir)) fs.mkdirSync(docsDir, { recursive: true });

    const filePath = path.join(docsDir, safeName);

    const fileContent = matter.stringify(content ?? '', {
      activeTheme: activeTheme ?? 'minimal',
      coverConfig: coverConfig ?? null,
    });

    fs.writeFileSync(filePath, fileContent, 'utf-8');
    return NextResponse.json({ success: true, name: safeName });
  } catch (error) {
    console.error('Create error:', error);
    return NextResponse.json({ error: 'No se pudo crear el archivo' }, { status: 500 });
  }
}
