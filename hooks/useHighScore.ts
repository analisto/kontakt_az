'use client';

/**
 * Persists per-difficulty high scores in localStorage.
 * Safe to call on the server — effects only run client-side.
 */

import { useState, useEffect } from 'react';
import type { Difficulty } from '../utils/constants';

const STORAGE_KEY = 'simon-says-highscores-v1';

type HighScores = Record<Difficulty, number>;

const DEFAULT: HighScores = { easy: 0, medium: 0, hard: 0 };

export function useHighScore() {
  const [scores, setScores] = useState<HighScores>(DEFAULT);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) setScores({ ...DEFAULT, ...JSON.parse(raw) });
    } catch {
      // ignore malformed data
    }
  }, []);

  /**
   * Submit a score for a given difficulty.
   * Only saves if it exceeds the current high score.
   * Returns whether the new score IS a new record.
   */
  function submit(difficulty: Difficulty, score: number): boolean {
    if (score <= scores[difficulty]) return false;
    const next = { ...scores, [difficulty]: score };
    setScores(next);
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      // storage full — ignore
    }
    return true;
  }

  return { scores, submit };
}
