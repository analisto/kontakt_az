# 🟢🔴🟡🔵 Simon Says — Neon Memory Game

A polished, neon-themed **Simon Says** memory game built with **Next.js 15**, **TypeScript**, and **Tailwind CSS**. Watch the sequence, repeat it, and see how far you can go!

---

## ✨ Features

- **Neon / cyberpunk visual theme** — deep space background, glowing buttons, shimmer title text
- **Smooth animations** — powered by Framer Motion (button glow, success ring, overlays, transitions)
- **3 difficulty levels** — Easy (slow), Medium (normal), Hard (fast)
- **Sound effects** — Web Audio API tones for each button, success jingle, and game-over buzz (no audio files needed)
- **Sound toggle** — mute/unmute at any time
- **High score persistence** — per-difficulty best scores saved to `localStorage`
- **Pause / Resume** — pause mid-sequence; sequence replays on resume
- **Full keyboard support** — play without a mouse
- **Touch-friendly** — works on mobile with large tap targets
- **Animated end screen** — game over overlay with score, high score, and "Play Again"
- **Fully responsive** — fits any viewport with no horizontal scrolling
- **Vercel-ready** — zero additional configuration required

---

## 🎮 Controls

### Keyboard
| Key | Action |
|-----|--------|
| `Q` | Green button (top-left) |
| `E` | Red button (top-right) |
| `A` | Yellow button (bottom-left) |
| `D` | Blue button (bottom-right) |
| `Space` / `P` | Pause / Resume |
| `Enter` | Start game (from idle screen) |

### Mouse / Touch
Click or tap any of the four colored buttons during your turn.

---

## 🧑‍💻 Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | [Next.js 15](https://nextjs.org/) (App Router) |
| Language | TypeScript (strict mode) |
| Styling | [Tailwind CSS v4](https://tailwindcss.com/) |
| Animations | [Framer Motion](https://www.framer.com/motion/) |
| Sound | Web Audio API (no audio files) |
| Persistence | `localStorage` |
| Deploy | [Vercel](https://vercel.com/) |

---

## 📁 Project Structure

```
simon_says/
├── app/
│   ├── favicon.svg          # Neon Simon favicon
│   ├── globals.css          # Global styles + custom animations
│   ├── layout.tsx           # Root layout + metadata
│   └── page.tsx             # Main game page
├── components/
│   ├── DifficultySelector.tsx  # Easy / Medium / Hard picker
│   ├── EndScreen.tsx           # Game over & paused overlays
│   ├── GameBoard.tsx           # 2×2 Simon board with center hub
│   ├── Header.tsx              # Title + sound toggle
│   ├── ScorePanel.tsx          # Score / round / high score display
│   └── SimonButton.tsx         # Individual neon button with glow
├── hooks/
│   ├── useHighScore.ts      # localStorage high score persistence
│   ├── useSimonGame.ts      # Core game state machine
│   └── useSound.ts          # Web Audio API sounds
└── utils/
    ├── constants.ts         # Button configs, difficulty configs
    └── gameLogic.ts         # Pure game logic helpers
```

---

## 🚀 Run Locally

### Prerequisites
- [Node.js](https://nodejs.org/) 18+
- npm (bundled with Node)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/simon_says.git
cd simon_says

# 2. Install dependencies
npm install

# 3. Start the development server
npm run dev

# 4. Open in browser
# http://localhost:3000
```

---

## ☁️ Deploy to Vercel

### Option A — Vercel CLI

```bash
npm i -g vercel
vercel
```

### Option B — GitHub Integration

1. Push your code to a GitHub repository
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Click **Deploy** — no extra configuration needed

The project is pre-configured for Vercel with `next.config.ts` and zero environment variables required.

---

## 📝 License

MIT — feel free to use, modify, and share.
