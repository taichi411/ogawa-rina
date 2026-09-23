import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { Board, Layer, TypeLayer, progress, clamp } from "./shared";

export const Problems: React.FC = () => {
  const f = useCurrentFrame();
  const left = interpolate(f, [0, 10, 22], [90, -5, 0], clamp);
  const wave = Math.sin(((f + 15) * Math.PI) / 40);
  return (
    <>
      <Board
        x={46}
        y={26}
        w={164}
        h={131}
        style={{
          translate: `0px ${left}px`,
          scale: `1 ${progress(f, 1, 13)}`,
          rotate: `${interpolate(f, [2, 16, 25], [-4, 1, 0], clamp)}deg`,
        }}
      />
      <TypeLayer
        name="problem-line-0"
        start={13}
        duration={6}
        count={7}
        bounce={2}
      />
      <TypeLayer
        name="problem-line-1"
        start={22}
        duration={10}
        count={9}
        bounce={2}
      />
      <TypeLayer
        name="problem-line-2"
        start={34}
        duration={8}
        count={7}
        bounce={2}
      />
      <TypeLayer
        name="problem-line-3"
        start={45}
        duration={16}
        count={10}
        bounce={2}
      />
      <Board
        x={305}
        y={160}
        w={165}
        h={89}
        style={{
          opacity: progress(f, 120, 127),
          translate: `0px ${interpolate(f, [120, 131, 140], [35, -4, 0], clamp)}px`,
          rotate: `${interpolate(f, [120, 133, 141], [-4, 1, 0], clamp)}deg`,
        }}
      />
      <TypeLayer
        name="problem-right-0"
        start={136}
        duration={10}
        count={7}
        bounce={2}
      />
      <TypeLayer
        name="problem-right-1"
        start={149}
        duration={10}
        count={6}
        bounce={2}
      />
      <Layer
        name="shrug-left"
        style={{ transformOrigin: "60px 9px", rotate: `${wave * 13}deg` }}
      />
      <Layer
        name="shrug-right"
        style={{ transformOrigin: "8px 10px", rotate: `${-wave * 13}deg` }}
      />
      <Layer name="shrug-body" />
      <Layer
        name="sweat"
        style={{
          scale: 1 + 0.13 * Math.sin(f * 0.22),
          opacity: 0.8 + 0.2 * Math.sin(f * 0.2),
        }}
      />
    </>
  );
};
