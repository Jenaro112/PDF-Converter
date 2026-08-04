import { PASTEL_COLORS } from '../themes';

export function processHighlights(text: string): string {
    // Process ==text==(color)
    let processedText = text.replace(/==([^=]+)==\(([^)]+)\)/g, (_, content, colorName) => {
        const color = PASTEL_COLORS[colorName.toLowerCase()] || colorName;
        return `<mark style="background-color: ${color}; padding: 1px 5px; border-radius: 4px; color: inherit;">${content}</mark>`;
    });

    // Process ==text==
    processedText = processedText.replace(/==([^=]+)==/g, (_, content) => {
        const defaultColor = PASTEL_COLORS['amarillo'];
        return `<mark style="background-color: ${defaultColor}; padding: 1px 5px; border-radius: 4px; color: inherit;">${content}</mark>`;
    });

    return processedText;
}
