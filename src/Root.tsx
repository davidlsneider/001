import { Composition } from 'remotion';
import { SwarmVaultVideo } from './Video';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="SwarmVaultPromo"
        component={SwarmVaultVideo}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
