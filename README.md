# Lit Protocol Animation

An animated explainer video for Lit Protocol's self-custodial automation feature, built with Motion Canvas (TypeScript).

## Overview

This 60-90 second animation showcases:
- **Self-custodial automation** - Users maintain full control of their assets
- **One-click agent wallet creation** - Simple setup process
- **Universal API** - Any wallet/dApp can integrate automations
- **Withdraw anytime** - Core feature emphasizing user control
- **Developer-friendly** - Perfect for building with Claude Code

## Project Structure

```
lit-protocol-animation/
├── src/
│   ├── project.ts              # Main project configuration
│   └── scenes/
│       ├── intro.tsx            # Problem/hook + solution intro
│       ├── apiIntegration.tsx   # API integration explanation
│       ├── agentAction.tsx      # Agent performing transactions
│       ├── selfCustodial.tsx    # Self-custody emphasis
│       └── callToAction.tsx     # Final CTA with branding
├── assets/
│   └── logos/                   # Lit Protocol brand assets
├── SCRIPT.md                    # Detailed storyboard and script
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Scenes Breakdown

### 1. Intro (22 seconds)
- **Problem**: Managing crypto requires constant attention
- **Solution**: Lit Protocol's one-click self-custodial automation

### 2. API Integration (18 seconds)
- Shows how wallets/dApps and agents interact via API
- Emphasizes simplicity and developer experience
- Highlights Claude Code integration

### 3. Agent in Action (15 seconds)
- Demonstrates automated transaction execution
- Shows various DeFi operations happening seamlessly
- No manual intervention required

### 4. Self-Custodial Control (15 seconds)
- **KEY FEATURE**: User maintains full control
- Withdrawal capability emphasized
- Security and trust visualized

### 5. Call to Action (8 seconds)
- Lit Protocol branding
- Links to docs and community
- Clear next steps

## Getting Started

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start the development server with live preview
npm run serve
```

This will open the Motion Canvas editor in your browser where you can:
- Preview the animation in real-time
- Scrub through the timeline
- Edit scenes and see changes instantly
- Adjust timing and transitions

### Building the Video

```bash
# Render the animation to video
npm run build
```

The rendered video will be saved in the `output/` directory.

## Customization

### Adjusting Timing

Edit the `waitFor()` and animation duration values in each scene file:

```typescript
yield* waitFor(2);  // Hold for 2 seconds
yield* someAnimation(1, 0.5);  // Animate to value 1 over 0.5 seconds
```

### Changing Colors

The animation uses these primary colors:
- Background: `#0a0a0a` (dark)
- Lit Orange: `#f97316`
- Agent Green: `#10b981`
- API Blue: `#3b82f6`
- Code Purple: `#a78bfa`

Edit color values in the scene files to match your preferences.

### Modifying Text

All text content is inline in the scene files. Search for `<Txt>` components and update the `text` prop.

### Adding Your Own Assets

Place custom images/logos in the `assets/` directory and reference them:

```typescript
<Img
  src="/assets/your-image.svg"
  width={200}
/>
```

## Technical Details

### Motion Canvas Features Used
- 2D scene composition
- Tweening and easing
- Signals for reactive animations
- Sequencing and chaining
- Layout management

### Scene Architecture
Each scene is self-contained with:
- Setup phase (creating elements)
- Animation phase (yielding animations)
- Cleanup phase (fading out for next scene)

## Script and Storyboard

See [SCRIPT.md](SCRIPT.md) for the detailed narrative flow, visual descriptions, and timing breakdown.

## Brand Guidelines

This animation uses official Lit Protocol brand assets. The logomarks are included in `assets/logos/`.

For the full brand kit, visit: https://github.com/LIT-Protocol/Brand-Kit

## Export Settings

Default export settings:
- Resolution: 1920x1080 (Full HD)
- Frame rate: 60 FPS
- Format: MP4 (H.264)

Adjust in `src/project.ts` if needed.

## Contributing

To add new scenes:
1. Create a new scene file in `src/scenes/`
2. Import and add it to the scenes array in `src/project.ts`
3. Follow the existing scene structure

## Resources

- [Motion Canvas Documentation](https://motioncanvas.io/docs/)
- [Lit Protocol Documentation](https://developer.litprotocol.com/)
- [Lit Protocol GitHub](https://github.com/LIT-Protocol)

## License

This project uses Lit Protocol's brand assets under their brand guidelines.

## Questions?

Join the Lit Protocol community:
- [Discord](https://discord.gg/4QDrg5sDjr)
- [Twitter](https://twitter.com/LitProtocol)
- [Developer Docs](https://developer.litprotocol.com/)
