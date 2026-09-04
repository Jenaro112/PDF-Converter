'use client';

import React from 'react';
import { useEditorStore } from '@/store/editor-store';
import { BarraAzulCover } from './strategies/BarraAzulCover';
import { BlancaSimpleCover } from './strategies/BlancaSimpleCover';
import { FcytUaderCover } from './strategies/FcytUaderCover';
import type { CoverData } from '@/store/editor-store';

const COVER_STRATEGIES: Record<string, React.FC<{ config: CoverData }>> = {
  barra_azul:   BarraAzulCover,
  blanca_simple: BlancaSimpleCover,
  fcyt_uader:   FcytUaderCover,
};

export function CoverRenderer() {
  const { coverConfig } = useEditorStore();
  
  if (!coverConfig || !coverConfig.showCover) return null;
  
  const Strategy = COVER_STRATEGIES[coverConfig.coverStyle];
  
  if (!Strategy) {
    console.warn(`Estilo de portada no encontrado: ${coverConfig.coverStyle}`);
    return null;
  }

  return <Strategy config={coverConfig} />;
}
