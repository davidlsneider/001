import {makeScene2D, Rect, Txt, Circle, Line, Layout} from '@motion-canvas/2d';
import {all, createRef, waitFor, sequence, chain, loop} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Scene 5: Self-Custodial Control

  const headline = createRef<Txt>();
  const userIcon = createRef<Circle>();
  const agentIcon = createRef<Circle>();
  const assetsBox = createRef<Rect>();
  const controlLine = createRef<Line>();
  const withdrawArrow = createRef<Line>();
  const securityShield = createRef<Txt>();
  const subtext1 = createRef<Txt>();
  const subtext2 = createRef<Txt>();
  const keyFeature = createRef<Rect>();

  view.add(
    <>
      {/* Headline */}
      <Txt
        ref={headline}
        y={-320}
        fontSize={48}
        fill={'#e5e7eb'}
        fontWeight={700}
        opacity={0}
      >
        Always Self-Custodial
      </Txt>

      {/* User Icon */}
      <Circle
        ref={userIcon}
        x={-350}
        y={0}
        size={120}
        fill={'#3b82f6'}
        opacity={0}
      >
        <Txt text="👤" fontSize={60} />
      </Circle>

      {/* Agent Icon */}
      <Circle
        ref={agentIcon}
        x={0}
        y={0}
        size={100}
        fill={'#10b981'}
        opacity={0}
      >
        <Txt text="🤖" fontSize={50} />
      </Circle>

      {/* Assets Box */}
      <Rect
        ref={assetsBox}
        x={350}
        y={0}
        width={200}
        height={160}
        fill={'#1e293b'}
        stroke={'#f59e0b'}
        lineWidth={3}
        radius={12}
        opacity={0}
      >
        <Txt
          text="Your Assets"
          y={-50}
          fontSize={24}
          fill={'#f59e0b'}
          fontWeight={700}
        />
        <Txt
          text="💰"
          fontSize={50}
        />
      </Rect>

      {/* Control line from user */}
      <Line
        ref={controlLine}
        points={[
          [-290, 0],
          [250, 0],
        ]}
        stroke={'#3b82f6'}
        lineWidth={3}
        opacity={0}
        lineDash={[8, 8]}
      />

      {/* Withdrawal arrow */}
      <Line
        ref={withdrawArrow}
        points={[
          [300, -80],
          [-200, -80],
        ]}
        stroke={'#10b981'}
        lineWidth={6}
        opacity={0}
        endArrow
        arrowSize={20}
      />

      {/* Security shield */}
      <Txt
        ref={securityShield}
        x={0}
        y={-180}
        text="🛡️"
        fontSize={80}
        opacity={0}
      />

      {/* Subtexts */}
      <Txt
        ref={subtext1}
        y={180}
        fontSize={36}
        fill={'#10b981'}
        fontWeight={700}
        opacity={0}
      >
        Withdraw Anytime
      </Txt>
      <Txt
        ref={subtext2}
        y={240}
        fontSize={28}
        fill={'#9ca3af'}
        opacity={0}
      >
        You maintain full control
      </Txt>

      {/* Key feature callout */}
      <Rect
        ref={keyFeature}
        y={-260}
        width={400}
        height={60}
        fill={'#7c3aed'}
        radius={30}
        opacity={0}
      >
        <Txt
          text="🔑 CORE FEATURE"
          fontSize={24}
          fill={'#ffffff'}
          fontWeight={700}
        />
      </Rect>
    </>
  );

  // Animate scene
  yield* headline().opacity(1, 0.6);
  yield* waitFor(0.3);

  // Show key feature badge
  yield* all(
    keyFeature().opacity(1, 0.5),
    keyFeature().scale(1.1, 0.3).to(1, 0.2)
  );

  yield* waitFor(0.3);

  // Show components
  yield* sequence(
    0.2,
    userIcon().opacity(1, 0.5),
    agentIcon().opacity(1, 0.5),
    assetsBox().opacity(1, 0.5),
  );

  yield* waitFor(0.3);

  // Show control line
  yield* controlLine().opacity(1, 0.6);

  yield* waitFor(0.4);

  // Show security shield
  yield* all(
    securityShield().opacity(1, 0.5),
    securityShield().scale(1.2, 0.3).to(1, 0.3)
  );

  // Pulse shield
  yield* loop(
    2,
    () => chain(
      securityShield().scale(1.1, 0.5),
      securityShield().scale(1, 0.5)
    )
  );

  yield* waitFor(0.3);

  // Show withdrawal capability
  yield* all(
    withdrawArrow().opacity(1, 0.8),
    withdrawArrow().lineWidth(8, 0.3).to(6, 0.3)
  );

  // Pulse user icon to show active control
  yield* all(
    userIcon().scale(1.2, 0.4).to(1, 0.4),
    assetsBox().scale(0.95, 0.4).to(1, 0.4)
  );

  yield* waitFor(0.3);

  // Show subtexts
  yield* sequence(
    0.2,
    subtext1().opacity(1, 0.6),
    subtext2().opacity(1, 0.6),
  );

  yield* waitFor(2.5);

  // Fade out for final scene
  yield* all(
    headline().opacity(0, 0.6),
    userIcon().opacity(0, 0.6),
    agentIcon().opacity(0, 0.6),
    assetsBox().opacity(0, 0.6),
    controlLine().opacity(0, 0.6),
    withdrawArrow().opacity(0, 0.6),
    securityShield().opacity(0, 0.6),
    subtext1().opacity(0, 0.6),
    subtext2().opacity(0, 0.6),
    keyFeature().opacity(0, 0.6),
  );
});
