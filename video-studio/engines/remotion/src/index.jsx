import React from "react";
import { registerRoot, Composition, AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

const Video = ({ hook, bullets }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fade = (start) => interpolate(f, [start, start + fps / 2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: "#0b1b2b", color: "#fff", fontFamily: "sans-serif", padding: "14% 8%" }}>
      <h1 style={{ fontSize: 64, opacity: fade(0) }}>{hook}</h1>
      {bullets.map((b, i) => (
        <p key={i} style={{ fontSize: 48, opacity: fade(fps * (2 + i * 1.5)) }}>• {b}</p>
      ))}
    </AbsoluteFill>
  );
};

// Kích thước và độ dài lấy từ --props (spec JSON) nên không cần sửa mã khi đổi video.
const Root = () => (
  <Composition
    id="Main"
    component={Video}
    fps={30}
    width={1080}
    height={1920}
    durationInFrames={450}
    defaultProps={{ hook: "", bullets: [] }}
    calculateMetadata={({ props }) => ({
      durationInFrames: props.duration * 30,
      width: props.platform === "youtube" ? 1920 : 1080,
      height: props.platform === "youtube" ? 1080 : 1920,
    })}
  />
);
registerRoot(Root);
