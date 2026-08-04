export function processPagebreaks(text: string): string {
    const pagebreakRegex = /(?:<!--\s*PAGE-?BREAK\s*-->|---PAGEBREAK---|===PAGEBREAK===|\\newpage|\\\\newpage|\\pagebreak|\\\\pagebreak)/gi;
    return text.replace(pagebreakRegex, '<div class="page-break"></div>');
}

export function cleanRedundantPagebreaks(html: string, hasCover: boolean): string {
    const pagebreakTag = '<div class="page-break"></div>';
    
    // Collapse consecutive pagebreaks
    const consecutiveRegex = new RegExp(`(?:${pagebreakTag}\\s*){2,}`, 'g');
    let cleanedHtml = html.replace(consecutiveRegex, pagebreakTag);

    // Remove leading pagebreaks if hasCover is true
    if (hasCover) {
        const leadingRegex = new RegExp(`^\\s*(?:<p>\\s*)?${pagebreakTag}(?:\\s*<\\/p>)?\\s*`, 'i');
        cleanedHtml = cleanedHtml.replace(leadingRegex, '');
    }

    // Remove trailing pagebreaks
    const trailingRegex = new RegExp(`(?:<p>\\s*)?${pagebreakTag}(?:\\s*<\\/p>)?\\s*$`, 'i');
    cleanedHtml = cleanedHtml.replace(trailingRegex, '');

    return cleanedHtml;
}
