import React from "react";
import {
  Img,
  interpolate,
  Easing,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { layers } from "./layers";

export const MINT = "#e8f6f2";
export const TEAL = "#398784";
export const CORAL = "#f36653";
export const YELLOW = "#f4c619";
export const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;
export const ease = Easing.bezier(0.18, 0.82, 0.22, 1);
export const progress = (f: number, start: number, end: number) =>
  interpolate(f, [start, end], [0, 1], { ...clamp, easing: ease });
export type LayerName = keyof typeof layers;

export const Layer: React.FC<{
  name: LayerName;
  style?: React.CSSProperties;
  x?: number;
  y?: number;
}> = ({ name, style, x, y }) => {
  const l = layers[name];
  return (
    <Img
      src={staticFile(`sample-recreation/${name}.png`)}
      style={{
        position: "absolute",
        left: x ?? l.x,
        top: y ?? l.y,
        width: l.w,
        height: l.h,
        ...style,
      }}
    />
  );
};

/** Source-derived type contours are split into individual animated glyph strips.
 * At rest this switches to a single image, so no resampling seams survive. */
export const TypeLayer: React.FC<{
  name: LayerName;
  start: number;
  duration: number;
  count?: number;
  bounce?: number;
}> = ({ name, start, duration, count = 12, bounce = 12 }) => {
  const frame = useCurrentFrame();
  const l = layers[name];
  if (frame < start) return null;
  if (frame > start + duration + 13) return <Layer name={name} />;
  return (
    <>
      {Array.from({ length: count }, (_, i) => {
        const age = frame - start - (i * duration) / count;
        if (age < 0) return null;
        const settle = progress(age, 0, 12);
        const offset = (1 - settle) * Math.sin(i * 1.8 + age * 0.5) * bounce;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: l.x + (i * l.w) / count,
              top: l.y + offset,
              width: l.w / count + 0.12,
              height: l.h,
              overflow: "hidden",
              opacity: Math.min(1, age / 2),
              rotate: `${(1 - settle) * Math.sin(i * 2) * 24}deg`,
            }}
          >
            <Img
              src={staticFile(`sample-recreation/${name}.png`)}
              style={{
                position: "absolute",
                width: l.w,
                height: l.h,
                maxWidth: "none",
                left: (-i * l.w) / count,
                top: 0,
              }}
            />
          </div>
        );
      })}
    </>
  );
};

export const Spark: React.FC<{
  x: number;
  y: number;
  r?: number;
  phase?: number;
}> = ({ x, y, r = 8, phase = 0 }) => {
  const f = useCurrentFrame();
  const s = 0.95 + 0.25 * Math.sin(f * 0.11 + phase);
  return (
    <svg
      style={{
        position: "absolute",
        left: x - r,
        top: y - r,
        width: 2 * r,
        height: 2 * r,
        scale: s,
        overflow: "visible",
      }}
      viewBox="-10 -10 20 20"
    >
      <path
        d="M0 -9 Q1 -1 9 0 Q1 1 0 9 Q-1 1 -9 0 Q-1 -1 0 -9Z"
        fill={MINT}
        stroke="#343f3e"
        strokeWidth="1"
      />
    </svg>
  );
};

export const Monitor: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
}> = ({ x, y, w, h }) => (
  <svg
    viewBox="0 0 190 154"
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      height: h,
      overflow: "visible",
    }}
  >
    <g
      fill="#fbfdfc"
      stroke="#697371"
      strokeWidth="1.15"
      strokeLinejoin="round"
    >
      <rect x="2" y="2" width="182" height="122" rx="1" />
      <rect x="10" y="10" width="166" height="98" fill={MINT} />
      <rect x="84" y="113" width="14" height="4" rx="2" />
      <path d="M77 125 L77 137 L63 148 L122 148 L107 137 L107 125Z" />
      <path d="M77 137H107 M63 146H122 M62 149H123V153H62Z" />
      <path d="M135 124 Q134 137 157 135 Q174 134 173 143" fill="none" />
      <path d="M163 142 Q160 142 158 147V153H190V148 Q188 142 184 142Z" />
    </g>
  </svg>
);

export const Board: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  style?: React.CSSProperties;
}> = ({ x, y, w, h, style }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      height: h,
      ...style,
    }}
  >
    <svg
      width={w}
      height={h}
      viewBox={`0 0 ${w} ${h}`}
      style={{ overflow: "visible" }}
    >
      <path
        d={`M0 9V2Q0 0 4 0H${w - 2}Q${w} 0 ${w} 3V10 M2 ${h - 10}V${h - 3}Q2 ${h} 5 ${h}H${w * 0.55}L${w * 0.62} ${h + 5}L${w * 0.61} ${h}H${w}`}
        fill="none"
        stroke="#3b4846"
        strokeWidth="1.2"
      />
      <rect x="4" y="7" width={w - 7} height={h - 14} rx="5" fill={TEAL} />
      <path
        d={`M9 37V15Q9 11 14 11H43 M${w - 15} ${h - 40}V${h - 18}Q${w - 15} ${h - 12} ${w - 22} ${h - 12}H${w - 47}`}
        fill="none"
        stroke="#72c7c1"
        strokeWidth="1.4"
      />
    </svg>
  </div>
);

export const Gleams: React.FC<{ variant?: "solution" | "cta" }> = ({
  variant = "solution",
}) => {
  const coords =
    variant === "solution"
      ? [
          [91, 131, 8],
          [101, 70, 5],
          [399, 79, 7],
          [417, 95, 8],
          [400, 135, 6],
          [335, 181, 8],
          [412, 162, 7],
          [84, 154, 3],
          [430, 114, 3],
          [83, 70, 3],
          [100, 163, 2],
          [344, 194, 4],
        ]
      : [
          [113, 144, 9],
          [124, 161, 3],
          [190, 144, 9],
          [387, 117, 9],
          [366, 147, 6],
          [386, 176, 6],
          [363, 182, 4],
          [176, 168, 4],
          [164, 128, 4],
          [178, 109, 2],
          [365, 198, 2],
        ];
  return (
    <>
      {coords.map(([x, y, r], i) => (
        <Spark key={i} x={x} y={y} r={r} phase={i * 1.2} />
      ))}
    </>
  );
};
