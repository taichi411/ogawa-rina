import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { Layer, TypeLayer, Monitor, Gleams, progress, clamp } from "./shared";

export const CallToAction: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <>
      <Layer
        name="cta-woman"
        style={{
          translate: `${interpolate(f, [0, 14], [-37, 0], clamp)}px 0px`,
          rotate: `${Math.sin(f * 0.095) * 0.35}deg`,
          transformOrigin: "55px 113px",
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          translate: `0px ${interpolate(f, [0, 30], [-38, 0], clamp)}px`,
        }}
      >
        <Monitor x={205} y={101} w={154} h={124} />
      </div>
      <div style={{ opacity: progress(f, 6, 18) }}>
        <Gleams variant="cta" />
      </div>
      <TypeLayer
        name="cta-heading"
        start={3}
        duration={34}
        count={29}
        bounce={4}
      />
      <TypeLayer
        name="cta-subheading"
        start={40}
        duration={12}
        count={11}
        bounce={2}
      />
      <Layer name="cta-url" style={{ opacity: progress(f, 8, 17) }} />
      <Layer
        name="browser-shell"
        style={{
          opacity: progress(f, 25, 30),
          scale: `1 ${progress(f, 25, 38)}`,
          transformOrigin: "40px 28px",
        }}
      />
      <TypeLayer
        name="browser-row-0"
        start={47}
        duration={16}
        count={12}
        bounce={0}
      />
      <TypeLayer
        name="browser-row-1"
        start={79}
        duration={16}
        count={12}
        bounce={0}
      />
    </>
  );
};
