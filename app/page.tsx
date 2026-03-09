'use client';

/**
 * Simon Says — main game page.
 *
 * Keyboard controls:
 *   Q = Green (top-left)     E = Red (top-right)
 *   A = Yellow (bottom-left) D = Blue (bottom-right)
 *   Space / P = Pause / Resume
 *   Enter = Start (on idle screen)
 */

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

import Header             from '../components/Header';
import GameBoard          from '../components/GameBoard';
import ScorePanel         from '../components/ScorePanel';
import DifficultySelector from '../components/DifficultySelector';
import EndScreen          from '../components/EndScreen';

import { useSimonGame }   from '../hooks/useSimonGame';
import { useSound }       from '../hooks/useSound';
import { useHighScore }   from '../hooks/useHighScore';

import { KEY_MAP }        from '../utils/constants';

export default function SimonSaysPage() {
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [newHighScore, setNewHighScore]  = useState(false);

  // ── Sound ──────────────────────────────────────────────────────────
  const { tone, playSuccess, playGameOver } = useSound(soundEnabled);

  // ── High scores ────────────────────────────────────────────────────
  const { scores, submit: submitHighScore } = useHighScore();

  // ── Game state machine ─────────────────────────────────────────────
  const { display, setDifficulty, start, pressButton, pause, resume, reset } =
    useSimonGame({
      onTone: tone,
      onSuccess: playSuccess,
      onGameOver: playGameOver,
      onHighScore: (difficulty, score) => {
        const isNew = submitHighScore(difficulty, score);
        setNewHighScore(isNew);
      },
    });

  const { phase, activeButton, score, round, difficulty } = display;

  // Clear new-high-score flag when a fresh game begins
  useEffect(() => {
    if (phase === 'showing' && round === 1) setNewHighScore(false);
  }, [phase, round]);

  // ── Keyboard controls ──────────────────────────────────────────────
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.repeat) return;
      const key = e.key.toLowerCase();

      // Pause / Resume
      if ((key === ' ' || key === 'p') && phase !== 'idle' && phase !== 'game_over') {
        e.preventDefault();
        phase === 'paused' ? resume() : pause();
        return;
      }

      // Start from idle screen
      if (key === 'enter' && phase === 'idle') {
        start();
        return;
      }

      // Button presses
      if (phase === 'player_turn') {
        const btn = KEY_MAP[key];
        if (btn) pressButton(btn.id);
      }
    },
    [phase, start, pressButton, pause, resume]
  );

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  const isInteractive = phase === 'player_turn';
  // Show labels on buttons when idle or during player's turn
  const showLabels = phase === 'idle' || phase === 'player_turn';

  return (
    <main
      className={[
        'min-h-dvh w-full flex flex-col items-center justify-center',
        'px-4 py-6 gap-4',
        'bg-[radial-gradient(ellipse_at_top,_#1e1040_0%,_#06060f_70%)]',
      ].join(' ')}
    >
      {/* ── Header ─────────────────────────────────────────────────── */}
      <Header
        soundEnabled={soundEnabled}
        onToggleSound={() => setSoundEnabled((s) => !s)}
      />

      {/* ── Score panel (hidden on idle) ────────────────────────────── */}
      {phase !== 'idle' && (
        <ScorePanel
          score={score}
          round={round}
          difficulty={difficulty}
          highScore={scores[difficulty]}
        />
      )}

      {/* ── Game board ─────────────────────────────────────────────── */}
      <div className="relative w-full flex justify-center">
        {/* Green success ring flash */}
        <AnimatePresence>
          {phase === 'success' && (
            <motion.div
              key="success-ring"
              initial={{ opacity: 0.9, scale: 0.95 }}
              animate={{ opacity: 0, scale: 1.18 }}
              transition={{ duration: 0.55, ease: 'easeOut' }}
              className={[
                'absolute inset-0 max-w-[360px] sm:max-w-[420px] mx-auto aspect-square',
                'rounded-3xl border-4 border-green-400 pointer-events-none z-10',
              ].join(' ')}
              style={{ boxShadow: '0 0 40px 12px #22c55e40' }}
            />
          )}
        </AnimatePresence>

        {/* Board floats gently on idle screen */}
        <div className={phase === 'idle' ? 'animate-float' : ''}>
          <GameBoard
            activeButton={activeButton}
            isInteractive={isInteractive}
            onPress={pressButton}
            showLabels={showLabels}
          />

          {/* Game over / paused overlay */}
          <EndScreen
            phase={phase}
            score={score}
            highScore={scores[difficulty]}
            difficulty={difficulty}
            isNewHighScore={newHighScore}
            onRestart={reset}
            onResume={resume}
          />
        </div>
      </div>

      {/* ── Status banner (showing / player_turn / success / paused) ── */}
      <AnimatePresence mode="wait">
        {phase !== 'idle' && phase !== 'game_over' && (
          <motion.div
            key={phase}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            transition={{ duration: 0.2 }}
            className={[
              'w-full max-w-[420px] py-3 px-4 rounded-xl text-center font-semibold text-sm',
              phase === 'player_turn'
                ? 'bg-violet-600/30 border border-violet-400/50 text-violet-200'
                : phase === 'success'
                ? 'bg-green-600/30 border border-green-400/50 text-green-200'
                : 'bg-white/5 border border-white/10 text-white/60',
            ].join(' ')}
          >
            {phase === 'showing'     && '👀 Watch the sequence carefully…'}
            {phase === 'player_turn' && '👆 Your turn! Tap the buttons in the same order.'}
            {phase === 'success'     && '✅ Correct! Get ready for the next round…'}
            {phase === 'paused'      && '⏸ Game paused'}
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Controls ───────────────────────────────────────────────── */}
      <AnimatePresence mode="wait">
        {phase === 'idle' ? (
          <motion.div
            key="idle-controls"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -10, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="flex flex-col items-center gap-3 w-full max-w-[420px]"
          >
            {/* ── How to Play card ───────────────────────────────── */}
            <div className="w-full rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs font-bold uppercase tracking-widest text-white/40 mb-2">
                How to Play
              </p>
              <ol className="text-sm text-white/70 space-y-1.5 list-none">
                <li>
                  <span className="text-violet-400 font-bold mr-1">1.</span>
                  Watch the buttons light up in sequence.
                </li>
                <li>
                  <span className="text-violet-400 font-bold mr-1">2.</span>
                  Repeat the exact same sequence by tapping the buttons.
                </li>
                <li>
                  <span className="text-violet-400 font-bold mr-1">3.</span>
                  Each round adds one more button to the sequence.
                </li>
                <li>
                  <span className="text-violet-400 font-bold mr-1">4.</span>
                  One wrong press and the game is over!
                </li>
              </ol>
              <p className="text-xs text-white/30 mt-3">
                Keyboard: <kbd className="font-mono text-white/50 bg-white/10 px-1 rounded">Q</kbd> Green &nbsp;
                <kbd className="font-mono text-white/50 bg-white/10 px-1 rounded">E</kbd> Red &nbsp;
                <kbd className="font-mono text-white/50 bg-white/10 px-1 rounded">A</kbd> Yellow &nbsp;
                <kbd className="font-mono text-white/50 bg-white/10 px-1 rounded">D</kbd> Blue &nbsp;·&nbsp;
                <kbd className="font-mono text-white/50 bg-white/10 px-1 rounded">Space</kbd> Pause
              </p>
            </div>

            <DifficultySelector selected={difficulty} onChange={setDifficulty} />

            <motion.button
              onClick={start}
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.96 }}
              className={[
                'w-full py-4 rounded-2xl text-xl font-extrabold tracking-wide',
                'bg-violet-600 hover:bg-violet-500 text-white',
                'shadow-[0_0_30px_6px_#7c3aed80]',
                'transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400',
              ].join(' ')}
            >
              ▶ Start Game
            </motion.button>
          </motion.div>
        ) : (
          <motion.div
            key="game-controls"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -10, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="flex gap-3 w-full max-w-[420px]"
          >
            {/* Pause button */}
            {(phase === 'showing' || phase === 'player_turn' || phase === 'success') && (
              <motion.button
                onClick={pause}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.96 }}
                className={[
                  'flex-1 py-3 rounded-xl font-bold text-sm',
                  'bg-white/10 hover:bg-white/20 border border-white/20 text-white/80',
                  'transition-colors focus-visible:outline-none',
                ].join(' ')}
              >
                ⏸ Pause
              </motion.button>
            )}

            {/* Resume button when paused */}
            {phase === 'paused' && (
              <motion.button
                onClick={resume}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.96 }}
                className={[
                  'flex-1 py-3 rounded-xl font-bold text-sm',
                  'bg-green-600 hover:bg-green-500 text-white',
                  'transition-colors focus-visible:outline-none',
                ].join(' ')}
              >
                ▶ Resume
              </motion.button>
            )}

            {/* Back to menu */}
            <motion.button
              onClick={reset}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.96 }}
              className={[
                'flex-1 py-3 rounded-xl font-bold text-sm',
                'bg-white/5 hover:bg-white/10 border border-white/15 text-white/60',
                'transition-colors focus-visible:outline-none',
              ].join(' ')}
            >
              ↩ Menu
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
