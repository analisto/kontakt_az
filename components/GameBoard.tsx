'use client';

/**
 * The main 2×2 Simon Says board.
 * Renders four colored buttons in the classic layout with a dark center hub.
 */

import SimonButton from './SimonButton';
import { BUTTONS } from '../utils/constants';
import type { ButtonId, ButtonConfig } from '../utils/constants';

interface Props {
  activeButton: ButtonId | null;
  isInteractive: boolean;
  onPress: (id: ButtonId) => void;
}

/** Corner assignment in grid order: [0]=tl, [1]=tr, [2]=bl, [3]=br */
const CORNERS: Array<'tl' | 'tr' | 'bl' | 'br'> = ['tl', 'tr', 'bl', 'br'];

export default function GameBoard({ activeButton, isInteractive, onPress }: Props) {
  return (
    <div
      className="relative w-full max-w-[360px] sm:max-w-[420px] aspect-square mx-auto"
      role="group"
      aria-label="Simon Says game board"
    >
      {/* 2×2 button grid */}
      <div className="grid grid-cols-2 gap-3 w-full h-full p-1">
        {BUTTONS.map((config: ButtonConfig, i) => (
          <SimonButton
            key={config.id}
            config={config}
            isActive={activeButton === config.id}
            isInteractive={isInteractive}
            onPress={() => onPress(config.id)}
            corner={CORNERS[i]}
          />
        ))}
      </div>

      {/* Center hub overlay */}
      <div
        className={[
          'absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2',
          'w-[22%] h-[22%] rounded-full z-10',
          'bg-gray-950 border-2 border-white/10',
          'flex items-center justify-center',
          'shadow-[0_0_0_4px_rgba(0,0,0,0.8)]',
        ].join(' ')}
        aria-hidden="true"
      >
        {/* Simon logo dot */}
        <div className="w-3 h-3 rounded-full bg-white/20" />
      </div>
    </div>
  );
}
