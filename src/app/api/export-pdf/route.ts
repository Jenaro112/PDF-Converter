import puppeteer from 'puppeteer';
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { documentText, coverConfig, activeTheme } = body;

    // Lanzar el navegador invisible
    const browser = await puppeteer.launch({ 
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    });
    
    const page = await browser.newPage();
    
    // Configurar viewport exacto para A4 (210mm x 297mm @ 96 DPI)
    await page.setViewport({ width: 794, height: 1123, deviceScaleFactor: 2 });
    
    // Viajar a la página secreta de impresión
    // Nota: localhost:3000 asume que el servidor corre en el puerto por defecto
    const appUrl = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000';
    await page.goto(`${appUrl}/print`, { waitUntil: 'networkidle0' });
    
    // Esperar a que la página React esté montada
    await page.waitForFunction('window.isReadyToReceive === true', { timeout: 10000 });
    
    // Inyectar todo el estado del editor en el navegador de Puppeteer
    await page.evaluate(({ text, cover, theme }) => {
       (window as any).loadDataForPrint(text, cover, theme);
    }, { text: documentText, cover: coverConfig, theme: activeTheme });
    
    // Esperar a que el Paginator mida y renderice la clase `.print-ready`
    await page.waitForSelector('.print-ready', { timeout: 15000 });
    
    // Pequeño margen extra para garantizar que los gráficos Mermaid u otras cargas finalicen
    await new Promise(r => setTimeout(r, 2000));
    
    // Imprimir a PDF respetando las dimensiones exactas de @page A4
    const pdfBuffer = await page.pdf({
      format: 'A4',
      preferCSSPageSize: true,
      printBackground: true, // Fundamental para que salgan los colores y la portada azul
      margin: { top: 0, right: 0, bottom: 0, left: 0 }
    });
    
    await browser.close();
    
    // Devolver el archivo como descarga
    return new NextResponse(Buffer.from(pdfBuffer), {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename="documento-pdf-converter.pdf"'
      }
    });
  } catch (error) {
    console.error('Error generando PDF:', error);
    return NextResponse.json({ error: 'Fallo al generar el PDF en el servidor' }, { status: 500 });
  }
}
