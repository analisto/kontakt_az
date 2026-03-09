'use client';

/**
 * Web Audio API sound utilities for Simon Says.
 * Creates tones and jingles without any audio files.
 */

import { useRef, useCallback } from 'react';

export function useSound(enabled: boolean) {
  const ctxRef = useRef<AudioContext | null>(null);

  /** Lazily creates and returns the AudioContext */
  function getCtx(): AudioContext {
    if (!ctxRef.current) {
      ctxRef.current = new (
        window.AudioContext ||
        // Safari fallback
        (window as unknown as { webkitAudioContext: typeof AudioContext })
          .webkitAudioContext
      )();
    }
    // Resume context if browser suspended it (autoplay policy)
    if (ctxRef.current.state === 'suspended') {
      ctxRef.current.resume();
    }
    return ctxRef.current;
  }

  /**
   * Plays a single oscillator tone.
   * @param frequency  Hz
   * @param duration   seconds
   * @param type       oscillator waveform
   */
  const tone = useCallback(
    (
      frequency: number,
      duration = 0.35,
      type: OscillatorType = 'sine'
    ) => {
      if (!enabled) return;
      const ac = getCtx();
      const osc = ac.createOscillator();
      const gain = ac.createGain();

      osc.connect(gain);
      gain.connect(ac.destination);

      osc.type = type;
      osc.frequency.setValueAtTime(frequency, ac.currentTime);
      gain.gain.setValueAtTime(0.28, ac.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + duration);

      osc.start(ac.currentTime);
      osc.stop(ac.currentTime + duration);
    },
    [enabled] // eslint-disable-line react-hooks/exhaustive-deps
  );

  /** Ascending success jingle (four notes) */
  const playSuccess = useCallback(() => {
    if (!enabled) return;
    [523.25, 659.25, 783.99, 1046.5].forEach((f, i) =>
      setTimeout(() => tone(f, 0.15), i * 90)
    );
  }, [enabled, tone]);

  /** Descending game-over buzz */
  const playGameOver = useCallback(() => {
    if (!enabled) return;
    [330, 220, 165, 110].forEach((f, i) =>
      setTimeout(() => tone(f, 0.3, 'sawtooth'), i * 180)
    );
  }, [enabled, tone]);

  return { tone, playSuccess, playGameOver };
}
