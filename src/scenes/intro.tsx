import {makeScene2D, Rect, Txt, Circle, Layout, Img} from '@motion-canvas/2d';
import {all, createRef, waitFor, sequence, chain, loop} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Scene 1: Problem/Hook + Scene 2: Solution

  // Problem visualization
  const problemContainer = createRef<Layout>();
  const signPrompts = Array.from({length: 5}, () => createRef<Rect>());
  const userIcon = createRef<Circle>();

  // Solution visualization
  const litLogo = createRef<Img>();
  const solutionText = createRef<Txt>();
  const clickAnimation = createRef<Circle>();

  view.add(
    <>
      {/* Problem Scene */}
      <Layout ref={problemContainer} opacity={1}>
        {/* User icon - frustrated */}
        <Circle
          ref={userIcon}
          x={0}
          y={0}
          size={120}
          fill={'#4a5568'}
          opacity={0}
        >
          <Txt
            text="😰"
            fontSize={60}
          />
        </Circle>

        {/* Multiple "Sign Transaction" prompts */}
        {signPrompts.map((ref, i) => (
          <Rect
            key={i}
            ref={ref}
            x={(i - 2) * 200}
            y={200}
            width={180}
            height={100}
            fill={'#ef4444'}
            radius={8}
            opacity={0}
          >
            <Txt
              text="SIGN\nTRANSACTION"
              fontSize={16}
              fill={'#ffffff'}
              fontWeight={700}
              textAlign="center"
            />
          </Rect>
        ))}

        {/* Problem text */}
        <Txt
          x={0}
          y={-250}
          fontSize={48}
          fill={'#e5e7eb'}
          fontWeight={700}
          opacity={0}
          ref={createRef<Txt>()}
        >
          Managing crypto requires
        </Txt>
        <Txt
          x={0}
          y={-180}
          fontSize={48}
          fill={'#e5e7eb'}
          fontWeight={700}
          opacity={0}
          ref={createRef<Txt>()}
        >
          constant attention...
        </Txt>
      </Layout>
    </>
  );

  // Animate Problem Scene
  yield* all(
    userIcon().opacity(1, 0.5),
    sequence(
      0.1,
      ...signPrompts.map(prompt => prompt().opacity(1, 0.3))
    ),
  );

  // Shake/flash the prompts to show urgency
  yield* loop(
    3,
    () => all(
      ...signPrompts.map(prompt =>
        chain(
          prompt().scale(1.1, 0.15),
          prompt().scale(1, 0.15)
        )
      )
    )
  );

  yield* waitFor(0.5);

  // Fade out problem scene
  yield* all(
    problemContainer().opacity(0, 0.8),
  );

  // Clear problem scene
  problemContainer().remove();

  // Add solution scene
  view.add(
    <>
      {/* Lit Protocol Logo */}
      <Img
        ref={litLogo}
        src="/assets/logos/lit-primary-white.svg"
        width={200}
        y={-150}
        opacity={0}
      />

      {/* Solution headline */}
      <Txt
        ref={solutionText}
        y={50}
        fontSize={52}
        fill={'#f97316'}
        fontWeight={700}
        opacity={0}
      >
        Self-Custodial Automation
      </Txt>

      {/* One-click visual */}
      <Circle
        ref={clickAnimation}
        x={0}
        y={180}
        size={80}
        fill={'#10b981'}
        opacity={0}
      >
        <Txt
          text="1 CLICK"
          fontSize={18}
          fill={'#ffffff'}
          fontWeight={700}
        />
      </Circle>
    </>
  );

  // Animate Solution Scene
  yield* sequence(
    0.3,
    litLogo().opacity(1, 1),
    solutionText().opacity(1, 0.8),
    all(
      clickAnimation().opacity(1, 0.5),
      clickAnimation().scale(1.2, 0.3).to(1, 0.3)
    )
  );

  yield* waitFor(2);

  // Fade out for next scene
  yield* all(
    litLogo().opacity(0, 0.6),
    solutionText().opacity(0, 0.6),
    clickAnimation().opacity(0, 0.6),
  );
});
