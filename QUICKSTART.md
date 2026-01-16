# Quick Start Guide - Preview & Render

## Step 1: Preview the Animation (Development Mode)

### Start the preview server:
```bash
npm run serve
```

### What happens:
- A local web server starts (usually at `http://localhost:9000`)
- Your browser will open automatically showing the **Motion Canvas Editor**
- You'll see a split-screen interface:
  - **Left side**: The animation canvas (where your video plays)
  - **Right side**: Timeline and controls
  - **Bottom**: Playback controls (play, pause, scrub)

### Using the Editor:

1. **Play the animation**: Click the play button ▶️ at the bottom
2. **Scrub through time**: Drag the playhead on the timeline
3. **Inspect scenes**: Each scene appears as a segment on the timeline
4. **Real-time editing**: Any changes you make to `.tsx` files will update live

### Tips:
- The animation will loop automatically
- Use spacebar to play/pause
- Click and drag the timeline to jump to specific moments
- Check the browser console (F12) for any errors

---

## Step 2: Render the Video (Export)

### Option A: Render from the Editor (Recommended for first time)

1. Start the preview server: `npm run serve`
2. In the Motion Canvas editor, look for the **Render** button (top right or in menu)
3. Click **Render** → Choose your settings:
   - **Format**: MP4 (H.264)
   - **Resolution**: 1920x1080 (Full HD)
   - **Frame Rate**: 60 FPS
   - **Range**: Full animation or specific scenes
4. Click **Start Rendering**
5. Wait for it to finish (progress bar will show)
6. Download the video when complete

### Option B: Render from Command Line

```bash
npm run build
```

**What happens:**
- Motion Canvas renders the entire project
- Creates an `output/` directory
- Saves the video as `project.mp4` (or similar name)
- Shows progress in terminal

**Time estimate:**
- For a 90-second animation at 60 FPS = ~5,400 frames
- Rendering time varies (could be 2-10 minutes depending on your machine)

---

## Step 3: Find Your Rendered Video

After rendering completes, check:
```bash
ls -la output/
```

Your video will be named something like:
- `project.mp4`
- `lit-protocol-animation.mp4`

You can play it with any video player!

---

## Troubleshooting

### "Port already in use" error
If port 9000 is busy:
```bash
# Kill any existing process
lsof -ti:9000 | xargs kill -9
# Then try again
npm run serve
```

### Preview is blank/black screen
- Check browser console (F12) for errors
- Verify all scene files compiled without errors
- Try refreshing the browser

### Rendering fails
- Make sure all dependencies are installed: `npm install`
- Check that there are no TypeScript errors: `npx tsc --noEmit`
- Look at terminal output for specific error messages

### Animation is too fast/slow
Edit the `waitFor()` values in scene files:
- `yield* waitFor(2);` = pause for 2 seconds
- Increase values to slow down, decrease to speed up

---

## Quick Commands Reference

| Command | What it does |
|---------|-------------|
| `npm install` | Install all dependencies |
| `npm run serve` | Start preview server (development) |
| `npm run build` | Render final video |
| `ls output/` | List rendered videos |

---

## What to Expect

### First Preview:
When you run `npm run serve`, you should see your animation with:
- Dark background (#0a0a0a)
- Lit Protocol logo appearing
- Text animations
- Scene transitions
- All 5 scenes playing in sequence (~78 seconds total)

### First Render:
The output video will be:
- Full HD (1920x1080)
- Smooth 60 FPS
- MP4 format (compatible with everything)
- Ready to upload to YouTube, Twitter, etc.

---

## Next Steps After Preview

1. **Watch it through** - Does the pacing feel right?
2. **Check timing** - Any scenes too fast/slow?
3. **Verify text** - All messages clear and readable?
4. **Test on mobile** - Does it look good on smaller screens?
5. **Adjust as needed** - Edit scene files and preview again
6. **Final render** - When happy, render the final video

---

Need help with edits or adjustments? Just ask!
