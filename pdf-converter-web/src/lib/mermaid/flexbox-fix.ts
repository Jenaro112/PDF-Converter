export function applyMermaidFlexboxFix(svgString: string): string {
    let result = svgString;

    // 1. Replace display: table-cell;
    result = result.replace(/display:\s*table-cell\s*;/g, 'display: flex !important; align-items: center !important; justify-content: center !important; width: 100% !important; text-align: center !important;');

    // 2. Replace max-width: 200px
    result = result.replace(/max-width:\s*200px/g, 'max-width:none');

    // 3. Find and adjust <foreignObject> width and translate
    const regex = /transform="translate\(-[\d\.]+\s*,\s*(-?[\d\.]+)\)"\s*><rect\/><foreignObject\s+width="([\d\.]+)"/g;
    result = result.replace(regex, (match, y, widthStr) => {
        const width = parseFloat(widthStr);
        const newWidth = width * 1.6;
        const newX = -(newWidth / 2);
        return `transform="translate(${newX}, ${y})"><rect/><foreignObject width="${newWidth}"`;
    });

    return result;
}
