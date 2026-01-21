# Swarm Vault Promotional Video

A professional promotional video for [SwarmVaults.xyz](https://swarmvaults.xyz) created with Remotion.

## About Swarm Vault

Swarm Vault is a blockchain platform powered by Lit Protocol that enables managers to execute coordinated transactions on behalf of multiple users on the Base blockchain. Users join "swarms" managed by trusted managers, with each member receiving a ZeroDev smart wallet.

## Video Overview

This 15-second promotional video includes 5 animated scenes:

1. **Title Scene** (0-3s): Eye-catching title with gradient background
2. **What Is It Scene** (3-6s): Explanation of Swarm Vault's core purpose
3. **Features Scene** (6-9s): Showcase of 6 key features with animated icons
4. **How It Works Scene** (9-12s): Step-by-step workflow visualization
5. **Call to Action Scene** (12-15s): Final call-to-action with website URL

## Features Highlighted

- 👥 Swarm Management
- 💼 Smart Wallets (ZeroDev)
- 🔄 Token Swaps (0x DEX)
- 📊 Real-time Balances
- 🔐 Lit Protocol PKP
- ⚡ Manager SDK

## Technical Details

- **Duration**: 15 seconds (450 frames @ 30fps)
- **Resolution**: 1920x1080 (Full HD)
- **Framework**: Remotion 4.0
- **React**: 19.2
- **Animations**: Smooth interpolations with opacity, scale, and slide effects

## Prerequisites

- Node.js 18+
- npm or pnpm
- Chrome/Chromium (for rendering)

## Installation

```bash
npm install
```

## Usage

### Preview the video

```bash
npm run preview
```

This opens an interactive browser preview where you can scrub through frames.

### Render the video

```bash
npm run build
```

This renders the video to `out/swarmvault.mp4`.

### Custom render options

```bash
# Render at different resolution
npx remotion render SwarmVaultPromo out/swarmvault.mp4 --width=3840 --height=2160

# Render as GIF
npx remotion render SwarmVaultPromo out/swarmvault.gif

# Render specific frame range
npx remotion render SwarmVaultPromo out/swarmvault.mp4 --frames=0-90
```

## Project Structure

```
.
├── src/
│   ├── index.ts           # Entry point, registers root
│   ├── Root.tsx           # Remotion composition definition
│   └── Video.tsx          # Main video component with all scenes
├── remotion.config.ts     # Remotion configuration
├── tsconfig.json          # TypeScript configuration
└── package.json           # Dependencies and scripts
```

## Customization

### Modify duration

Edit `src/Root.tsx`:

```tsx
<Composition
  id="SwarmVaultPromo"
  component={SwarmVaultVideo}
  durationInFrames={450}  // Change this (30 fps = 1 second per 30 frames)
  fps={30}
  width={1920}
  height={1080}
/>
```

### Adjust scene timing

Edit sequence timings in `src/Video.tsx`:

```tsx
<Sequence from={0} durationInFrames={90}>    // Scene 1: 0-3s
<Sequence from={90} durationInFrames={90}>   // Scene 2: 3-6s
// etc...
```

### Change colors

Each scene uses gradient backgrounds. Modify the `background` styles in each scene component.

### Update content

Edit text, features, and steps directly in the scene components within `src/Video.tsx`.

## Deployment

### Render to video file

The rendered video can be:
- Uploaded to YouTube, Vimeo, or social media
- Embedded on the SwarmVaults.xyz website
- Used in presentations and marketing materials

### Deploy to Remotion Lambda

For cloud rendering:

```bash
npx remotion lambda render SwarmVaultPromo
```

See [Remotion Lambda docs](https://www.remotion.dev/docs/lambda) for setup.

## Technology Stack

Built with:
- [Remotion](https://remotion.dev) - Video creation in React
- [React](https://react.dev) - Component framework
- [TypeScript](https://www.typescriptlang.org) - Type safety

## Resources

- [Remotion Documentation](https://www.remotion.dev/docs)
- [Swarm Vault GitHub](https://github.com/LIT-Protocol/swarm-vault)
- [Swarm Vault Website](https://swarmvaults.xyz)

## License

ISC
