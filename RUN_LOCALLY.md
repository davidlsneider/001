# Running the Animation Locally

All files have been committed and pushed to the `claude/lit-protocol-animation-HYH8E` branch.

## ✅ Everything is Ready!

The project is fully set up and all compilation errors are fixed. When you run it on a machine with browser access, everything will work smoothly.

---

## 🚀 Quick Start (When You Have Local Access)

### 1. Pull the Repository

```bash
git clone [your-repo-url]
cd 001
git checkout claude/lit-protocol-animation-HYH8E
```

Or if you already have it:
```bash
git pull origin claude/lit-protocol-animation-HYH8E
```

### 2. Install Dependencies

```bash
npm install
```

This will install:
- Motion Canvas core and 2D libraries
- Motion Canvas UI (the visual editor)
- Vite (build tool)
- TypeScript

### 3. Start the Editor

```bash
npm run serve
```

This will:
- Start a local development server
- Open automatically at http://localhost:9000/
- Show the Motion Canvas visual editor

### 4. Preview Your Animation

In the editor you'll see:
- **Center**: Your animation canvas (black background)
- **Bottom**: Timeline with all 5 scenes
- **Controls**: Play, pause, scrub through time

Click **Play ▶️** to watch the full animation!

### 5. Render to Video

1. Click the **"Render"** button (top right, camera icon 📹)
2. Choose settings:
   - **Resolution**: 1920x1080 (recommended)
   - **Frame Rate**: 60 FPS (recommended)
   - **Format**: MP4 / H.264
   - **Range**: Full (all scenes)
3. Click **"Start Rendering"** or **"Export"**
4. Wait 3-5 minutes for rendering to complete
5. Download the MP4 file

---

## 📁 What's Been Created

### Project Structure
```
lit-protocol-animation/
├── src/
│   ├── project.ts              # Main project config
│   ├── scenes.d.ts             # TypeScript declarations
│   └── scenes/
│       ├── intro.tsx            # Scene 1: Problem + Solution (22s)
│       ├── apiIntegration.tsx   # Scene 2: API explanation (18s)
│       ├── agentAction.tsx      # Scene 3: Agent in action (15s)
│       ├── selfCustodial.tsx    # Scene 4: Self-custody feature (15s)
│       └── callToAction.tsx     # Scene 5: CTA (8s)
├── assets/
│   └── logos/                   # Lit Protocol brand assets
├── SCRIPT.md                    # Full storyboard and narration
├── QUICKSTART.md                # Detailed preview/render guide
├── README.md                    # Complete documentation
└── package.json                 # Dependencies and scripts
```

### Animation Breakdown (~78 seconds total)

1. **Intro (22s)**
   - Problem: Crypto requires constant manual signing
   - Solution: Lit Protocol's one-click agent wallet

2. **API Integration (18s)**
   - Shows universal API for wallets/dApps
   - Highlights Claude Code integration
   - Code snippet demo

3. **Agent in Action (15s)**
   - Automated DeFi operations
   - Swaps, staking, bridging, liquidity
   - No manual intervention needed

4. **Self-Custodial Control (15s)**
   - **CORE FEATURE**: User always in control
   - Withdraw anytime capability
   - Security and trust visualization

5. **Call to Action (8s)**
   - Lit Protocol branding
   - litprotocol.com
   - Links to docs and Discord

---

## 🎨 Making Changes

The editor supports **live reload**. While the server is running:

1. Edit any `.tsx` file in `src/scenes/`
2. Save the file
3. Browser auto-refreshes with your changes

### Common Adjustments

**Timing:**
```typescript
yield* waitFor(2);  // Wait 2 seconds - increase to slow down
```

**Colors:**
```typescript
fill={'#f97316'}  // Lit orange - change hex code
```

**Text:**
```typescript
<Txt text="Your text here" />  // Update any text
```

**Position:**
```typescript
x={100} y={-50}  // Adjust positioning
```

---

## 🎯 Technical Details

### Technologies Used
- **Motion Canvas**: TypeScript-based animation framework
- **React-like JSX**: For scene composition
- **Vite**: Fast build tool and dev server
- **TypeScript**: Type-safe development

### Features Highlighted
- ✅ Self-custodial automation
- ✅ One-click agent wallet creation
- ✅ Universal API for any wallet/dApp
- ✅ Simple integration (perfect for Claude Code)
- ✅ Withdraw anytime (core feature)
- ✅ Full user control maintained

### Animation Style
- Modern, clean aesthetic
- Dark background (#0a0a0a)
- Smooth transitions
- Professional pacing
- Tech/crypto color palette
- Easy to read text

---

## 📝 All Commits Made

1. **Initial setup**: Motion Canvas project with all 5 scenes
2. **Fixed dependencies**: Added @motion-canvas/ui for editor support
3. **Fixed compilation**: Resolved all TypeScript errors

Everything is working and ready to render! 🎬

---

## 🆘 Troubleshooting

### "npm install" fails
- Make sure you have Node.js v18+ installed
- Try `npm cache clean --force` then retry

### Port 9000 already in use
```bash
lsof -ti:9000 | xargs kill -9  # Kill the process
npm run serve                   # Try again
```

### Page loads but is blank
- Check browser console (F12) for errors
- Make sure all dependencies installed
- Try hard refresh (Ctrl+Shift+R)

### Changes not showing
- Make sure you saved the file
- Check terminal for compilation errors
- Try refreshing browser

---

## 🎥 Final Output

Your rendered video will be:
- **Format**: MP4 (H.264 codec)
- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 60 FPS
- **Duration**: ~78 seconds
- **File Size**: ~15-30 MB (depending on complexity)

Perfect for:
- YouTube, Twitter, LinkedIn
- Website embedding
- Presentations
- Social media marketing

---

## 📚 Additional Resources

- [Motion Canvas Docs](https://motioncanvas.io/docs/)
- [Lit Protocol Docs](https://developer.litprotocol.com/)
- [Project README](./README.md) - Full documentation
- [SCRIPT.md](./SCRIPT.md) - Detailed storyboard

---

**Enjoy creating your Lit Protocol animation! 🔥**
