import "./index.css";
import { MyComposition } from "./Composition";
import { Composition } from "remotion";
import { ReferenceRecreation } from "./sample/Recreation";

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
    </>
  );
};
