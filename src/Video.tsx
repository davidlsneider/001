import { AbsoluteFill, interpolate, Sequence, useCurrentFrame, useVideoConfig } from 'remotion';

export const SwarmVaultVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      <Sequence from={0} durationInFrames={90}>
        <TitleScene />
      </Sequence>
      <Sequence from={90} durationInFrames={90}>
        <WhatIsItScene />
      </Sequence>
      <Sequence from={180} durationInFrames={90}>
        <FeaturesScene />
      </Sequence>
      <Sequence from={270} durationInFrames={90}>
        <HowItWorksScene />
      </Sequence>
      <Sequence from={360} durationInFrames={90}>
        <CallToActionScene />
      </Sequence>
    </AbsoluteFill>
  );
};

const TitleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const titleScale = interpolate(frame, [0, 20], [0.8, 1], {
    extrapolateRight: 'clamp',
  });

  const subtitleOpacity = interpolate(frame, [15, 35], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          opacity: titleOpacity,
          transform: `scale(${titleScale})`,
          textAlign: 'center',
        }}
      >
        <h1
          style={{
            fontSize: 120,
            fontWeight: 'bold',
            color: 'white',
            margin: 0,
            textShadow: '0 4px 20px rgba(0,0,0,0.3)',
          }}
        >
          Swarm Vault
        </h1>
        <div
          style={{
            fontSize: 48,
            color: 'rgba(255, 255, 255, 0.9)',
            marginTop: 20,
            opacity: subtitleOpacity,
          }}
        >
          Coordinated Blockchain Transactions
        </div>
      </div>
    </AbsoluteFill>
  );
};

const WhatIsItScene: React.FC = () => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const slideIn = interpolate(frame, [0, 20], [-100, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
        padding: 80,
        justifyContent: 'center',
      }}
    >
      <div style={{ opacity, transform: `translateX(${slideIn}px)` }}>
        <h2
          style={{
            fontSize: 80,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: 40,
          }}
        >
          What is Swarm Vault?
        </h2>
        <p
          style={{
            fontSize: 42,
            color: 'rgba(255, 255, 255, 0.95)',
            lineHeight: 1.6,
            maxWidth: 1600,
          }}
        >
          A blockchain platform that enables managers to execute transactions
          on behalf of multiple users on the Base blockchain. Users join
          "swarms" managed by trusted managers, each receiving a ZeroDev smart
          wallet.
        </p>
      </div>
    </AbsoluteFill>
  );
};

const FeaturesScene: React.FC = () => {
  const frame = useCurrentFrame();

  const features = [
    { icon: '👥', title: 'Swarm Management', delay: 0 },
    { icon: '💼', title: 'Smart Wallets', delay: 10 },
    { icon: '🔄', title: 'Token Swaps', delay: 20 },
    { icon: '📊', title: 'Real-time Balances', delay: 30 },
    { icon: '🔐', title: 'Lit Protocol PKP', delay: 40 },
    { icon: '⚡', title: 'Manager SDK', delay: 50 },
  ];

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #059669 0%, #10b981 100%)',
        padding: 80,
      }}
    >
      <h2
        style={{
          fontSize: 80,
          fontWeight: 'bold',
          color: 'white',
          marginBottom: 60,
          textAlign: 'center',
        }}
      >
        Key Features
      </h2>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: 40,
          maxWidth: 1600,
          margin: '0 auto',
        }}
      >
        {features.map((feature, index) => {
          const opacity = interpolate(
            frame,
            [feature.delay, feature.delay + 15],
            [0, 1],
            { extrapolateRight: 'clamp' }
          );

          const scale = interpolate(
            frame,
            [feature.delay, feature.delay + 15],
            [0.5, 1],
            { extrapolateRight: 'clamp' }
          );

          return (
            <div
              key={index}
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.15)',
                borderRadius: 20,
                padding: 40,
                textAlign: 'center',
                opacity,
                transform: `scale(${scale})`,
                backdropFilter: 'blur(10px)',
              }}
            >
              <div style={{ fontSize: 80, marginBottom: 20 }}>
                {feature.icon}
              </div>
              <div
                style={{
                  fontSize: 32,
                  color: 'white',
                  fontWeight: '600',
                }}
              >
                {feature.title}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const HowItWorksScene: React.FC = () => {
  const frame = useCurrentFrame();

  const steps = [
    '1. Manager creates a swarm',
    '2. Members join with smart wallets',
    '3. Manager defines transactions',
    '4. Lit Protocol signs for members',
    '5. Execute across all wallets',
  ];

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%)',
        padding: 80,
        justifyContent: 'center',
      }}
    >
      <h2
        style={{
          fontSize: 80,
          fontWeight: 'bold',
          color: 'white',
          marginBottom: 60,
          textAlign: 'center',
        }}
      >
        How It Works
      </h2>
      <div style={{ maxWidth: 1400, margin: '0 auto' }}>
        {steps.map((step, index) => {
          const opacity = interpolate(
            frame,
            [index * 12, index * 12 + 15],
            [0, 1],
            { extrapolateRight: 'clamp' }
          );

          const slideX = interpolate(
            frame,
            [index * 12, index * 12 + 15],
            [50, 0],
            { extrapolateRight: 'clamp' }
          );

          return (
            <div
              key={index}
              style={{
                fontSize: 48,
                color: 'white',
                marginBottom: 30,
                padding: 25,
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                borderRadius: 15,
                opacity,
                transform: `translateX(${slideX}px)`,
                backdropFilter: 'blur(10px)',
              }}
            >
              {step}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const CallToActionScene: React.FC = () => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const scale = interpolate(frame, [0, 20], [0.9, 1], {
    extrapolateRight: 'clamp',
  });

  const pulse = Math.sin(frame / 10) * 0.05 + 1;

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #dc2626 0%, #f97316 100%)',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          textAlign: 'center',
          opacity,
          transform: `scale(${scale})`,
        }}
      >
        <h2
          style={{
            fontSize: 90,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: 40,
          }}
        >
          Get Started Today
        </h2>
        <div
          style={{
            fontSize: 56,
            color: 'white',
            marginBottom: 60,
            opacity: 0.9,
          }}
        >
          swarmvaults.xyz
        </div>
        <div
          style={{
            fontSize: 36,
            color: 'rgba(255, 255, 255, 0.8)',
            transform: `scale(${pulse})`,
          }}
        >
          Coordinated blockchain transactions made simple
        </div>
      </div>
    </AbsoluteFill>
  );
};
