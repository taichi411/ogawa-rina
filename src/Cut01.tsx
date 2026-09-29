import {
  AbsoluteFill,
  Audio,
  Sequence,
  Video,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

const Subtitle: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 6], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 170,
        paddingLeft: 60,
        paddingRight: 60,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          opacity,
          color: "white",
          fontSize: 52,
          fontWeight: 700,
          lineHeight: 1.45,
          textAlign: "center",
          textShadow:
            "0 3px 12px rgba(0,0,0,0.9), 0 1px 3px rgba(0,0,0,1)",
          fontFamily:
            '"Hiragino Sans", "Yu Gothic", "Meiryo", sans-serif',
        }}
      >
        {children}
      </div>
    </AbsoluteFill>
  );
};

export const Cut01: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Video
        src={staticFile("video/cut01.mp4")}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />

      <Audio src={staticFile("audio/rina-intro-01.wav")} />

      {/* 0.0s - 2.5s */}
      <Sequence from={0} durationInFrames={75}>
        <Subtitle>はじめまして、小川莉奈です。</Subtitle>
      </Sequence>

      {/* 2.5s - 5.4s */}
      <Sequence from={75} durationInFrames={87}>
        <Subtitle>大阪で普通に会社員してます。</Subtitle>
      </Sequence>
    </AbsoluteFill>
  );
};
