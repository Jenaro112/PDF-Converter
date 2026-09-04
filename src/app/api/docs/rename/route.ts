import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function POST(req: Request) {
  try {
    const { oldName, newName } = await req.json();

    const sanitize = (n: string) =>
      n.replace(/[^a-zA-Z0-9._\- ]/g, '').trim();

    const safeOld = sanitize(oldName);
    const rawNew  = sanitize(newName);
    const safeNew = rawNew.endsWith('.md') ? rawNew : rawNew + '.md';

    if (!safeOld || !safeNew) {
      return NextResponse.json({ error: 'Nombre invalido' }, { status: 400 });
    }

    const docsDir = path.join(process.cwd(), 'docs');
    if (!fs.existsSync(docsDir)) fs.mkdirSync(docsDir, { recursive: true });

    const oldPath = path.join(docsDir, safeOld);
    const newPath = path.join(docsDir, safeNew);

    if (!fs.existsSync(oldPath)) {
      return NextResponse.json({ error: 'Archivo origen no encontrado' }, { status: 404 });
    }

    fs.renameSync(oldPath, newPath);
    return NextResponse.json({ success: true, name: safeNew });
  } catch (error) {
    console.error('Rename error:', error);
    return NextResponse.json({ error: 'No se pudo renombrar' }, { status: 500 });
  }
}
