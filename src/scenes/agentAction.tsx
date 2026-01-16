import {makeScene2D, Rect, Txt, Circle, Layout, Icon} from '@motion-canvas/2d';
import {all, createRef, waitFor, sequence, chain} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Scene 4: Agent in Action

  const headline = createRef<Txt>();
  const agentIcon = createRef<Circle>();
  const txBoxes = Array.from({length: 4}, () => createRef<Rect>());
  const checkmarks = Array.from({length: 4}, () => createRef<Txt>());
  const subtext = createRef<Txt>();

  const transactions = [
    { label: 'Swap ETH → USDC', color: '#8b5cf6' },
    { label: 'Stake on Lido', color: '#3b82f6' },
    { label: 'Bridge to L2', color: '#10b981' },
    { label: 'Provide Liquidity', color: '#f59e0b' },
  ];

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
        Automated Execution
      </Txt>

      {/* Agent Icon in center */}
      <Circle
        ref={agentIcon}
        x={0}
        y={-80}
        size={140}
        fill={'#10b981'}
        opacity={0}
      >
        <Txt text="🤖" fontSize={80} />
      </Circle>

      {/* Transaction boxes arranged around agent */}
      {txBoxes.map((ref, i) => {
        const angle = (i * Math.PI) / 2 - Math.PI / 4; // Positions at 45, 135, 225, 315 degrees
        const radius = 320;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius - 80;

        return (
          <Layout key={i}>
            <Rect
              ref={ref}
              x={x}
              y={y}
              width={240}
              height={80}
              fill={'#1e293b'}
              stroke={transactions[i].color}
              lineWidth={3}
              radius={8}
              opacity={0}
            >
              <Txt
                text={transactions[i].label}
                fontSize={20}
                fill={'#e5e7eb'}
                fontWeight={600}
              />
            </Rect>
            <Txt
              ref={checkmarks[i]}
              x={x + 140}
              y={y}
              text="✓"
              fontSize={40}
              fill={'#10b981'}
              opacity={0}
            />
          </Layout>
        );
      })}

      {/* Subtext */}
      <Txt
        ref={subtext}
        y={280}
        fontSize={32}
        fill={'#9ca3af'}
        opacity={0}
      >
        Any crypto transaction, fully automated
      </Txt>
    </>
  );

  // Animate scene
  yield* headline().opacity(1, 0.6);
  yield* waitFor(0.3);

  // Show agent
  yield* all(
    agentIcon().opacity(1, 0.6),
    agentIcon().scale(1.2, 0.4).to(1, 0.3)
  );

  yield* waitFor(0.3);

  // Show transaction boxes one by one
  for (let i = 0; i < txBoxes.length; i++) {
    yield* sequence(
      0.1,
      txBoxes[i]().opacity(1, 0.4),
      chain(
        txBoxes[i]().scale(1.1, 0.2),
        txBoxes[i]().scale(1, 0.2)
      )
    );

    // Pulse the agent for each transaction
    yield* agentIcon().scale(1.15, 0.15).to(1, 0.15);

    // Show checkmark
    yield* all(
      checkmarks[i]().opacity(1, 0.3),
      checkmarks[i]().scale(1.3, 0.2).to(1, 0.2)
    );

    yield* waitFor(0.3);
  }

  // Show subtext
  yield* subtext().opacity(1, 0.8);

  yield* waitFor(2);

  // Fade out for next scene
  yield* all(
    headline().opacity(0, 0.6),
    agentIcon().opacity(0, 0.6),
    subtext().opacity(0, 0.6),
    ...txBoxes.map(box => box().opacity(0, 0.6)),
    ...checkmarks.map(check => check().opacity(0, 0.6)),
  );
});
