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
}: Props) {
  return (
    <motion.button
      aria-label={`${config.label} button${isActive ? ' (active)' : ''}`}
      aria-pressed={isActive}
      disabled={!isInteractive}
      onClick={onPress}
      // Tactile press animation — only when interactive
      whileTap={isInteractive ? { scale: 0.93 } : undefined}
      transition={{ type: 'spring', stiffness: 400, damping: 20 }}
      className={[
        'w-full h-full select-none outline-none focus-visible:ring-4 focus-visible:ring-white/50',
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
      {/* Subtle gloss highlight on the button face */}
      <span
        className={[
          'block w-full h-full rounded-[inherit]',
          'bg-gradient-to-br from-white/10 to-transparent',
          'pointer-events-none',
        ].join(' ')}
      />
    </motion.button>
  );
}
