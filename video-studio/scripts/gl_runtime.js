// Chạy một chuyển cảnh gl-transitions trên <canvas> bằng WebGL. Dùng chung cho bộ dựng (HyperFrames) và khung xem thử trong app.
// glT(canvas) → { draw(name, fromImg, toImg, progress) }   (lib: danh mục gl_transitions.json)
function glT(canvas, lib) {
  const gl = canvas.getContext("webgl", { preserveDrawingBuffer: true, premultipliedAlpha: false });
  const progs = {}, texCache = new Map();
  const VS = "attribute vec2 _p;varying vec2 _uv;void main(){gl_Position=vec4(_p,0.,1.);_uv=vec2(.5,.5)*(_p+vec2(1.,1.));}";
  const head = "precision highp float;varying vec2 _uv;uniform sampler2D from,to;uniform float progress,ratio,_fromR,_toR;"
    + "vec4 getFromColor(vec2 uv){return texture2D(from,.5+(uv-.5)*vec2(min(ratio/_fromR,1.),min(_fromR/ratio,1.)));}"
    + "vec4 getToColor(vec2 uv){return texture2D(to,.5+(uv-.5)*vec2(min(ratio/_toR,1.),min(_toR/ratio,1.)));}\n";
  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
  function sh(type, src) {
    const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }
  function prog(name) {
    if (progs[name]) return progs[name];
    const t = lib[name], p = gl.createProgram();
    gl.attachShader(p, sh(gl.VERTEX_SHADER, VS));
    gl.attachShader(p, sh(gl.FRAGMENT_SHADER, head + t.glsl + "\nvoid main(){gl_FragColor=transition(_uv);}"));
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    return (progs[name] = p);
  }
  function tex(img) {
    if (texCache.has(img)) return texCache.get(img);
    const t = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
    for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]])
      gl.texParameteri(gl.TEXTURE_2D, k, v);
    texCache.set(img, t);
    return t;
  }
  return {
    compile: prog,
    draw(name, from, to, progress) {
      const p = prog(name), t = lib[name];
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.useProgram(p);
      const loc = gl.getAttribLocation(p, "_p");
      gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
      [["from", from], ["to", to]].forEach(([u, img], i) => {
        gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, tex(img)); gl.uniform1i(gl.getUniformLocation(p, u), i);
      });
      const r = canvas.width / canvas.height;
      gl.uniform1f(gl.getUniformLocation(p, "progress"), progress);
      for (const u of ["ratio", "_fromR", "_toR"]) gl.uniform1f(gl.getUniformLocation(p, u), r);
      for (const [n, [type, v]] of Object.entries(t.params)) {
        const l = gl.getUniformLocation(p, n); if (!l) continue;
        const a = [].concat(v);
        if (type === "float") gl.uniform1f(l, a[0]);
        else if (type === "int" || type === "bool") gl.uniform1i(l, a[0]);
        else if (type === "ivec2") gl.uniform2iv(l, a);
        else gl["uniform" + a.length + "fv"](l, a);
      }
      gl.drawArrays(gl.TRIANGLES, 0, 6);
    },
  };
}
if (typeof module !== "undefined") module.exports = glT;
