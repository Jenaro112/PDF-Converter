'use client';

import React, { useMemo } from 'react';

// ==========================================
// CÁLCULOS MATEMÁTICOS Y ESTADÍSTICOS
// ==========================================

// Aproximación de Lanczos para log-Gamma ln(Γ(z))
function logGamma(z: number): number {
  if (z < 0.5) {
    return Math.log(Math.PI / Math.sin(Math.PI * z)) - logGamma(1 - z);
  }
  z -= 1;
  const p = [
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-6,
    1.5056327351493116e-7
  ];
  const g = 7;
  let x = p[0];
  for (let i = 1; i < p.length; i++) {
    x += p[i] / (z + i);
  }
  const t = z + g + 0.5;
  return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
}

// Función de error Gaussiana para calcular probabilidades de la Normal
function erf(x: number): number {
  const sign = x >= 0 ? 1 : -1;
  const absX = Math.abs(x);
  const a1 = 0.254829592;
  const a2 = -0.284496736;
  const a3 = 1.421413741;
  const a4 = -1.453152027;
  const a5 = 1.061405429;
  const p = 0.3275911;

  const t = 1.0 / (1.0 + p * absX);
  const y = 1.0 - (((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t) * Math.exp(-absX * absX);
  return sign * y;
}

// CDF de la Normal estándar N(0,1)
function normalCdf(z: number): number {
  return 0.5 * (1.0 + erf(z / Math.SQRT2));
}

// Densidad Normal f(x)
function normalPdf(x: number, mu: number, sigma: number): number {
  if (sigma <= 0) return 0;
  const z = (x - mu) / sigma;
  return (1 / (sigma * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * z * z);
}

// Densidad t de Student f(t; nu)
function studentPdf(t: number, nu: number): number {
  if (nu <= 0) return 0;
  const logNumerator = logGamma((nu + 1) / 2);
  const logDenominator = logGamma(nu / 2) + 0.5 * Math.log(Math.PI * nu);
  const term = 1 + (t * t) / nu;
  const logFactor = -((nu + 1) / 2) * Math.log(term);
  return Math.exp(logNumerator - logDenominator + logFactor);
}

// Densidad Chi-Cuadrado f(x; k)
function chi2Pdf(x: number, k: number): number {
  if (x <= 0 || k <= 0) return 0;
  const logNumerator = (k / 2 - 1) * Math.log(x) - x / 2;
  const logDenominator = (k / 2) * Math.log(2) + logGamma(k / 2);
  return Math.exp(logNumerator - logDenominator);
}

// ==========================================
// PARSER DE CONFIGURACIÓN DECLARATIVA
// ==========================================

function parseConfig(rawText: string): Record<string, any> {
  const trimmed = rawText.trim();
  if (trimmed.startsWith('{')) {
    try {
      return JSON.parse(trimmed);
    } catch {
      // Ignora y pasa al parser línea por línea
    }
  }

  const result: Record<string, any> = {};
  const lines = trimmed.split('\n');

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#') || line.startsWith('//')) continue;

    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) continue;

    const key = line.slice(0, colonIdx).trim();
    let val = line.slice(colonIdx + 1).trim();

    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
      result[key] = val;
      continue;
    }

    if (val.startsWith('[') && val.endsWith(']')) {
      const inner = val.slice(1, -1).trim();
      if (!inner) {
        result[key] = [];
      } else {
        result[key] = inner.split(',').map((s) => {
          const item = s.trim();
          const n = Number(item);
          return isNaN(n) ? item.replace(/^['"]|['"]$/g, '') : n;
        });
      }
      continue;
    }

    if (val.toLowerCase() === 'true') {
      result[key] = true;
      continue;
    }
    if (val.toLowerCase() === 'false') {
      result[key] = false;
      continue;
    }

    const num = Number(val);
    if (!isNaN(num) && val !== '') {
      result[key] = num;
      continue;
    }

    result[key] = val;
  }

  return result;
}

// ==========================================
// COMPONENTE PRINCIPAL STATS-PLOT
// ==========================================

export interface StatsPlotProps {
  configText: string;
}

export function StatsPlot({ configText }: StatsPlotProps) {
  const config = useMemo(() => parseConfig(configText), [configText]);

  const type = String(config.type || 'normal').toLowerCase();
  const title = config.title || '';
  const subtitle = config.subtitle || '';
  const xLabel = config.xLabel || 'x';
  const yLabel = config.yLabel || 'Densidad f(x)';
  const shade = Array.isArray(config.shade) && config.shade.length === 2 ? config.shade : null;
  const userShadeLabel = config.shadeLabel ? String(config.shadeLabel) : null;

  // Parámetros de renderizado SVG
  const width = 640;
  const height = 290;
  const padLeft = 60;
  const padRight = 35;
  const padTop = title ? 55 : 30;
  const padBottom = 48;
  const plotWidth = width - padLeft - padRight;
  const plotHeight = height - padTop - padBottom;

  // Paleta armónica moderna (Tailwind/Indigo/Amber/Teal)
  const colors = {
    primary: '#4F46E5',    // Indigo (Normal / Principal)
    primaryFill: 'rgba(79, 70, 229, 0.16)',
    primaryStroke: '#4338CA',
    secondary: '#EA580C',  // Naranja / Ámbar (Student t o curva 2)
    secondaryFill: 'rgba(234, 88, 12, 0.14)',
    tertiary: '#0D9488',   // Teal (Chi2 curva 3)
    quaternary: '#9333EA', // Violeta
    grid: '#F3F4F6',
    border: '#E5E7EB',
    axis: '#9CA3AF',
    textMain: '#1F2937',
    textMuted: '#6B7280'
  };

  // Cálculo según el tipo de gráfico
  const plotData = useMemo(() => {
    let xMin = -4;
    let xMax = 4;
    let yMax = 0.45;
    let curves: Array<{
      id: string;
      label: string;
      stroke: string;
      strokeWidth: number;
      strokeDasharray?: string;
      fill?: string;
      points: Array<{ x: number; y: number; px: number; py: number }>;
    }> = [];
    let shadeRegion: {
      pathD: string;
      label: string;
      x1: number;
      x2: number;
    } | null = null;
    let verticalMarkers: Array<{ x: number; label: string; px: number }> = [];

    // Mapeo coordenadas
    const toPx = (x: number, y: number, curXMin: number, curXMax: number, curYMax: number) => {
      const px = padLeft + ((x - curXMin) / (curXMax - curXMin)) * plotWidth;
      const py = padTop + plotHeight - (y / curYMax) * plotHeight;
      return { px, py };
    };

    // 1. MODELO NORMAL
    if (type === 'normal' || type === 'gauss' || type === 'gaussian') {
      const mu = Number(config.mu ?? 0);
      const sigma = Number(config.sigma ?? 1);
      const safeSigma = sigma > 0 ? sigma : 1;

      xMin = mu - 3.8 * safeSigma;
      xMax = mu + 3.8 * safeSigma;
      const peakY = normalPdf(mu, mu, safeSigma);
      yMax = peakY * 1.18;

      // Puntos de la curva
      const numSteps = 240;
      const step = (xMax - xMin) / numSteps;
      const pts: Array<{ x: number; y: number; px: number; py: number }> = [];

      for (let i = 0; i <= numSteps; i++) {
        const x = xMin + i * step;
        const y = normalPdf(x, mu, safeSigma);
        const { px, py } = toPx(x, y, xMin, xMax, yMax);
        pts.push({ x, y, px, py });
      }

      curves.push({
        id: 'normal',
        label: `N(μ = ${mu}, σ = ${safeSigma})`,
        stroke: colors.primary,
        strokeWidth: 2.5,
        points: pts
      });

      // Marcadores principales (media y puntos de inflexión)
      const showMarkers = config.showMarkers !== false;
      if (showMarkers) {
        verticalMarkers.push({
          x: mu,
          label: `μ = ${mu}`,
          px: toPx(mu, 0, xMin, xMax, yMax).px
        });
        if (config.showInflection !== false) {
          verticalMarkers.push({
            x: mu - safeSigma,
            label: `μ - σ`,
            px: toPx(mu - safeSigma, 0, xMin, xMax, yMax).px
          });
          verticalMarkers.push({
            x: mu + safeSigma,
            label: `μ + σ`,
            px: toPx(mu + safeSigma, 0, xMin, xMax, yMax).px
          });
        }
      }

      // Región sombreada
      if (shade) {
        const [a, b] = shade;
        const clampedA = Math.max(xMin, a);
        const clampedB = Math.min(xMax, b);

        const shadeSteps = 120;
        const shadeStep = (clampedB - clampedA) / shadeSteps;
        let d = `M ${toPx(clampedA, 0, xMin, xMax, yMax).px} ${padTop + plotHeight} `;

        for (let i = 0; i <= shadeSteps; i++) {
          const sx = clampedA + i * shadeStep;
          const sy = normalPdf(sx, mu, safeSigma);
          const { px, py } = toPx(sx, sy, xMin, xMax, yMax);
          d += `L ${px} ${py} `;
        }
        d += `L ${toPx(clampedB, 0, xMin, xMax, yMax).px} ${padTop + plotHeight} Z`;

        // Probabilidad calculada
        const z1 = (a - mu) / safeSigma;
        const z2 = (b - mu) / safeSigma;
        const prob = Math.max(0, normalCdf(z2) - normalCdf(z1));
        const autoLabel = `P(${a} ≤ X ≤ ${b}) ≈ ${(prob * 100).toFixed(2)}%`;

        shadeRegion = {
          pathD: d,
          label: userShadeLabel || autoLabel,
          x1: toPx(clampedA, 0, xMin, xMax, yMax).px,
          x2: toPx(clampedB, 0, xMin, xMax, yMax).px
        };
      }
    }

    // 2. COMPARATIVA NORMAL vs STUDENT t
    else if (
      type === 'compare_normal_student' ||
      type === 'student_vs_normal' ||
      type === 't_vs_z' ||
      type === 'compare'
    ) {
      xMin = -4.5;
      xMax = 4.5;
      yMax = 0.44;

      const df = Number(config.df ?? 3);
      const secondaryDf = config.df2 ? Number(config.df2) : null;

      const numSteps = 240;
      const step = (xMax - xMin) / numSteps;

      // Curva Normal Z
      const ptsZ: Array<{ x: number; y: number; px: number; py: number }> = [];
      for (let i = 0; i <= numSteps; i++) {
        const x = xMin + i * step;
        const y = normalPdf(x, 0, 1);
        const { px, py } = toPx(x, y, xMin, xMax, yMax);
        ptsZ.push({ x, y, px, py });
      }
      curves.push({
        id: 'z',
        label: 'Normal Estándar Z ~ N(0, 1)',
        stroke: colors.primary,
        strokeWidth: 2.5,
        points: ptsZ
      });

      // Curva Student t
      const ptsT: Array<{ x: number; y: number; px: number; py: number }> = [];
      for (let i = 0; i <= numSteps; i++) {
        const x = xMin + i * step;
        const y = studentPdf(x, df);
        const { px, py } = toPx(x, y, xMin, xMax, yMax);
        ptsT.push({ x, y, px, py });
      }
      curves.push({
        id: 't',
        label: `t de Student (gl = ${df})`,
        stroke: colors.secondary,
        strokeWidth: 2.5,
        strokeDasharray: '6 4',
        points: ptsT
      });

      // Segunda curva opcional de Student (ej. con más grados de libertad)
      if (secondaryDf) {
        const ptsT2: Array<{ x: number; y: number; px: number; py: number }> = [];
        for (let i = 0; i <= numSteps; i++) {
          const x = xMin + i * step;
          const y = studentPdf(x, secondaryDf);
          const { px, py } = toPx(x, y, xMin, xMax, yMax);
          ptsT2.push({ x, y, px, py });
        }
        curves.push({
          id: 't2',
          label: `t de Student (gl = ${secondaryDf})`,
          stroke: colors.tertiary,
          strokeWidth: 2,
          strokeDasharray: '2 2',
          points: ptsT2
        });
      }

      verticalMarkers.push({
        x: 0,
        label: 'Centro = 0',
        px: toPx(0, 0, xMin, xMax, yMax).px
      });
    }

    // 3. MODELO STUDENT t INDIVIDUAL
    else if (type === 'student' || type === 't') {
      const df = Number(config.df ?? 4);
      xMin = -4.5;
      xMax = 4.5;
      yMax = studentPdf(0, df) * 1.25;

      const numSteps = 240;
      const step = (xMax - xMin) / numSteps;
      const ptsT: Array<{ x: number; y: number; px: number; py: number }> = [];

      for (let i = 0; i <= numSteps; i++) {
        const x = xMin + i * step;
        const y = studentPdf(x, df);
        const { px, py } = toPx(x, y, xMin, xMax, yMax);
        ptsT.push({ x, y, px, py });
      }

      curves.push({
        id: 'student',
        label: `t de Student (gl = ${df})`,
        stroke: colors.secondary,
        strokeWidth: 2.5,
        points: ptsT
      });

      verticalMarkers.push({
        x: 0,
        label: 't = 0',
        px: toPx(0, 0, xMin, xMax, yMax).px
      });

      if (shade) {
        const [a, b] = shade;
        const clampedA = Math.max(xMin, a);
        const clampedB = Math.min(xMax, b);

        const shadeSteps = 120;
        const shadeStep = (clampedB - clampedA) / shadeSteps;
        let d = `M ${toPx(clampedA, 0, xMin, xMax, yMax).px} ${padTop + plotHeight} `;

        for (let i = 0; i <= shadeSteps; i++) {
          const sx = clampedA + i * shadeStep;
          const sy = studentPdf(sx, df);
          const { px, py } = toPx(sx, sy, xMin, xMax, yMax);
          d += `L ${px} ${py} `;
        }
        d += `L ${toPx(clampedB, 0, xMin, xMax, yMax).px} ${padTop + plotHeight} Z`;

        shadeRegion = {
          pathD: d,
          label: userShadeLabel || `Región [${a}, ${b}]`,
          x1: toPx(clampedA, 0, xMin, xMax, yMax).px,
          x2: toPx(clampedB, 0, xMin, xMax, yMax).px
        };
      }
    }

    // 4. MODELO CHI-CUADRADO
    else if (type === 'chi2' || type === 'chisquare' || type === 'chi_cuadrado') {
      const dfs = Array.isArray(config.dfs)
        ? config.dfs.map(Number)
        : [Number(config.df ?? 4)];

      xMin = 0;
      const maxDf = Math.max(...dfs);
      xMax = Math.max(16, maxDf * 2.8);
      yMax = 0.35;

      const numSteps = 260;
      const step = (xMax - xMin) / numSteps;

      const chiColors = [colors.primary, colors.secondary, colors.tertiary, colors.quaternary];

      dfs.forEach((dfVal, idx) => {
        const pts: Array<{ x: number; y: number; px: number; py: number }> = [];
        for (let i = 0; i <= numSteps; i++) {
          const x = i === 0 ? 0.001 : xMin + i * step;
          const y = chi2Pdf(x, dfVal);
          const { px, py } = toPx(x, y, xMin, xMax, yMax);
          pts.push({ x, y, px, py });
        }
        curves.push({
          id: `chi2-${dfVal}`,
          label: `χ² (gl = ${dfVal})`,
          stroke: chiColors[idx % chiColors.length],
          strokeWidth: 2.4,
          points: pts
        });
      });

      if (shade && dfs.length === 1) {
        const [a, b] = shade;
        const dfVal = dfs[0];
        const clampedA = Math.max(0.001, a);
        const clampedB = Math.min(xMax, b);

        const shadeSteps = 120;
        const shadeStep = (clampedB - clampedA) / shadeSteps;
        let d = `M ${toPx(clampedA, 0, xMin, xMax, yMax).px} ${padTop + plotHeight} `;

        for (let i = 0; i <= shadeSteps; i++) {
          const sx = clampedA + i * shadeStep;
          const sy = chi2Pdf(sx, dfVal);
          const { px, py } = toPx(sx, sy, xMin, xMax, yMax);
          d += `L ${px} ${py} `;
        }
        d += `L ${toPx(clampedB, 0, xMin, xMax, yMax).px} ${padTop + plotHeight} Z`;

        shadeRegion = {
          pathD: d,
          label: userShadeLabel || `Área crítica [${a}, ${b}]`,
          x1: toPx(clampedA, 0, xMin, xMax, yMax).px,
          x2: toPx(clampedB, 0, xMin, xMax, yMax).px
        };
      }
    }

    // Generar Ticks del Eje X
    const xTicks: Array<{ val: number; px: number; label: string }> = [];
    const tickCount = 6;
    const xSpan = xMax - xMin;
    const tickStep = xSpan / tickCount;

    for (let i = 0; i <= tickCount; i++) {
      const val = xMin + i * tickStep;
      const { px } = toPx(val, 0, xMin, xMax, yMax);
      const isInteger = Math.abs(val - Math.round(val)) < 0.05;
      xTicks.push({
        val,
        px,
        label: isInteger ? Math.round(val).toString() : val.toFixed(1)
      });
    }

    return {
      xMin,
      xMax,
      yMax,
      curves,
      shadeRegion,
      verticalMarkers,
      xTicks
    };
  }, [type, config, shade, userShadeLabel, plotWidth, plotHeight, padLeft, padTop]);

  return (
    <div
      className="stats-plot-card my-6 overflow-hidden rounded-2xl border border-gray-200/90 bg-white shadow-sm transition-all hover:shadow-md"
      style={{ breakInside: 'avoid', pageBreakInside: 'avoid' }}
    >
      {/* Encabezado del gráfico */}
      {(title || subtitle) && (
        <div className="border-b border-gray-100 bg-gray-50/70 px-5 py-3">
          {title && (
            <h4 className="m-0 text-[15px] font-semibold text-gray-800 tracking-tight">
              {title}
            </h4>
          )}
          {subtitle && (
            <p className="m-0 mt-0.5 text-xs text-gray-500 font-normal">
              {subtitle}
            </p>
          )}
        </div>
      )}

      {/* SVG Vectorial Nativo */}
      <div className="p-3">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-auto block select-none"
          style={{ maxHeight: '380px' }}
        >
          <defs>
            <linearGradient id="shadeGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#4F46E5" stopOpacity="0.32" />
              <stop offset="100%" stopColor="#4F46E5" stopOpacity="0.06" />
            </linearGradient>
            <filter id="plotShadow" x="-5%" y="-5%" width="110%" height="110%">
              <feDropShadow dx="0" dy="1" stdDeviation="1.5" floodColor="#000" floodOpacity="0.08" />
            </filter>
          </defs>

          {/* Líneas Guía de Fondo (Grid) */}
          {[0.25, 0.5, 0.75, 1].map((pct) => {
            const y = padTop + plotHeight * (1 - pct);
            return (
              <line
                key={pct}
                x1={padLeft}
                y1={y}
                x2={padLeft + plotWidth}
                y2={y}
                stroke={colors.grid}
                strokeWidth={1}
                strokeDasharray="3 3"
              />
            );
          })}

          {/* Área sombreada bajo la curva (Probabilidad) */}
          {plotData.shadeRegion && (
            <g className="shade-group">
              <path
                d={plotData.shadeRegion.pathD}
                fill="url(#shadeGradient)"
                stroke="#4F46E5"
                strokeWidth={1.2}
                strokeOpacity={0.6}
              />
              {/* Etiqueta ubicada hacia el lateral superior derecho (fuera del centro de la curva) */}
              <g
                transform={`translate(${padLeft + plotWidth - 10}, ${padTop + 18})`}
              >
                <rect
                  x="-175"
                  y="-13"
                  width="175"
                  height="26"
                  rx="6"
                  fill="white"
                  stroke="#C7D2FE"
                  strokeWidth="1.2"
                  filter="url(#plotShadow)"
                />
                <circle cx="-162" cy="0" r="4" fill="#4F46E5" />
                <text
                  x="-82"
                  y="4"
                  textAnchor="middle"
                  fontSize="11"
                  fontWeight="600"
                  fill="#3730A3"
                  fontFamily="'Space Grotesk', system-ui, sans-serif"
                >
                  {plotData.shadeRegion.label}
                </text>
              </g>
            </g>
          )}

          {/* Ejes X e Y */}
          <line
            x1={padLeft}
            y1={padTop + plotHeight}
            x2={padLeft + plotWidth}
            y2={padTop + plotHeight}
            stroke={colors.axis}
            strokeWidth={1.5}
          />
          <line
            x1={padLeft}
            y1={padTop}
            x2={padLeft}
            y2={padTop + plotHeight}
            stroke={colors.axis}
            strokeWidth={1.5}
          />

          {/* Ticks y etiquetas del Eje X */}
          {plotData.xTicks.map((tick, i) => (
            <g key={i} transform={`translate(${tick.px}, ${padTop + plotHeight})`}>
              <line y1="0" y2="5" stroke={colors.axis} strokeWidth={1.2} />
              <text
                y="18"
                textAnchor="middle"
                fontSize="11"
                fill={colors.textMuted}
                fontFamily="system-ui, -apple-system, sans-serif"
              >
                {tick.label}
              </text>
            </g>
          ))}

          {/* Nombre del Eje X */}
          <text
            x={padLeft + plotWidth / 2}
            y={height - 8}
            textAnchor="middle"
            fontSize="12"
            fontWeight="500"
            fill={colors.textMain}
            fontFamily="'Space Grotesk', system-ui, sans-serif"
          >
            {xLabel}
          </text>

          {/* Marcadores Verticales Destacados */}
          {plotData.verticalMarkers.map((marker, idx) => (
            <g key={idx} transform={`translate(${marker.px}, 0)`}>
              <line
                y1={padTop}
                y2={padTop + plotHeight}
                stroke="#6366F1"
                strokeWidth={1.2}
                strokeDasharray="4 3"
                opacity={0.8}
              />
              <rect
                x="-26"
                y={padTop - 20}
                width="52"
                height="18"
                rx="4"
                fill="#EEF2FF"
                stroke="#C7D2FE"
                strokeWidth="1"
              />
              <text
                x="0"
                y={padTop - 7}
                textAnchor="middle"
                fontSize="10"
                fontWeight="600"
                fill="#4338CA"
                fontFamily="'Space Grotesk', system-ui, sans-serif"
              >
                {marker.label}
              </text>
            </g>
          ))}

          {/* Curvas matemáticas */}
          {plotData.curves.map((curve) => {
            const pathD = curve.points.reduce((acc, pt, idx) => {
              return idx === 0 ? `M ${pt.px} ${pt.py}` : `${acc} L ${pt.px} ${pt.py}`;
            }, '');

            return (
              <path
                key={curve.id}
                d={pathD}
                fill="none"
                stroke={curve.stroke}
                strokeWidth={curve.strokeWidth}
                strokeDasharray={curve.strokeDasharray}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            );
          })}
        </svg>

        {/* Leyenda interactiva debajo del gráfico */}
        {plotData.curves.length > 0 && (
          <div className="mt-2 flex flex-wrap items-center justify-center gap-4 pt-1">
            {plotData.curves.map((curve) => (
              <div key={curve.id} className="flex items-center gap-2 text-xs font-medium text-gray-700">
                <span
                  className="inline-block h-2 w-5 rounded-full"
                  style={{
                    backgroundColor: curve.stroke,
                    borderStyle: curve.strokeDasharray ? 'dashed' : 'solid'
                  }}
                />
                <span>{curve.label}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
