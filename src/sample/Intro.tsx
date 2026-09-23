import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { Layer, TypeLayer, progress, clamp, TEAL } from "./shared";

export const Intro: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <>
      <svg
        width="486"
        height="274"
        style={{ position: "absolute", opacity: progress(f, 17, 26) }}
      >
        <path
          d="M115 44V35Q115 29 122 29H359Q366 29 366 36V45 M119 180V188Q119 196 126 196H299L323 206Q326 208 323 203L317 196H347"
          fill="none"
          stroke={TEAL}
          strokeWidth="2.7"
        />
        <path
          d="M126 69V44Q126 37 135 37H151 M127 73V77 M354 163V179Q354 185 347 185H330 M354 153V158"
          fill="none"
          stroke="#77c9c0"
          strokeWidth="2.4"
        />
      </svg>
      <TypeLayer
        name="intro-title"
        start={18}
        duration={10}
        count={8}
        bounce={19}
      />
      <TypeLayer
        name="intro-problem"
        start={25}
        duration={4}
        count={7}
        bounce={25}
      />
      <TypeLayer
        name="intro-question"
        start={49}
        duration={10}
        count={8}
        bounce={4}
      />
      <Layer
        name="intro-woman"
        style={{
          translate: `0px ${interpolate(f, [24, 33, 39], [130, -4, 0], clamp)}px`,
          opacity: progress(f, 24, 27),
        }}
      />
      <Layer
        name="question"
        style={{
          opacity: progress(f, 27, 32),
          rotate: `${interpolate(f, [28, 34, 42], [-18, 8, 0], clamp)}deg`,
          scale: interpolate(f, [26, 33, 41], [0.3, 1.12, 1], clamp),
        }}
      />
      {f >= 52 && f < 68 ? (
        <div
          style={{
            position: "absolute",
            left: 148,
            top: 168,
            height: 1.5,
            width: 178 * progress(f, 52, 60),
            background: "#f3aa77",
            opacity: 1 - progress(f, 62, 68),
          }}
        />
      ) : null}
    </>
  );
};
