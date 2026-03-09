'use client';

/**
 * Core Simon Says game state machine.
 *
 * Uses refs for mutable game data (avoids stale closures in setTimeout callbacks)
 * and useState only for the display slice that components need to re-render on.
 */

import { useState, useRef, useCallback } from 'react';
import type { ButtonId, Difficulty } from '../utils/constants';
import { BUTTON_MAP, DIFFICULTY_MAP } from '../utils/constants';
import { extendSequence, checkInput, roundScore } from '../utils/gameLogic';

// ------------------------------------------------------------------
// Types
// ------------------------------------------------------------------

export type Phase =
  | 'idle'         // before first start
  | 'showing'      // CPU is playing the sequence
  | 'player_turn'  // waiting for player input
  | 'success'      // round complete, brief celebration
  | 'game_over'    // player made a mistake
  | 'paused';      // game paused mid-round

export interface GameDisplay {
  phase: Phase;
  sequence: ButtonId[];
  activeButton: ButtonId | null;
  score: number;
  round: number;
  difficulty: Difficulty;
}

interface Callbacks {
  /** Called each time a button is shown/pressed — plays its tone */
  onTone: (frequency: number) => void;
  /** Called when player completes a round */
  onSuccess: () => void;
  /** Called when player presses the wrong button */
  onGameOver: () => void;
  /** Called at end of every round so high score can be persisted */
  onHighScore: (difficulty: Difficulty, score: number) => void;
}

// ------------------------------------------------------------------
// Hook
// ------------------------------------------------------------------

