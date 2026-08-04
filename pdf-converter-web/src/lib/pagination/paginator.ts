/**
 * Client-side A4 Paginator
 * Splits top-level HTML nodes into discrete A4 page cards (.preview-page)
 * based on 257mm printable height and manual page breaks (<!-- PAGEBREAK --> / .page-break).
 */
export function paginateDocument(
  container: HTMLElement,
  coverHtml: string,
  bodyHtml: string
): void {
  if (typeof window === 'undefined' || !container) return;

  // Build temporary wrapper to parse body HTML
  const temp = document.createElement('div');
  temp.innerHTML = bodyHtml;

  // Extract top-level elements
  const nodes = Array.from(temp.children);
  if (nodes.length === 0 && !coverHtml) {
    container.innerHTML = `<div class="preview-page">${bodyHtml}</div>`;
    return;
  }

  // Measure exact printable height (257mm = 297mm - 40mm padding)
  const calcEl = document.createElement('div');
  calcEl.style.cssText =
    'position:fixed;left:-9999px;top:0;height:257mm;width:210mm;padding:0 20mm;box-sizing:border-box;visibility:hidden;';
  document.body.appendChild(calcEl);
  const maxPagePx = calcEl.clientHeight || 970;
  document.body.removeChild(calcEl);

  // Hidden ruler to measure overflow
  const ruler = document.createElement('div');
  ruler.style.cssText =
    'position:fixed;left:-9999px;top:0;width:210mm;padding:0 20mm;box-sizing:border-box;overflow:hidden;font-family:var(--font-family-content);font-size:11pt;line-height:1.6;visibility:hidden;';
  document.body.appendChild(ruler);

  const pages: HTMLElement[] = [];

  // If cover page is enabled, prepend cover as Page 1
  if (coverHtml) {
    const coverWrapper = document.createElement('div');
    coverWrapper.innerHTML = coverHtml;
    const coverPage = coverWrapper.firstElementChild as HTMLElement;
    if (coverPage) {
      coverPage.setAttribute('data-page-number', '1');
      pages.push(coverPage);
    }
  }

  // Create first content page
  let currentPage = document.createElement('div');
  currentPage.className = 'preview-page';
  ruler.innerHTML = '';

  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i] as HTMLElement;

    // Check for manual page break
    const isManualBreak =
      node.classList.contains('page-break') ||
      node.classList.contains('pagebreak') ||
      (node.getAttribute('style') && node.getAttribute('style')!.includes('break'));

    if (isManualBreak) {
      if (currentPage.children.length > 0) {
        pages.push(currentPage);
        currentPage = document.createElement('div');
        currentPage.className = 'preview-page';
        ruler.innerHTML = '';
      }
      continue;
    }

    const clone = node.cloneNode(true) as HTMLElement;
    ruler.appendChild(clone);

    // If adding node overflows printable height limit
    if (ruler.scrollHeight > maxPagePx && currentPage.children.length > 0) {
      pages.push(currentPage);
      currentPage = document.createElement('div');
      currentPage.className = 'preview-page';
      ruler.innerHTML = '';
      ruler.appendChild(clone);
    }

    currentPage.appendChild(node.cloneNode(true));
  }

  if (currentPage.children.length > 0 || pages.length === 0) {
    pages.push(currentPage);
  }

  document.body.removeChild(ruler);

  // Assign page numbers for visual indicators
  pages.forEach((page, idx) => {
    page.setAttribute('data-page-number', String(idx + 1));
  });

  // Render all pages in container
  container.innerHTML = '';
  pages.forEach((p) => container.appendChild(p));
}
