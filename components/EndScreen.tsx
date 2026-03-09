'use client';

/**
 * Animated full-screen overlay shown when the game ends.
 * Covers game over and the paused state.
 */

import { motion, AnimatePresence } from 'framer-motion';
import type { Phase } from '../hooks/useSimonGame';
import type { Difficulty } from '../utils/constants';

interface Props {
  phase: Phase;
  score: number;
  highScore: number;
  difficulty: Difficulty;
  isNewHighScore: boolean;
  onRestart: () => void;
  onResume?: () => void;
}

const DIFFICULTY_LABELS: Record<Difficulty, string> = {
  easy: 'Easy',
  medium: 'Medium',
  hard: 'Hard',
};

export default function EndScreen({
  phase,
  score,
  highScore,
  difficulty,
  isNewHighScore,
  onRestart,
  onResume,
}: Props) {
  const visible = phase === 'game_over' || phase === 'paused';

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          key={phase}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.25 }}
          className={[
            'absolute inset-0 z-20 flex flex-col items-center justify-center',
            'rounded-2xl backdrop-blur-md',
            phase === 'game_over' ? 'bg-black/70' : 'bg-black/60',
          ].join(' ')}
        >
          {phase === 'game_over' ? (
            <>
              {/* Title */}
              <motion.div
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: 'spring', stiffness: 260, damping: 18, delay: 0.05 }}
                className="text-5xl font-black tracking-tight mb-1"
                style={{ color: '#ef4444', textShadow: '0 0 30px #ef4444' }}
              >
                GAME OVER
              </motion.div>

              {/* Score block */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="flex flex-col items-center mt-3 mb-5 gap-1"
              >
                <span className="text-white/50 text-sm uppercase tracking-widest">
                  Your Score
                </span>
                <span className="text-5xl font-extrabold text-white tabular-nums">
                  {score}
                </span>

                {isNewHighScore ? (
                  <motion.span
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: [1, 1.15, 1], opacity: 1 }}
                    transition={{ delay: 0.4, duration: 0.5 }}
                    className="text-yellow-400 font-bold text-sm mt-1 px-3 py-1 rounded-full bg-yellow-400/15 border border-yellow-400/40"
                    style={{ textShadow: '0 0 12px #eab308' }}
                  >
                    🏆 New High Score!
                  </motion.span>
                ) : (
                  <span className="text-white/40 text-xs mt-1">
                    Best ({DIFFICULTY_LABELS[difficulty]}): {highScore}
                  </span>
                )}
              </motion.div>

              {/* Actions */}
              <motion.button
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
                onClick={onRestart}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.96 }}
                className={[
                  'px-10 py-3 rounded-xl text-lg font-bold',
                  'bg-violet-600 hover:bg-violet-500 text-white',
                  'shadow-[0_0_20px_4px_#7c3aed80]',
                  'transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400',
                ].join(' ')}
              >
                Play Again
              </motion.button>
            </>
          ) : (
            /* ── Paused ────────────────────────────────────────── */
            <>
              <motion.div
                initial={{ scale: 0.7, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                className="text-4xl font-black text-white/90 tracking-wide mb-6"
              >
                PAUSED
              </motion.div>

              <div className="flex gap-3">
                {onResume && (
                  <motion.button
                    initial={{ y: 10, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    onClick={onResume}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.96 }}
                    className={[
                      'px-8 py-3 rounded-xl text-base font-bold',
                      'bg-green-600 hover:bg-green-500 text-white',
                      'shadow-[0_0_16px_3px_#22c55e60]',
                      'transition-colors focus-visible:outline-none',
                    ].join(' ')}
                  >
                    Resume
                  </motion.button>
                )}

                <motion.button
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.15 }}
                  onClick={onRestart}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.96 }}
                  className={[
                    'px-8 py-3 rounded-xl text-base font-bold',
                    'bg-white/10 hover:bg-white/20 text-white/80',
                    'border border-white/20',
                    'transition-colors focus-visible:outline-none',
                  ].join(' ')}
                >
                  Restart
                </motion.button>
              </div>
            </>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
