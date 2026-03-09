'use client';

/**
 * Difficulty picker shown on the idle screen.
 * Renders Easy / Medium / Hard buttons.
 */

import { motion } from 'framer-motion';
import { DIFFICULTY_CONFIGS } from '../utils/constants';
import type { Difficulty } from '../utils/constants';

interface Props {
  selected: Difficulty;
  onChange: (d: Difficulty) => void;
}

/** Neon accent colour per difficulty */
const ACCENT: Record<Difficulty, { ring: string; text: string; glow: string }> = {
  easy:   { ring: 'border-green-500',  text: 'text-green-400',  glow: 'shadow-[0_0_12px_2px_#22c55e80]' },
  medium: { ring: 'border-yellow-400', text: 'text-yellow-300', glow: 'shadow-[0_0_12px_2px_#eab30880]' },
  hard:   { ring: 'border-red-500',    text: 'text-red-400',    glow: 'shadow-[0_0_12px_2px_#ef444480]' },
};

export default function DifficultySelector({ selected, onChange }: Props) {
  return (
    <div
      className="flex gap-3 justify-center w-full"
      role="radiogroup"
      aria-label="Difficulty"
    >
      {DIFFICULTY_CONFIGS.map((d) => {
        const key = d.label.toLowerCase() as Difficulty;
        const isSelected = selected === key;
        const accent = ACCENT[key];

        return (
          <motion.button
            key={key}
            role="radio"
            aria-checked={isSelected}
            onClick={() => onChange(key)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.96 }}
            transition={{ type: 'spring', stiffness: 400, damping: 20 }}
            className={[
              'flex-1 max-w-[110px] py-2.5 px-2 rounded-xl border-2',
              'transition-all duration-200 text-center',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50',
              isSelected
                ? `${accent.ring} bg-white/10 ${accent.glow}`
                : 'border-white/15 bg-white/5 text-white/50 hover:border-white/30',
            ].join(' ')}
          >
            <span
              className={[
                'block text-sm font-bold',
                isSelected ? accent.text : '',
              ].join(' ')}
            >
              {d.label}
            </span>
            <span className="block text-[10px] mt-0.5 text-white/40">
              {d.description}
            </span>
          </motion.button>
        );
      })}
    </div>
  );
}
