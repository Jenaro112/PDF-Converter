import { NextResponse } from 'next/server';
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File | null;
    
    if (!file) {
      return NextResponse.json({ error: 'No se envió ningún archivo' }, { status: 400 });
    }

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // Guardar en la carpeta public/uploads
    const uploadDir = join(process.cwd(), 'public', 'uploads');
    
    if (!existsSync(uploadDir)) {
      await mkdir(uploadDir, { recursive: true });
    }

    // Sanitizar el nombre
    const extension = file.type.split('/')[1] || 'png';
    const filename = `img_${Date.now()}.${extension}`;
    const filepath = join(uploadDir, filename);

    await writeFile(filepath, buffer);

    // Devolver la URL pública
    return NextResponse.json({ url: `/uploads/${filename}` });
  } catch (error) {
    console.error('Error uploading file:', error);
    return NextResponse.json({ error: 'Error al subir la imagen' }, { status: 500 });
  }
}
