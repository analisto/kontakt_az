/**
 * Core Simon Says game constants and configuration.
 * All timing values are in milliseconds.
 */

export type ButtonId = 'green' | 'red' | 'yellow' | 'blue';

export interface ButtonConfig {
  id: ButtonId;
  label: string;
  /** Dim background color (CSS hex) */
  baseColor: string;
  /** Lit/active background color (CSS hex) */
  activeColor: string;
  /** Neon glow color (CSS hex) */
  glowColor: string;
  /** Web Audio API oscillator frequency in Hz */
  frequency: number;
  /** Keyboard shortcut */
  key: string;
}

/**
 * Classic Simon Says button order:
 * top-left = green, top-right = red, bottom-left = yellow, bottom-right = blue
 */
export const BUTTONS: ButtonConfig[] = [
  {
    id: 'green',
    label: 'Green',
    baseColor: '#14532d',
    activeColor: '#22c55e',
    glowColor: '#22c55e',
    frequency: 392.0, // G4
    key: 'q',
  },
  {
    id: 'red',
    label: 'Red',
    baseColor: '#7f1d1d',
    activeColor: '#ef4444',
    glowColor: '#ef4444',
    frequency: 261.63, // C4
    key: 'e',
  },
  {
    id: 'yellow',
    label: 'Yellow',
    baseColor: '#713f12',
    activeColor: '#eab308',
    glowColor: '#eab308',
    frequency: 523.25, // C5
    key: 'a',
  },
  {
    id: 'blue',
    label: 'Blue',
    baseColor: '#1e3a5f',
    activeColor: '#3b82f6',
    glowColor: '#3b82f6',
    frequency: 329.63, // E4
    key: 'd',
  },
];

/** O(1) lookup of button config by id */
export const BUTTON_MAP = Object.fromEntries(
  BUTTONS.map((b) => [b.id, b])
) as Record<ButtonId, ButtonConfig>;

/** O(1) lookup of button config by keyboard key */
export const KEY_MAP = Object.fromEntries(
  BUTTONS.map((b) => [b.key, b])
) as Record<string, ButtonConfig>;

export type Difficulty = 'easy' | 'medium' | 'hard';

export interface DifficultyConfig {
  label: string;
  description: string;
  /** How long each button stays lit (ms) */
  litDuration: number;
  /** Gap between buttons in sequence (ms) */
  gapDuration: number;
}

export const DIFFICULTY_CONFIGS: DifficultyConfig[] = [
  { label: 'Easy', description: 'Slow & steady', litDuration: 800, gapDuration: 300 },
  { label: 'Medium', description: 'Normal pace', litDuration: 500, gapDuration: 200 },
  { label: 'Hard', description: 'Fast & furious', litDuration: 280, gapDuration: 80 },
];

export const DIFFICULTY_MAP = Object.fromEntries(
  DIFFICULTY_CONFIGS.map((d) => [d.label.toLowerCase(), d])
) as Record<Difficulty, DifficultyConfig>;
