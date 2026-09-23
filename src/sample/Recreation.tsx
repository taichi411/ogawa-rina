import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";
import { Intro } from "./Intro";
import { Problems } from "./Problems";
import { Solution } from "./Solution";
import { Benefits } from "./Benefits";
import { Question } from "./Question";
import { CallToAction } from "./CallToAction";
import { MINT, TEAL } from "./shared";
import { wipe } from "./wipe";

const Shutters: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <>
      {(wipe[f] ?? []).map(([x, w, color], i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            top: 0,
            bottom: 0,
            left: x,
            width: w,
            background: color === 1 ? "#000" : TEAL,
          }}
        />
      ))}
    </>
  );
};

export const ReferenceRecreation: React.FC = () => {
  const { width, height } = useVideoConfig();
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: MINT }}>
      <div
        style={{
          position: "absolute",
          width: 486,
          height: 274,
          left: 0,
          top: 0,
          transform: `scale(${width / 486},${height / 274})`,
          transformOrigin: "top left",
          overflow: "hidden",
          background: MINT,
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            overflow: "hidden",
            clipPath: "inset(14px 14px 14px 15px)",
          }}
        >
          <Sequence durationInFrames={98} name="01 リード獲得の悩み">
            <Intro />
          </Sequence>
          <Sequence
            from={98}
            durationInFrames={216}
            name="02 マーケティングの課題"
          >
            <Problems />
          </Sequence>
          <Sequence
            from={314}
            durationInFrames={154}
            name="03 ホワイトペーパー"
          >
            <Solution />
          </Sequence>
          <Sequence
            from={468}
            durationInFrames={151}
            name="04 リード獲得の仕組み"
          >
            <Benefits />
          </Sequence>
          <Sequence
            from={619}
            durationInFrames={139}
            name="05 企画・制作の悩み"
          >
            <Question />
          </Sequence>
          <Sequence from={758} durationInFrames={139} name="06 はじめかた・CTA">
            <CallToAction />
          </Sequence>
        </div>
        {f >= 17 ? (
          <div
            style={{
              position: "absolute",
              inset: 0,
              border: `14px solid ${TEAL}`,
              borderLeftWidth: 15,
              pointerEvents: "none",
            }}
          />
        ) : null}
        <Shutters />
      </div>
      <Audio src={staticFile("sample-recreation/reference-audio.m4a")} />
    </AbsoluteFill>
  );
};