export function useSimonGame(callbacks: Callbacks) {
  const { onTone, onSuccess, onGameOver, onHighScore } = callbacks;

  // ── Mutable refs — mutated by timeouts without triggering re-renders ──
  const sequenceRef     = useRef<ButtonId[]>([]);
  const playerIndexRef  = useRef(0);
  const scoreRef        = useRef(0);
  const difficultyRef   = useRef<Difficulty>('medium');
  const phaseRef        = useRef<Phase>('idle');
  const timersRef       = useRef<ReturnType<typeof setTimeout>[]>([]);

  // ── Display state — drives component re-renders ──────────────────────
  const [display, setDisplay] = useState<GameDisplay>({
    phase: 'idle',
    sequence: [],
    activeButton: null,
    score: 0,
    round: 0,
    difficulty: 'medium',
  });

  // ── Timer helpers ─────────────────────────────────────────────────────

  const clearTimers = useCallback(() => {
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];
  }, []);

  const schedule = useCallback((fn: () => void, delay: number) => {
    const id = setTimeout(fn, delay);
    timersRef.current.push(id);
    return id;
  }, []);

  // ── Sequence playback ─────────────────────────────────────────────────

  /**
   * Animates the Simon sequence on the board, then transitions to player_turn.
   * Safe to call at any time — always clears previous timers first.
   */
  const playSequence = useCallback(
    (seq: ButtonId[], difficulty: Difficulty) => {
      clearTimers();

      phaseRef.current = 'showing';
      setDisplay((prev) => ({
        ...prev,
        phase: 'showing',
        activeButton: null,
        sequence: seq,
      }));

      const { litDuration, gapDuration } = DIFFICULTY_MAP[difficulty];
      let t = 500; // initial pause before first blink

      for (const id of seq) {
        const btnId = id; // capture for closure
        const startAt = t;

        // Light up
        schedule(() => {
          setDisplay((prev) => ({ ...prev, activeButton: btnId }));
          onTone(BUTTON_MAP[btnId].frequency);
        }, startAt);

        // Dim
        schedule(() => {
          setDisplay((prev) => ({ ...prev, activeButton: null }));
        }, startAt + litDuration);

        t += litDuration + gapDuration;
      }

      // Hand over to player
      schedule(() => {
        phaseRef.current = 'player_turn';
        playerIndexRef.current = 0;
        setDisplay((prev) => ({
          ...prev,
          phase: 'player_turn',
          activeButton: null,
        }));
      }, t);
    },
    [clearTimers, schedule, onTone]
  );

  // ── Public actions ────────────────────────────────────────────────────

  /** Change difficulty — only effective before the game starts */
  const setDifficulty = useCallback((d: Difficulty) => {
    difficultyRef.current = d;
    setDisplay((prev) => ({ ...prev, difficulty: d }));
  }, []);

  /** Start a fresh game */
  const start = useCallback(() => {
    clearTimers();
    scoreRef.current = 0;
    playerIndexRef.current = 0;

    const seq = extendSequence([]);
    sequenceRef.current = seq;

    setDisplay({
      phase: 'showing',
      sequence: seq,
      activeButton: null,
      score: 0,
      round: 1,
      difficulty: difficultyRef.current,
    });

    playSequence(seq, difficultyRef.current);
  }, [clearTimers, playSequence]);

  /**
   * Register a player button press.
   * No-op if not in player_turn phase.
   */
  const pressButton = useCallback(
    (btnId: ButtonId) => {
      if (phaseRef.current !== 'player_turn') return;

      // Brief visual + audio feedback for the pressed button
      onTone(BUTTON_MAP[btnId].frequency);
      setDisplay((prev) => ({ ...prev, activeButton: btnId }));
      schedule(() => {
        setDisplay((prev) => ({ ...prev, activeButton: null }));
      }, 200);

      const idx = playerIndexRef.current;
      const result = checkInput(sequenceRef.current, idx, btnId);

      if (result === 'wrong') {
        // ── Game Over ─────────────────────────────────────
        clearTimers();
        phaseRef.current = 'game_over';
        setDisplay((prev) => ({ ...prev, phase: 'game_over' }));
        onGameOver();
        onHighScore(difficultyRef.current, scoreRef.current);
        return;
      }

      if (result === 'incomplete') {
        // Correct so far — advance player index and wait for next press
        playerIndexRef.current += 1;
        return;
      }

      // ── Round complete ────────────────────────────────────
      const earned = roundScore(sequenceRef.current.length);
      scoreRef.current += earned;
      const newScore = scoreRef.current;

      const nextSeq = extendSequence(sequenceRef.current);
      sequenceRef.current = nextSeq;

      phaseRef.current = 'success';
      setDisplay((prev) => ({
        ...prev,
        phase: 'success',
        score: newScore,
        sequence: nextSeq,
        round: nextSeq.length,
      }));

      onSuccess();
      onHighScore(difficultyRef.current, newScore);

      // Short celebration pause, then show next (longer) sequence
      schedule(() => {
        playSequence(nextSeq, difficultyRef.current);
      }, 900);
    },
    [clearTimers, schedule, onTone, onSuccess, onGameOver, onHighScore, playSequence]
  );

  /** Pause mid-game (works during showing or player_turn) */
  const pause = useCallback(() => {
    if (
      phaseRef.current !== 'player_turn' &&
      phaseRef.current !== 'showing'
    )
      return;

    clearTimers();
    phaseRef.current = 'paused';
    setDisplay((prev) => ({ ...prev, phase: 'paused' }));
  }, [clearTimers]);

  /** Resume from pause — always re-shows the current sequence */
  const resume = useCallback(() => {
    if (phaseRef.current !== 'paused') return;
    playSequence(sequenceRef.current, difficultyRef.current);
  }, [playSequence]);

  /** Return to the idle screen */
  const reset = useCallback(() => {
    clearTimers();
    sequenceRef.current = [];
    playerIndexRef.current = 0;
    scoreRef.current = 0;
    phaseRef.current = 'idle';

    setDisplay((prev) => ({
      phase: 'idle',
      sequence: [],
      activeButton: null,
      score: 0,
      round: 0,
      difficulty: prev.difficulty,
    }));
  }, [clearTimers]);

  return { display, setDifficulty, start, pressButton, pause, resume, reset };
}
