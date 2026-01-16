import {makeScene2D, Txt, Img, Rect, Layout} from '@motion-canvas/2d';
import {all, createRef, waitFor, sequence} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Scene 6: Call to Action

  const logo = createRef<Img>();
  const headline = createRef<Txt>();
  const websiteUrl = createRef<Txt>();
  const docsLink = createRef<Rect>();
  const discordLink = createRef<Rect>();
  const features = Array.from({length: 3}, () => createRef<Txt>());

  const keyFeatures = [
    '✓ Self-custodial automation',
    '✓ One-click agent creation',
    '✓ Simple API for any wallet/dApp',
  ];

  view.add(
    <>
      {/* Lit Protocol Logo */}
      <Img
        ref={logo}
        src="/assets/logos/lit-primary-white.svg"
        width={300}
        y={-200}
        opacity={0}
      />

      {/* Main CTA headline */}
      <Txt
        ref={headline}
        y={-50}
        fontSize={52}
        fill={'#f97316'}
        fontWeight={700}
        opacity={0}
      >
        Build Self-Custodial Automation
      </Txt>

      {/* Key features recap */}
      {features.map((ref, i) => (
        <Txt
          key={i}
          ref={ref}
          y={40 + i * 50}
          fontSize={28}
          fill={'#9ca3af'}
          opacity={0}
        >
          {keyFeatures[i]}
        </Txt>
      ))}

      {/* Website URL */}
      <Txt
        ref={websiteUrl}
        y={220}
        fontSize={40}
        fill={'#3b82f6'}
        fontWeight={700}
        opacity={0}
      >
        litprotocol.com
      </Txt>

      {/* Action buttons */}
      <Rect
        ref={docsLink}
        x={-180}
        y={300}
        width={200}
        height={60}
        fill={'#10b981'}
        radius={8}
        opacity={0}
      >
        <Txt
          text="📚 Docs"
          fontSize={24}
          fill={'#ffffff'}
          fontWeight={700}
        />
      </Rect>

      <Rect
        ref={discordLink}
        x={180}
        y={300}
        width={200}
        height={60}
        fill={'#5865f2'}
        radius={8}
        opacity={0}
      >
        <Txt
          text="💬 Discord"
          fontSize={24}
          fill={'#ffffff'}
          fontWeight={700}
        />
      </Rect>
    </>
  );

  // Animate final scene
  yield* logo().opacity(1, 1);
  yield* waitFor(0.4);

  yield* headline().opacity(1, 0.8);
  yield* waitFor(0.3);

  // Show features one by one
  yield* sequence(
    0.2,
    ...features.map(feature => feature().opacity(1, 0.5))
  );

  yield* waitFor(0.5);

  // Show website
  yield* all(
    websiteUrl().opacity(1, 0.6),
    websiteUrl().scale(1.1, 0.3).to(1, 0.3)
  );

  yield* waitFor(0.4);

  // Show action buttons
  yield* sequence(
    0.2,
    docsLink().opacity(1, 0.5),
    discordLink().opacity(1, 0.5),
  );

  // Hold final frame
  yield* waitFor(3);
});
