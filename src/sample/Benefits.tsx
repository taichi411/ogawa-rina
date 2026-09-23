import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { Layer, TypeLayer, Monitor, progress, clamp } from "./shared";

export const Benefits: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <>
      <div
        style={{
          position: "absolute",
          inset: 0,
          translate: `0px ${interpolate(f, [0, 31], [-43, 0], clamp)}px`,
        }}
      >
        <Monitor x={149} y={102} w={190} h={154} />
      </div>
      <TypeLayer
        name="benefit-heading"
        start={0}
        duration={20}
        count={21}
        bounce={4}
      />
      <TypeLayer
        name="benefit-title"
        start={9}
        duration={28}
        count={21}
        bounce={9}
      />
      <Layer
        name="folder-alone"
        style={{
          opacity: progress(f, 40, 45) * (1 - progress(f, 68, 79)),
          scale: interpolate(f, [40, 47, 53], [0.6, 1.08, 1], clamp),
          transformOrigin: "33px 27px",
        }}
      />
      <Layer
        name="folder-papers"
        style={{
          opacity: progress(f, 68, 79),
          translate: `0px ${12 * (1 - progress(f, 68, 79))}px`,
        }}
      />
      {f >= 42 && f < 78 ? (
        <svg width="486" height="274" style={{ position: "absolute" }}>
          <g
            stroke="#f38b6e"
            strokeWidth="2"
            opacity={Math.sin(progress(f, 42, 78) * Math.PI)}
          >
            {Array.from({ length: 8 }, (_, i) => {
              const a = (i * Math.PI) / 4;
              return (
                <line
                  key={i}
                  x1={244 + Math.cos(a) * 38}
                  y1={171 + Math.sin(a) * 38}
                  x2={244 + Math.cos(a) * 47}
                  y2={171 + Math.sin(a) * 47}
                />
              );
            })}
          </g>
        </svg>
      ) : null}
      <Layer
        name="person-left"
        style={{ translate: `0px ${115 * (1 - progress(f, 77, 91))}px` }}
      />
      <Layer
        name="person-center"
        style={{ translate: `0px ${115 * (1 - progress(f, 82, 96))}px` }}
      />
      <Layer
        name="person-right"
        style={{ translate: `0px ${115 * (1 - progress(f, 88, 102))}px` }}
      />
    </>
  );
};
