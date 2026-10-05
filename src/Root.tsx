import "./index.css";
import { MyComposition } from "./Composition";
import { Composition } from "remotion";
import { Cut01 } from "./Cut01";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <MyComposition />
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
