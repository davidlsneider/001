import {makeScene2D, Rect, Txt, Line, Circle, Layout, Code} from '@motion-canvas/2d';
import {all, createRef, waitFor, sequence, createSignal} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Scene 3: API Integration

  const dappBox = createRef<Rect>();
  const agentBox = createRef<Rect>();
  const apiLine1 = createRef<Line>();
  const apiLine2 = createRef<Line>();
  const codeSnippet = createRef<Code>();
  const headline = createRef<Txt>();
  const subtext1 = createRef<Txt>();
  const subtext2 = createRef<Txt>();
  const claudeCode = createRef<Txt>();

  // Data flow particles
  const particles = Array.from({length: 6}, () => createRef<Circle>());
  const particleProgress = createSignal(0);

  view.add(
    <>
      {/* Headline */}
      <Txt
        ref={headline}
        y={-320}
        fontSize={44}
        fill={'#e5e7eb'}
        fontWeight={700}
        opacity={0}
      >
        Universal API Integration
      </Txt>

      {/* DApp/Wallet Box (Left) */}
      <Rect
        ref={dappBox}
        x={-400}
        y={0}
        width={280}
        height={200}
        fill={'#1e293b'}
        stroke={'#3b82f6'}
        lineWidth={3}
        radius={12}
        opacity={0}
      >
        <Txt
          text="Your Wallet"
          y={-60}
          fontSize={28}
          fill={'#3b82f6'}
          fontWeight={700}
        />
        <Txt
          text="or DApp"
          y={-20}
          fontSize={24}
          fill={'#60a5fa'}
          fontWeight={500}
        />
        <Circle
          y={50}
          size={60}
          fill={'#3b82f6'}
        >
          <Txt text="🔑" fontSize={32} />
        </Circle>
      </Rect>

      {/* Agent Wallet Box (Right) */}
      <Rect
        ref={agentBox}
        x={400}
        y={0}
        width={280}
        height={200}
        fill={'#1e293b'}
        stroke={'#10b981'}
        lineWidth={3}
        radius={12}
        opacity={0}
      >
        <Txt
          text="Agent"
          y={-60}
          fontSize={28}
          fill={'#10b981'}
          fontWeight={700}
        />
        <Txt
          text="Wallet"
          y={-20}
          fontSize={24}
          fill={'#34d399'}
          fontWeight={500}
        />
        <Circle
          y={50}
          size={60}
          fill={'#10b981'}
        >
          <Txt text="🤖" fontSize={32} />
        </Circle>
      </Rect>

      {/* API Connection Lines */}
      <Line
        ref={apiLine1}
        points={[
          [-260, -40],
          [260, -40],
        ]}
        stroke={'#f97316'}
        lineWidth={4}
        opacity={0}
        lineDash={[10, 10]}
        endArrow
      />
      <Line
        ref={apiLine2}
        points={[
          [260, 40],
          [-260, 40],
        ]}
        stroke={'#f97316'}
        lineWidth={4}
        opacity={0}
        lineDash={[10, 10]}
        endArrow
      />

      {/* API particles flowing */}
      {particles.map((ref, i) => (
        <Circle
          key={`particle-${i}`}
          ref={ref}
          size={12}
          fill={'#fbbf24'}
          opacity={0}
          x={() => -260 + particleProgress() * 520}
          y={() => i % 2 === 0 ? -40 : 40}
        />
      ))}

      {/* Subtitle texts */}
      <Txt
        ref={subtext1}
        y={180}
        fontSize={28}
        fill={'#9ca3af'}
        opacity={0}
      >
        Install automations via simple API
      </Txt>
      <Txt
        ref={subtext2}
        y={230}
        fontSize={28}
        fill={'#9ca3af'}
        opacity={0}
      >
        Both interact through the same interface
      </Txt>

      {/* Claude Code mention */}
      <Txt
        ref={claudeCode}
        y={290}
        fontSize={24}
        fill={'#a78bfa'}
        opacity={0}
        fontWeight={600}
      >
        ⚡ Perfect for building with Claude Code
      </Txt>

      {/* Code snippet */}
      <Code
        ref={codeSnippet}
        y={-80}
        fontSize={18}
        opacity={0}
        code={`// Install automation
await litProtocol.createAgent({
  trigger: "priceAbove",
  action: "swap",
  params: { threshold: 100 }
});`}
      />
    </>
  );

  // Animate scene
  yield* headline().opacity(1, 0.6);
  yield* waitFor(0.3);

  yield* sequence(
    0.3,
    dappBox().opacity(1, 0.6),
    agentBox().opacity(1, 0.6),
  );

  yield* waitFor(0.4);

  // Show API connections
  yield* all(
    apiLine1().opacity(1, 0.6),
    apiLine2().opacity(1, 0.6),
  );

  yield* waitFor(0.3);

  // Animate particles flowing
  yield* all(
    ...particles.map((p, i) =>
      sequence(i * 0.1, p().opacity(1, 0.3))
    )
  );

  // Flow particles back and forth
  yield* particleProgress(1, 1.5);
  yield* particleProgress(0, 1.5);

  yield* waitFor(0.3);

  // Show code snippet
  yield* codeSnippet().opacity(1, 0.8);

  yield* waitFor(0.8);

  // Show subtitle texts
  yield* sequence(
    0.3,
    subtext1().opacity(1, 0.6),
    subtext2().opacity(1, 0.6),
    claudeCode().opacity(1, 0.6),
  );

  yield* waitFor(2.5);

  // Fade out for next scene
  yield* all(
    headline().opacity(0, 0.5),
    dappBox().opacity(0, 0.5),
    agentBox().opacity(0, 0.5),
    apiLine1().opacity(0, 0.5),
    apiLine2().opacity(0, 0.5),
    ...particles.map(p => p().opacity(0, 0.5)),
    codeSnippet().opacity(0, 0.5),
    subtext1().opacity(0, 0.5),
    subtext2().opacity(0, 0.5),
    claudeCode().opacity(0, 0.5),
  );
});
