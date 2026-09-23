import React from "react";
import { useCurrentFrame } from "remotion";
import { Layer, TypeLayer, progress, TEAL } from "./shared";

export const Question: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <>
      <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
        {Array.from({ length: 56 }, (_, i) => {
          const row = Math.floor(i / 8) - 1,
            col = (i % 8) - 1;
          return (
            <Layer
              key={i}
              name="background-question"
              x={
                18 + col * 70 + Math.abs(row % 2) * 33 - Math.floor(row / 2) * 5
              }
              y={47 + row * 46.75}
              style={{
                opacity: progress(f, col * 1.5 + row, 17 + col),
                scale: progress(f, col + row, 15 + col),
              }}
            />
          );
        })}
      </div>
      <svg
        width="486"
        height="274"
        style={{ position: "absolute", opacity: progress(f, 1, 8) }}
      >
        <path
          d="M121 117V125H238L249 132L246 125H379V117"
          stroke={TEAL}
          fill="none"
          strokeWidth="2"
        />
        <rect x="122" y="37" width="258" height="84" rx="3" fill="#fff" />
      </svg>
      <TypeLayer
        name="question-copy"
        start={6}
        duration={31}
        count={23}
        bounce={17}
      />
      <Layer
        name="desk-woman"
        style={{ translate: `0px ${125 * (1 - progress(f, 0, 10))}px` }}
      />
      <Layer
        name="books-left"
        style={{ clipPath: `inset(${100 * (1 - progress(f, 6, 39))}% 0 0 0)` }}
      />
      <Layer
        name="books-right"
        style={{ clipPath: `inset(${100 * (1 - progress(f, 10, 44))}% 0 0 0)` }}
      />
      <Layer
        name="sweat"
        x={297}
        y={143}
        style={{ rotate: "-25deg", scale: 1.2 + 0.12 * Math.sin(f * 0.24) }}
      />
    </>
  );
};
