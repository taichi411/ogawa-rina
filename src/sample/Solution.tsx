import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { Layer, TypeLayer, progress, clamp, CORAL, Gleams } from "./shared";

export const Solution: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <>
      <Layer
        name="city"
        style={{
          translate: `0px ${76 * (1 - progress(f, 20, 50))}px`,
          opacity: progress(f, 20, 31),
        }}
      />
      <Layer name="city-back" style={{ opacity: progress(f, 105, 139) }} />
      <div
        style={{
          position: "absolute",
          left: 99,
          top: 81,
          width: 289,
          height: 46,
          borderRadius: 28,
          background: CORAL,
          scale: `${progress(f, 3, 18)} 1`,
        }}
      />
      <TypeLayer
        name="solution-heading"
        start={0}
        duration={11}
        bounce={12}
        count={14}
      />
      <TypeLayer
        name="solution-title"
        start={5}
        duration={9}
        bounce={34}
        count={10}
      />
      <TypeLayer
        name="solution-copy"
        start={30}
        duration={20}
        bounce={5}
        count={20}
      />
      <div style={{ opacity: progress(f, 6, 19) }}>
        <Gleams />
      </div>
      <Layer
        name="happy-woman"
        style={{
          translate: `0px ${interpolate(f, [9, 21, 28], [120, -12, 0], clamp)}px`,
          rotate: `${f < 28 ? 0 : Math.sin((f - 28) * 0.1) * 0.45}deg`,
          transformOrigin: "60px 102px",
        }}
      />
    </>
  );
};
