import {
  AbsoluteFill,
  Audio,
  Video,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const Cut01: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(
    frame,
    [0, Math.round(0.25 * fps)],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

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
          はじめまして、小川莉奈です。
          <br />
          大阪で普通に会社員してます。
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
