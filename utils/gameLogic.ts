/**
 * Pure utility functions for Simon Says game logic.
 * No side-effects — safe to test in isolation.
 */

import { ButtonId, BUTTONS } from './constants';

/** Returns a random button id from the 4 choices */
export function randomButton(): ButtonId {
  return BUTTONS[Math.floor(Math.random() * BUTTONS.length)].id;
}

/** Appends one new random button to an existing sequence */
export function extendSequence(seq: ButtonId[]): ButtonId[] {
  return [...seq, randomButton()];
}

/**
 * Validates a player's input against the target sequence.
 *
 * @returns
 *  - `'wrong'`      – player pressed the wrong button
 *  - `'incomplete'` – input is correct so far but sequence not fully entered
 *  - `'correct'`    – full sequence entered correctly
 */
export function checkInput(
  sequence: ButtonId[],
  inputIndex: number,
  pressed: ButtonId
): 'correct' | 'incomplete' | 'wrong' {
  if (pressed !== sequence[inputIndex]) return 'wrong';
  if (inputIndex + 1 === sequence.length) return 'correct';
  return 'incomplete';
}

/** Calculates score for completing a round (length of sequence) */
export function roundScore(sequenceLength: number): number {
  return sequenceLength;
}
