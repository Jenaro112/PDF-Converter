export function protectLatex(text: string): { text: string; displayMaths: string[]; inlineMaths: string[] } {
    const displayMaths: string[] = [];
    const inlineMaths: string[] = [];

    // Protect display math $$...$$
    let protectedText = text.replace(/\$\$([\s\S]+?)\$\$/g, (_, match) => {
        const placeholder = `\x00DISPLAY_MATH_${displayMaths.length}\x00`;
        displayMaths.push(match);
        return placeholder;
    });

    // Protect inline math $...$ (not preceded or followed by $)
    protectedText = protectedText.replace(/(?<!\$)\$([^\$]+?)\$(?!\$)/g, (_, match) => {
        const placeholder = `\x00INLINE_MATH_${inlineMaths.length}\x00`;
        inlineMaths.push(match);
        return placeholder;
    });

    return { text: protectedText, displayMaths, inlineMaths };
}

export function restoreLatex(html: string, displayMaths: string[], inlineMaths: string[]): string {
    let restoredHtml = html;

    displayMaths.forEach((match, index) => {
        const placeholder = `\x00DISPLAY_MATH_${index}\x00`;
        const replacement = `<div class="math-display">$$${match}$$</div>`;
        
        // Remove <p> tags around display math if they exist
        const pWrappedPlaceholder = new RegExp(`<p>\\s*${placeholder}\\s*<\\/p>`, 'g');
        if (pWrappedPlaceholder.test(restoredHtml)) {
            restoredHtml = restoredHtml.replace(pWrappedPlaceholder, replacement);
        } else {
            restoredHtml = restoredHtml.replace(new RegExp(placeholder, 'g'), replacement);
        }
    });

    inlineMaths.forEach((match, index) => {
        const placeholder = `\x00INLINE_MATH_${index}\x00`;
        const replacement = `<span class="math-inline">$${match}$</span>`;
        restoredHtml = restoredHtml.replace(new RegExp(placeholder, 'g'), replacement);
    });

    return restoredHtml;
}
