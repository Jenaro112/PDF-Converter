import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function POST(req: Request) {
  try {
    const { fileName } = await req.json();

    const safeName = fileName.replace(/[^a-zA-Z0-9._\- ]/g, '').trim();
    if (!safeName) {
      return NextResponse.json({ error: 'Nombre invalido' }, { status: 400 });
    }

    const docsDir = path.join(process.cwd(), 'docs');
    const filePath = path.join(docsDir, safeName);

    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Delete error:', error);
    return NextResponse.json({ error: 'No se pudo eliminar' }, { status: 500 });
  }
}
