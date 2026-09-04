import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    const docsDir = path.join(process.cwd(), 'docs');
    if (!fs.existsSync(docsDir)) {
      return NextResponse.json({ files: [] });
    }

    const files = fs.readdirSync(docsDir)
      .filter((f) => f.endsWith('.md'))
      .map((name) => {
        const filePath = path.join(docsDir, name);
        const stat = fs.statSync(filePath);
        return {
          name,
          size: stat.size,
          modified: stat.mtime.toISOString(),
        };
      });

    return NextResponse.json({ files });
  } catch (error) {
    console.error('Error listing docs:', error);
    return NextResponse.json({ error: 'No se pudieron listar los archivos' }, { status: 500 });
  }
}
