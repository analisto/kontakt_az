'use client';

/**
 * A single Simon Says colored button.
 * Lights up with a neon glow when active; dims when inactive.
 * Accepts both click and keyboard events via the parent's handler.
 */

import { motion } from 'framer-motion';
import type { ButtonConfig } from '../utils/constants';

interface Props {
  config: ButtonConfig;
  /** Whether this button is currently lit (CPU showing or player pressing it) */
  isActive: boolean;
  /** Whether the player can interact right now */
  isInteractive: boolean;
  /** Called when the player presses this button */
  onPress: () => void;
  /** Which corner of the 2×2 grid this button occupies */
  corner: 'tl' | 'tr' | 'bl' | 'br';
  /** Show color name + key hint label (idle / player turn) */
  showLabel?: boolean;
}

/** Outer corner radius per grid position (large outer, small inner) */
const CORNER_RADIUS: Record<Props['corner'], string> = {
  tl: 'rounded-tl-[44%] rounded-tr-xl rounded-bl-xl rounded-br-md',
  tr: 'rounded-tr-[44%] rounded-tl-xl rounded-br-xl rounded-bl-md',
  bl: 'rounded-bl-[44%] rounded-br-xl rounded-tl-xl rounded-tr-md',
  br: 'rounded-br-[44%] rounded-bl-xl rounded-tr-xl rounded-tl-md',
};

export default function SimonButton({
  config,
  isActive,
  isInteractive,
  onPress,
  corner,
  showLabel = false,
}: Props) {
  return (
    <motion.button
      aria-label={`${config.label} button${isActive ? ' (active)' : ''}`}
      aria-pressed={isActive}
      disabled={!isInteractive}
      onClick={onPress}
      whileTap={isInteractive ? { scale: 0.93 } : undefined}
      transition={{ type: 'spring', stiffness: 400, damping: 20 }}
      className={[
        'w-full h-full select-none outline-none focus-visible:ring-4 focus-visible:ring-white/50',
        'relative flex items-center justify-center',
        'transition-[background-color,box-shadow] duration-100',
        CORNER_RADIUS[corner],
        isInteractive ? 'cursor-pointer' : 'cursor-default',
      ].join(' ')}
      style={{
        backgroundColor: isActive ? config.activeColor : config.baseColor,
        boxShadow: isActive
          ? `0 0 24px 6px ${config.glowColor}cc, 0 0 60px 10px ${config.glowColor}44`
          : `inset 0 2px 4px rgba(0,0,0,0.5)`,
      }}
    >
      {/* Gloss highlight */}
      <span
        className="absolute inset-0 rounded-[inherit] bg-gradient-to-br from-white/10 to-transparent pointer-events-none"
      />

      {/* Color name + keyboard shortcut label */}
      {showLabel && (
        <span className="relative flex flex-col items-center gap-0.5 pointer-events-none select-none">
          <span
            className="text-xs sm:text-sm font-bold uppercase tracking-widest"
            style={{ color: isActive ? '#fff' : `${config.activeColor}cc` }}
          >
            {config.label}
          </span>
          <kbd
            className="text-[10px] sm:text-xs font-mono px-1.5 py-0.5 rounded border"
            style={{
              color: isActive ? '#fff' : `${config.activeColor}99`,
              borderColor: isActive ? '#ffffff60' : `${config.activeColor}44`,
              backgroundColor: 'rgba(0,0,0,0.3)',
            }}
          >
            {config.key.toUpperCase()}
          </kbd>
        </span>
      )}
    </motion.button>
  );
}
