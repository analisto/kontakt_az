'use client';

/**
 * Top bar: game title + sound toggle.
 * Title uses an animated gradient shimmer effect.
 */

import { motion } from 'framer-motion';

interface Props {
  soundEnabled: boolean;
  onToggleSound: () => void;
}

export default function Header({ soundEnabled, onToggleSound }: Props) {
  return (
    <header className="flex items-center justify-between w-full max-w-[420px] mx-auto px-1">
      {/* Logo / title */}
      <motion.div
        initial={{ x: -20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="flex flex-col leading-none"
      >
        <span className="text-2xl sm:text-3xl font-black tracking-tight shimmer-text">
          SIMON
        </span>
        <span className="text-[10px] sm:text-xs font-semibold uppercase tracking-[0.25em] text-white/40 -mt-0.5">
          Memory Game
        </span>
      </motion.div>

      {/* Sound toggle */}
      <motion.button
        initial={{ x: 20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        onClick={onToggleSound}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        aria-label={soundEnabled ? 'Mute sound' : 'Enable sound'}
        className={[
          'w-10 h-10 rounded-xl flex items-center justify-center text-xl',
          'bg-white/5 border border-white/10',
          'hover:bg-white/10 transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/40',
        ].join(' ')}
      >
        {soundEnabled ? '🔊' : '🔇'}
      </motion.button>
    </header>
  );
}
