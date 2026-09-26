import "./index.css";
import { MyComposition } from "./Composition";
import { Composition } from "remotion";
import { ReferenceRecreation } from "./sample/Recreation";
import { Cut01 } from "./Cut01";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <MyComposition />
      <Composition
        id="SampleRecreation"
        component={ReferenceRecreation}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={897}
      />
      <Composition
        id="RinaCut01"
        component={Cut01}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={180}
      />
    </>
  );
};
