import { NextRequest, NextResponse } from 'next/server';

/**
 * POST /api/export/pdf
 *
 * Receives the fully rendered HTML document and converts it to PDF
 * using Puppeteer with exact A4 format, full-bleed backgrounds,
 * and zero margins (the .page divs provide the 20mm padding).
 *
 * Body: { html: string, filename?: string, footerText?: string }
 * Response: application/pdf binary
 */
export async function POST(request: NextRequest) {
  try {
    const { html, filename = 'document.pdf', footerText = '' } = await request.json();

    if (!html || typeof html !== 'string') {
      return NextResponse.json(
        { error: 'Missing or invalid "html" field in request body.' },
        { status: 400 }
      );
    }

    // Dynamic import of puppeteer to avoid bundling issues
    const puppeteer = await import('puppeteer');

    const browser = await puppeteer.default.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
      ],
    });

    const page = await browser.newPage();

    // Match the original Puppeteer script: Retina viewport for sharp rendering
    await page.setViewport({
      width: 800,
      height: 1200,
      deviceScaleFactor: 2,
    });

    // Force print media type for @page rules
    await page.emulateMediaType('print');

    // Load the HTML content
    await page.setContent(html, {
      waitUntil: ['domcontentloaded', 'load'],
    });

    // Wait for all fonts to load
    await page.waitForFunction(() => document.fonts?.ready);

    // Wait for all images to load completely
    await page.evaluate(async () => {
      const images = Array.from(document.querySelectorAll('img'));
      await Promise.all(
        images.map((img) => {
          if (img.complete && img.naturalWidth > 0) return Promise.resolve();
          return new Promise<void>((resolve) => {
            img.addEventListener('load', () => resolve());
            img.addEventListener('error', () => resolve());
          });
        })
      );
    });

    // Escape footer text for HTML
    const escapeHtml = (str: string) =>
      str.replace(/[&<>"']/g, (char) =>
        ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char] || char)
      );

    const escapedFooter = escapeHtml(footerText);

    // Generate PDF — exact match of the original pdf.mjs
    const pdfBuffer = await page.pdf({
      format: 'A4',
      printBackground: true,
      displayHeaderFooter: true,
      footerTemplate: `<div style="width:100%; font-size:8px; color:#555; padding:0 18mm; text-align:center; font-family:Arial,sans-serif;">${escapedFooter ? `${escapedFooter} · ` : ''}Página <span class="pageNumber"></span> de <span class="totalPages"></span></div>`,
      headerTemplate: '<span></span>',
      preferCSSPageSize: true,
      margin: {
        top: '0px',
        right: '0px',
        bottom: '0px',
        left: '0px',
      },
    });

    await browser.close();

    return new NextResponse(pdfBuffer as unknown as BodyInit, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Content-Length': pdfBuffer.length.toString(),
      },
    });
  } catch (error) {
    console.error('[PDF Export Error]', error);
    return NextResponse.json(
      {
        error: 'Failed to generate PDF.',
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 }
    );
  }
}

// Body size limit is configured in next.config.ts via experimental.serverActions.bodySizeLimit
