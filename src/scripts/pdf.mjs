import puppeteer from "puppeteer";
import { pathToFileURL } from "url";

const [htmlPath, pdfPath, footerText = ""] = process.argv.slice(2);

if (!htmlPath || !pdfPath) {
  console.error("Uso: node pdf.mjs <input.html> <output.pdf>");
  process.exit(1);
}

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();

// Viewport estándar para renderizado A4 con Retina (2x) para mantener nitidez sin comprimir en exceso
await page.setViewport({
  width: 800,
  height: 1200,
  deviceScaleFactor: 2,
});

// Forzar modo print para que se respeten @page y reglas de impresión
await page.emulateMediaType("print");

// Usar pathToFileURL para generar URIs válidas en Windows (file:///C:/...) y macOS/Linux
await page.goto(pathToFileURL(htmlPath).href, { waitUntil: ["networkidle0", "domcontentloaded"] });
await page.waitForFunction(() => document.fonts?.ready);

// Esperar a que todas las imágenes carguen completamente antes de generar el PDF
await page.evaluate(async () => {
  const images = Array.from(document.querySelectorAll('img'));
  await Promise.all(images.map(img => {
    if (img.complete && img.naturalWidth > 0) return Promise.resolve();
    return new Promise((resolve) => {
      img.addEventListener('load', resolve);
      img.addEventListener('error', resolve);
    });
  }));
});

const escapeHtml = (value) => value.replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));
const footer = escapeHtml(footerText);
await page.pdf({
  path: pdfPath,
  format: "A4",
  printBackground: true,
  displayHeaderFooter: true,
  footerTemplate: `<div style="width:100%; font-size:8px; color:#555; padding:0 18mm; text-align:center; font-family:Arial,sans-serif;">${footer ? `${footer} · ` : ""}Página <span class="pageNumber"></span> de <span class="totalPages"></span></div>`,
  headerTemplate: '<span></span>',
  preferCSSPageSize: true,
  margin: { top: "0px", right: "0px", bottom: "0px", left: "0px" },
});

await browser.close();
console.log("✓");
