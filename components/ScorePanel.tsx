'use client';

/**
 * Displays current score, round number, and difficulty-specific high score.
 */

import { motion, AnimatePresence } from 'framer-motion';
import type { Difficulty } from '../utils/constants';

interface Props {
  score: number;
  round: number;
  difficulty: Difficulty;
  highScore: number;
}

function Stat({
  label,
  value,
  highlight,
}: {
  label: string;
  value: string | number;
  highlight?: boolean;
}) {
  return (
    <div className="flex flex-col items-center gap-0.5">
      <span className="text-xs font-semibold uppercase tracking-widest text-white/40">
        {label}
      </span>
      <AnimatePresence mode="popLayout">
        <motion.span
          key={String(value)}
          initial={{ y: -10, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 10, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          className={[
            'text-2xl sm:text-3xl font-bold tabular-nums',
            highlight ? 'text-yellow-400' : 'text-white',
          ].join(' ')}
        >
          {value}
        </motion.span>
      </AnimatePresence>
    </div>
  );
}

const DIFFICULTY_LABELS: Record<Difficulty, string> = {
  easy: 'Easy',
  medium: 'Medium',
  hard: 'Hard',
};

export default function ScorePanel({ score, round, difficulty, highScore }: Props) {
  return (
    <div
      className={[
        'w-full max-w-[420px] mx-auto',
        'grid grid-cols-3 gap-2',
        'px-4 py-3 rounded-2xl',
        'bg-white/5 border border-white/10 backdrop-blur-sm',
      ].join(' ')}
    >
      <Stat label="Score" value={score} />
      <Stat label="Round" value={round || '-'} />
      <div className="flex flex-col items-center gap-0.5">
        <span className="text-xs font-semibold uppercase tracking-widest text-white/40">
          Best&nbsp;
          <span className="text-yellow-400/70">{DIFFICULTY_LABELS[difficulty]}</span>
        </span>
        <span className="text-2xl sm:text-3xl font-bold tabular-nums text-yellow-400">
          {highScore || '-'}
        </span>
      </div>
    </div>
  );
}
