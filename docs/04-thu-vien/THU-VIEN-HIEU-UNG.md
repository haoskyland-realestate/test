# Thư viện hiệu ứng v1

Tự sinh từ `video-studio/scripts/effects.py`. Dùng tên ở cột đầu trong `timeline.json`.

## Phong cách (`meta.style`)
| Tên | Mô tả |
|---|---|
| `hien-dai` | Hiện đại: chữ đậm không chân, vàng nhấn, nhịp nhanh (giống video test đã duyệt) |
| `sang-trong` | Sang trọng: navy + vàng champagne, tiêu đề chữ có chân, chuyển động chậm, màu ấm có viền tối |
| `toi-gian` | Tối giản: đen trắng, một màu nhấn nhạt, chữ mảnh, hiện mờ dần, màu nhạt |
| `edit-phim` | Edit phim (mẫu edit-phim-01): chữ trắng nổi 3D giữa khung, lao vào mờ → rõ, nhịp nhanh, màu rực, phụ đề nhỏ nền tối |
| `vang-cao-cap` | Vàng cao cấp: chữ Anton vàng ánh kim căn giữa, từng từ bật ra theo lời, thẻ minh hoạ nền đen viền vàng |
| `chu-mau` | Chữ động nhiều màu: từng từ bật ra, xếp chồng, to nhỏ xen kẽ, trắng – xanh ngọc – cam – hồng |
| `neon-cam` | Neon cam: chữ cam phát sáng gõ dần theo lời, số nổi cam, thẻ tối viền sáng, khung gần – xa xen kẽ |
| `giai-thich-sang` | Giải thích sáng: thẻ trắng bo góc, nhãn BƯỚC cam, chữ đen dễ đọc, thẻ minh hoạ nền kem – hợp hướng dẫn thủ tục, quy trình |

## Chỉnh màu (`look` của từng cảnh, mặc định theo phong cách)
| Tên | Mô tả |
|---|---|
| `tu-nhien` | Tự nhiên: màu thật, chỉ tự cân |
| `tuoi-dam` | Tươi đậm: rực, tương phản rõ, hợp mạng xã hội |
| `trong-treo` | Trong trẻo: sáng, nhẹ, trời xanh, hợp nội thất và nhà mẫu |
| `am-sang` | Ấm sang: ấm nhẹ, bớt rực, viền tối, hạt phim nhẹ |
| `dien-anh` | Điện ảnh: vùng tối xanh ngọc, da và nắng cam ấm |
| `nang-chieu` | Nắng chiều: vàng ấm, dịu |
| `mat-hien-dai` | Mát hiện đại: xanh nhẹ, tương phản cao |
| `nhat-toi-gian` | Nhạt tối giản: sáng, ít màu, ít tương phản |
| `den-trang` | Đen trắng tương phản |
| `trung-tinh` | Tự nhiên: màu thật, chỉ tự cân |

## Chuyển cảnh (`transitions[].type`, đổi độ dài bằng `dur`)
| Tên | Mặc định | Mô tả |
|---|---|---|
| `cut` | 0.0s | Cắt thẳng (mặc định, dùng nhiều nhất) |
| `cube-h` | 0.8s | Khối 3D xoay ngang: sang chương mới |
| `cube-v` | 0.8s | Khối 3D xoay dọc: sang chương mới |
| `flip` | 0.8s | Lật thẻ 3D: đổi phương án, so sánh |
| `fade` | 0.5s | Hòa tan: đổi thời gian, cảm xúc chậm |
| `dip` | 0.6s | Tối dần rồi sáng: mở/kết chương |
| `zoom` | 0.5s | Phóng xuyên: từ xa vào gần, ngoài vào trong |
| `slide` | 0.4s | Trượt ngang: danh sách, từng mục |
| `wipe` | 0.5s | Quét ngang: tối giản |
| `circle` | 0.6s | Mở vòng tròn: tiết lộ, nhấn mạnh |
| `gl-BookFlip` | 0.8s | Lật sách · The right half of the outgoing image is a book page that turns over from right to left on the spine at the middle of the frame, curling near its free edge, its back bringing the left half of the incoming image (gl-transitions) |
| `gl-CameraShake` | 0.8s | Rung máy · The camera jolts violently in random directions, with motion blur and color fringes along each jolt; the cut happens at the peak of the shake, which then settles on the incoming image (gl-transitions) |
| `gl-CircleIris` | 0.8s | Mở mống mắt tròn · The outgoing image closes into a circle over a background color, then the incoming one opens from it (gl-transitions) |
| `gl-CrossZoom` | 0.8s | Phóng chéo mờ chuyển động · A crossfade through a strong zoom blur (gl-transitions) |
| `gl-DefocusBlur` | 0.8s | Mất nét rồi rõ · A crossfade through an out-of-focus blur (gl-transitions) |
| `gl-Directional` | 0.8s | Trượt theo hướng · The incoming image pushes the outgoing one out in a given direction (gl-transitions) |
| `gl-Doorway` | 0.8s | Mở cửa · The outgoing image opens like double doors swinging toward the viewer, as the incoming one comes forward from the dark room behind, with a floor reflection (gl-transitions) |
| `gl-Dreamy` | 0.8s | Mơ màng, sang trọng · A crossfade with a gentle wavy distortion (gl-transitions) |
| `gl-DreamyZoom` | 0.8s | Phóng mơ màng · Zooms and rotates into a bright flash, then out to the incoming image (gl-transitions) |
| `gl-FilmBurn` | 0.8s | Cháy phim · Glowing film-burn light leaks wash over the image and reveal the incoming one (gl-transitions) |
| `gl-GlowDissolve` | 0.8s | Hòa tan phát sáng · The incoming image spreads over the outgoing one with a hot, glowing edge (gl-transitions) |
| `gl-InvertedPageCurl` | 0.8s | Cuộn trang · The outgoing image curls away like a page, revealing the incoming one (gl-transitions) |
| `gl-LensFlare` | 0.8s | Lóe sáng ống kính · A bright light sweeps across the frame and flares the lens: a long thin horizontal streak, a glowing core and a trail of colored ghost reflections; at its peak the incoming image spreads out from the light under its glare (gl-transitions) |
| `gl-LightWipe` | 0.8s | Quét ánh sáng · A band of intense light sweeps across the frame like a glint on glass, blooming the highlights of both images, and leaves the incoming image behind it (gl-transitions) |
| `gl-Morph` | 0.8s | Biến hình mềm · A crossfade in which each image is displaced by the other's colors, like a morph (gl-transitions) |
| `gl-Swirl` | 0.8s | Xoáy · The image twists into a round swirl around the center that peaks mid-way, where the outgoing image dissolves into the incoming one, then untwists (gl-transitions) |
| `gl-WhipPan` | 0.8s | Lia nhanh ngang · A fast camera pan that streaks both images with motion blur, the incoming one arriving from the opposite side (gl-transitions) |
| `gl-WhipTilt` | 0.8s | Lia nhanh dọc · The camera tilts fast from the outgoing image to the incoming one, set edge to edge at an angle above it, streaking both in perspective with a vertical motion blur (gl-transitions) |
| `gl-WindowBlinds` | 0.8s | Rèm cửa sổ · A crossfade through horizontal window blinds (gl-transitions) |
| `gl-ZoomInOut` | 0.8s | Phóng vào rồi ra · Zooms into the outgoing image until it blurs into a flat color, then out to the incoming one (gl-transitions) |
| `gl-Accordion` | 0.8s | The outgoing image folds up like a pleated paper toward one side while the incoming one unfolds out of the other, both in 3D with lit and shadowed pleats (gl-transitions) |
| `gl-ApertureWipe` | 0.8s | A camera aperture opens its turning blades to reveal the incoming image (gl-transitions) |
| `gl-ArrowWipe` | 0.8s | A notched arrowhead window onto the incoming image flies in from the edge behind it (or appears at the center), then swells until it fills the frame (gl-transitions) |
| `gl-Ascii` | 0.8s | The image turns into text-mode characters, denser where it is brighter, the characters scramble into those of the incoming image, then resolve back into it (gl-transitions) |
| `gl-BandWipe` | 0.8s | Alternating bands wipe in from opposite sides together and interleave like fingers, while both images stay still (gl-transitions) |
| `gl-BlockCover` | 0.8s | Blocks of a solid color pop in at random over the outgoing image until they cover the frame, then pop out in another random order to show the incoming image (gl-transitions) |
| `gl-BlockSlide` | 0.8s | The frame is cut into a grid of blocks that slide out one after another in a staggered cascade, some of them shrinking as they go, while the blocks of the incoming image slide in behind them to take their place (gl-transitions) |
| `gl-BloomDissolve` | 0.8s | The highlights of the outgoing image blow out into a soft, wide glow that floods the frame; under it the incoming image takes over, then the glow subsides back into its highlights while the image stays sharp (gl-transitions) |
| `gl-BokehDissolve` | 0.8s | The image falls out of focus like a camera lens, its highlights swelling into large bright bokeh discs, and the incoming image sharpens back out of its own bokeh (gl-transitions) |
| `gl-Bounce` | 0.8s | The outgoing image drops out of the frame with a few bounces, revealing the incoming one (gl-transitions) |
| `gl-BowTie` | 0.8s | Two triangles grow from the top and bottom edges into a bow tie that reveals the incoming image, with an adjustable shape, and can run in reverse (gl-transitions) |
| `gl-BowTieHorizontal` | 0.8s | Two triangles grow from the left and right edges into a bow tie that reveals the incoming image (gl-transitions) |
| `gl-BrushWipe` | 0.8s | A few broad brush strokes sweep across the frame in turn, back and forth, painting in the incoming image with streaky bristle edges and dry, ragged ends (gl-transitions) |
| `gl-BurnThrough` | 0.8s | The outgoing image burns away in noisy, glowing patches (gl-transitions) |
| `gl-ButterflyWaveScrawler` | 0.8s | Wavy, color-separated ripples scramble the outgoing image into the incoming one (gl-transitions) |
| `gl-CardSwipe` | 0.8s | The outgoing image is flicked off like the top card of a stack, swinging around a point below it as it flies out, while the incoming card behind it grows to fill the frame (gl-transitions) |
| `gl-CellDissolve` | 0.8s | Irregular cells, like cracked mud or soap foam, switch to the incoming image one by one, with an optional bright border glowing along the cracks between them (gl-transitions) |
| `gl-Chessboard` | 0.8s | A chessboard pattern of squares reveals the incoming image (gl-transitions) |
| `gl-CircleBurst` | 0.8s | Discs of three solid colors burst out of a point one after another, each covering the last, then a hole bursts open from the same point in the last one to reveal the incoming image (gl-transitions) |
| `gl-CircleOpen` | 0.8s | A soft-edged circle opens from the center to reveal the incoming image (gl-transitions) |
| `gl-ClockWipe` | 0.8s | A wipe that sweeps around the center from a starting angle (gl-transitions) |
| `gl-Clothesline` | 0.8s | The camera pulls back to show the outgoing image as a print hung by two clothespins on a line in front of a wall, the line is pulled sideways and carries it away while the incoming print slides in, both prints swinging and tilting like hanging paper, then the camera moves back in on the incoming print until it fills the frame (gl-transitions) |
| `gl-CodeRain` | 0.8s | The outgoing image darkens into a grid of flickering code characters tinted by its colors, then glowing streams of characters fall down the columns at their own speeds, each with a bright head and a fading tail, leaving the incoming image behind (gl-transitions) |
| `gl-ColorCoords` | 0.8s | A crossfade in which the colors of one image displace the other (gl-transitions) |
| `gl-ColorDistance` | 0.8s | Pixels switch to the incoming image in order of how close their colors are (gl-transitions) |
| `gl-ColorPanelWipe` | 0.8s | Solid color panels, slightly staggered, sweep across and cover the frame, then sweep off the far side and reveal the incoming image (gl-transitions) |
| `gl-ColorPhase` | 0.8s | A crossfade in which each color channel changes at a different time (gl-transitions) |
| `gl-ColorWrap` | 0.8s | Each color channel of the outgoing image is shifted and wraps around into psychedelic bands, while crossfading to the incoming image (gl-transitions) |
| `gl-Comb` | 0.8s | The frame is cut into interleaved strips that slide in opposite directions, each pushing the outgoing image out and the incoming one in (gl-transitions) |
| `gl-ComicPanels` | 0.8s | The frame splits into slanted comic-book panels with gutters and ink borders; one after another in reading order, each panel lifts off the page with a zoom kick and a drop shadow and punches over to the incoming image, then the gutters close up over the full incoming image (gl-transitions) |
| `gl-CrazyParametricFun` | 0.8s | The outgoing image is pulled along a parametric curve into a psychedelic swirl (gl-transitions) |
| `gl-CrossWarp` | 0.8s | The outgoing image zooms in while the incoming one zooms out into place, sweeping from right to left (gl-transitions) |
| `gl-Crosshatch` | 0.8s | The incoming image appears through a crosshatch of lines spreading from the center (gl-transitions) |
| `gl-Crumple` | 0.8s | The outgoing image crumples into a creased paper ball, shaded along its folds, which is then tossed away to reveal the incoming image (gl-transitions) |
| `gl-Cube` | 0.8s | The two images are faces of a box that turns a quarter turn in perspective, the outgoing face darkening as it turns away, above a reflective floor (gl-transitions) |
| `gl-CurtainRise` | 0.8s | The outgoing image rises like a theater festoon curtain: cords lift its hem into scalloped swags while the fabric gathers into shaded ruffles, and it is drawn up out of the frame over the incoming image (gl-transitions) |
| `gl-Curtains` | 0.8s | The outgoing image parts in the middle like stage curtains, gathering into shaded folds as it is pulled to the sides (gl-transitions) |
| `gl-CurvedWipe` | 0.8s | The outgoing image is pulled away by its middle: the wipe edge bulges into a smooth curve that leads the way, then flattens as it reaches the far side (gl-transitions) |
| `gl-CylinderRoll` | 0.8s | The frame wraps around a drum that rolls up, the outgoing image turning away over its top in a motion blur and the incoming one coming around from below and unrolling flat (gl-transitions) |
| `gl-DiamondWipe` | 0.8s | A soft-edged diamond grows from the center to reveal the incoming image (gl-transitions) |
| `gl-DirectionalEased` | 0.8s | Like Directional, with an eased movement (gl-transitions) |
| `gl-DirectionalScaled` | 0.8s | Like Directional, with both images scaled down while they slide (gl-transitions) |
| `gl-DirectionalWarp` | 0.8s | A diagonal wipe with a warped, smeared edge (gl-transitions) |
| `gl-DirectionalWipe` | 0.8s | A straight wipe in any direction, diagonal and soft-edged by default; a smoothness of 0 gives a hard edge (gl-transitions) |
| `gl-Disintegrate` | 0.8s | The outgoing image crumbles into fine dust from one side, its grains blown away by the wind and fading out, revealing the incoming image underneath (gl-transitions) |
| `gl-DitherDissolve` | 0.8s | The incoming image appears through a regular 8x8 ordered dither pattern, like a retro computer screen (gl-transitions) |
| `gl-DominoFall` | 0.8s | The outgoing image is cut into standing slats that topple backward like dominoes in a chain reaction across the frame, each one leaning onto the next and knocking it over, until they all lie flat and reveal the incoming image (gl-transitions) |
| `gl-DoomMelt` | 0.8s | The outgoing image melts down in uneven columns, like the Doom screen wipe (gl-transitions) |
| `gl-Drape` | 0.8s | The outgoing image hangs like a sheet of fabric that is let go at the top: it collapses into soft, uneven folds that hide one another as the cloth bunches up and slides down out of the frame, revealing the incoming image behind it (gl-transitions) |
| `gl-DuotoneFade` | 0.8s | The outgoing image is printed in two inks, shadows first, as a bold high-contrast duotone; the incoming image is printed over it in the same two inks, its dark tones landing before its highlights, then its own colors come back, highlights first (gl-transitions) |
| `gl-EdgeGlow` | 0.8s | Both images fade through black with their edges glowing (gl-transitions) |
| `gl-EyeBlink` | 0.8s | Curved eyelids close from the top and bottom over the outgoing image, which blurs and dims, then open on the incoming image as it comes back into focus, as if the viewer blinked (gl-transitions) |
| `gl-FacetedGlass` | 0.8s | The frame is seen through a pane of irregular cut-glass facets, each one showing its own shifted, zoomed and tilted view of the image, with bright beveled edges and thin dark seams; the facets turn to the incoming image one by one, then the glass flattens out and clears (gl-transitions) |
| `gl-Fade` | 0.8s | A linear crossfade between the two images (gl-transitions) |
| `gl-FadeColor` | 0.8s | A fade through a solid color, black by default (gl-transitions) |
| `gl-FadeGrayscale` | 0.8s | A crossfade through grayscale (gl-transitions) |
| `gl-FallOver` | 0.8s | The outgoing image falls over backward, hinged on its bottom edge, revealing the incoming one behind it (gl-transitions) |
| `gl-FilmDissolve` | 0.8s | A cross-dissolve blended in linear light, as light adds up on film: the frame keeps its brightness all the way through and the highlights of each image shine through the other (gl-transitions) |
| `gl-FilmStrip` | 0.8s | The picture slips like film in a projector gate: it shrinks to show the sprocket holes, the strip runs down with motion blur and a slight weave, then the incoming frame lands in place (gl-transitions) |
| `gl-Fisheye` | 0.8s | The outgoing image bulges toward the viewer through a strong fisheye lens, then the incoming one flattens back into place (gl-transitions) |
| `gl-FlameWipe` | 0.8s | A wall of flames sweeps across the frame, scorching the outgoing image ahead of it and leaving the incoming image under a fading warm glow (gl-transitions) |
| `gl-FlashFade` | 0.8s | A crossfade that brightens toward a color in the middle (gl-transitions) |
| `gl-FlowerWipe` | 0.8s | A flower shape with several petals grows to reveal the incoming image (gl-transitions) |
| `gl-FlyEye` | 0.8s | The image breaks into a fly's-eye grid of lenses with color separation (gl-transitions) |
| `gl-Fold` | 0.8s | The incoming image unfolds from the left while the outgoing one folds away to the right (gl-transitions) |
| `gl-FrostWipe` | 0.8s | Ice crystals grow in from the edges of the frame with feathery, branching fronts, frosting the outgoing image white and blurry until it is covered, then thaw back out to the edges on the incoming image (gl-transitions) |
| `gl-Funnel` | 0.8s | The outgoing image narrows into a curved funnel toward a point on the bottom edge and slides into it, its sides bending like a window minimized into a dock, revealing the incoming image behind it (gl-transitions) |
| `gl-Gallery` | 0.8s | The camera pulls back from the outgoing image to show it as a slide hanging in a row on a wall in perspective, the row glides along as each slide turns away from the center, and the camera moves back in on the incoming slide until it fills the frame (gl-transitions) |
| `gl-GlintDissolve` | 0.8s | The bright points of the outgoing image sparkle into crisp four-point star glints that swell and twinkle up to the cut, then shrink back into the highlights of the incoming image, which stays sharp (gl-transitions) |
| `gl-GlitchBands` | 0.8s | A crossfade with glitchy horizontal bands and color shifts (gl-transitions) |
| `gl-GlitchDisplace` | 0.8s | Blocks of the image are displaced in a glitch that flashes into the incoming image (gl-transitions) |
| `gl-GlitchFlicker` | 0.8s | A flickering glitch with RGB offset, ghosting and scanlines that flashes back to the outgoing image (gl-transitions) |
| `gl-GlitchMemories` | 0.8s | A crossfade with glitchy, color-shifted blocks (gl-transitions) |
| `gl-GlitterDissolve` | 0.8s | The image becomes a shimmering field of tiny diamond sequins that flip over in 3D at random moments, each lifting and tilting on its own axis and flashing a glint of light, and land on the incoming image (gl-transitions) |
| `gl-GooeyWipe` | 0.8s | Soft, glossy blobs of liquid pop up over the outgoing image, swell and melt into each other, revealing the incoming image until they cover the whole frame (gl-transitions) |
| `gl-GravityLens` | 0.8s | A black disk appears and grows, bending the outgoing image around it like a heavy mass bends light: the image is stretched into a bright ring at the disk's edge and swallowed until the frame is black, then the disk shrinks back, unbending the incoming image (gl-transitions) |
| `gl-GridFlip` | 0.8s | The image splits into a grid of cards that lift apart and turn over in perspective one after another, each one showing its part of the incoming image on its back (gl-transitions) |
| `gl-Halftone` | 0.8s | The image breaks into printed halftone dots whose size follows its shades, the dots reshape into the incoming image, then merge back into it (gl-transitions) |
| `gl-HeartWipe` | 0.8s | A heart grows from the center with a little heartbeat to reveal the incoming image (gl-transitions) |
| `gl-HeatHaze` | 0.8s | Shimmering heat waves rise through the frame, strongest at the bottom, making the outgoing image wobble like the air over hot asphalt; the incoming image shows through the haze and settles as it calms (gl-transitions) |
| `gl-Hexagonalize` | 0.8s | Both images turn into hexagons, crossfade, then sharpen again (gl-transitions) |
| `gl-Hologram` | 0.8s | The outgoing image turns into a flickering hologram (blue by default) with scanlines and jittering rows, breaks up, and the hologram resolves into the incoming image in full color (gl-transitions) |
| `gl-Honeycomb` | 0.8s | The image splits into hexagons that spin and shrink away in a wave from the center, uncovering the incoming image (gl-transitions) |
| `gl-HorizontalClose` | 0.8s | The incoming image closes in from the top and bottom edges toward the middle (gl-transitions) |
| `gl-HorizontalOpen` | 0.8s | The incoming image opens from a line in the middle toward the top and bottom edges (gl-transitions) |
| `gl-HsvFade` | 0.8s | A crossfade through the HSV color space that cycles through hues (gl-transitions) |
| `gl-InkBleed` | 0.8s | The incoming image spreads over the outgoing one like drops of ink in water, blooming from a few points with curling, wispy edges and a darker rim, until it fills the frame (gl-transitions) |
| `gl-InsetWipe` | 0.8s | A rectangle anchored in a corner, on an edge or in the center grows until the incoming image fills the frame, revealing it in place without scaling it; in reverse, the outgoing image shrinks into the rectangle (gl-transitions) |
| `gl-InsideCube` | 0.8s | The camera stands inside a cube: the outgoing image covers the wall in front of it and the view turns toward the next inner wall, so the outgoing image swings away in perspective as the incoming one turns into view, the walls darkening into the shaded inner corner between them (gl-transitions) |
| `gl-Kaleidoscope` | 0.8s | A crossfade through a spinning kaleidoscope (gl-transitions) |
| `gl-KeyholeWipe` | 0.8s | A keyhole grows steadily from the center until the incoming image fills the frame, its bevelled rim and inner shadow making it read as a hole cut in a plate (gl-transitions) |
| `gl-LeafWipe` | 0.8s | A leaf shape grows from the center to reveal the incoming image (gl-transitions) |
| `gl-LedWall` | 0.8s | The picture zooms into a giant LED screen of round glowing diodes on a dark panel; a refresh wave sweeps across it, each diode flicking with a bright pop as it switches to the incoming image, then the diodes melt back into the plain picture (gl-transitions) |
| `gl-LeftRight` | 0.8s | The outgoing image shrinks away to the left while the incoming one slides in from the right (gl-transitions) |
| `gl-LightRays` | 0.8s | Shafts of light burst from the highlights of the outgoing image and stream outward from a slowly drifting center; at their peak the incoming image takes over and its own rays shrink back into its highlights (gl-transitions) |
| `gl-LightStreaks` | 0.8s | The highlights of the outgoing image flare into long horizontal (or vertical) lens streaks while it smears with motion blur; at the peak the incoming image takes over and its streaks shrink back into its highlights as it sharpens (gl-transitions) |
| `gl-LightningFlash` | 0.8s | Forked lightning bolts crack down from the top of the frame, the screen flashes white in a few stuttering strobes, and the incoming image appears lit by the last flickers as they fade out (gl-transitions) |
| `gl-LiquidFill` | 0.8s | The incoming image rises over the outgoing one like liquid filling a glass, its surface sloshing in waves, lit by a bright meniscus line, bending the image just below it, with a few bubbles rising through it (gl-transitions) |
| `gl-LissajousTiles` | 0.8s | The image breaks into a grid of tiles that swirl along Lissajous curves, in a Scanimate style, and flip one by one to the incoming image before settling back (gl-transitions) |
| `gl-LuminanceMelt` | 0.8s | The outgoing image melts away in noisy vertical streaks, depending on its brightness (gl-transitions) |
| `gl-MoireWipe` | 0.8s | Two sets of fine concentric rings, centered on two points that drift toward each other, overlay the image and interfere into a shifting moire of wide bands; the bands open onto the incoming image and widen until it fills the frame, while the thin dark and light ring lines fade away (gl-transitions) |
| `gl-Mosaic` | 0.8s | The view pans across a mosaic of rotated tiles from both images and settles on the incoming one (gl-transitions) |
| `gl-MultiplyBlend` | 0.8s | A crossfade through the multiplied blend of both images (gl-transitions) |
| `gl-NoiseDissolve` | 0.8s | The incoming image appears pixel by pixel in random noise (gl-transitions) |
| `gl-Overexposure` | 0.8s | A crossfade through a washed-out, overexposed white (gl-transitions) |
| `gl-PaperFold` | 0.8s | The outgoing image is a sheet of paper that folds in half in 3D along a vertical crease, then in half again along a horizontal one, its lit and shaded faces turning to show the back of the paper, and the small folded packet flies off the frame, leaving its shadow on the incoming image underneath (gl-transitions) |
| `gl-PaperTear` | 0.8s | The outgoing image tears in two along a ragged line, and the halves are pulled apart to reveal the incoming one (gl-transitions) |
| `gl-PerlinDissolve` | 0.8s | The incoming image appears through blobs of Perlin noise (gl-transitions) |
| `gl-PhotoDevelop` | 0.8s | The outgoing image washes out to a blank cream card, then the incoming image develops on it like an instant photo: shadows first, faint and tinted, then its contrast and colors come up and it settles (gl-transitions) |
| `gl-Pinwheel` | 0.8s | A spinning pinwheel reveals the incoming image (gl-transitions) |
| `gl-PixelStretch` | 0.8s | A line sweeps across the frame and drags the outgoing image's pixels behind it as long streaks, which shorten as it goes and reveal the incoming image (gl-transitions) |
| `gl-Pixelize` | 0.8s | Both images pixelate, crossfade, then sharpen again (gl-transitions) |
| `gl-PlasmaDissolve` | 0.8s | A flowing plasma of sine waves, as in the old demos, draws moving bands through which the incoming image spreads like tendrils, with a glowing edge (gl-transitions) |
| `gl-PlusWipe` | 0.8s | A plus-shaped cross grows from the center and widens its arms until the incoming image fills the frame (gl-transitions) |
| `gl-PolkaDotsCurtain` | 0.8s | The incoming image appears through growing polka dots (gl-transitions) |
| `gl-PopIn` | 0.8s | The incoming image pops in as a rounded card over the outgoing one, with an elastic overshoot: too big, a bit small, then it settles into the full frame as its corners square off (gl-transitions) |
| `gl-PowerKaleido` | 0.8s | The image folds into an animated kaleidoscope before revealing the incoming one (gl-transitions) |
| `gl-Prisms` | 0.8s | The frame is cut into 3D prisms that turn in a cascade, like a rotating billboard, from the outgoing image on one face to the incoming one on the next (gl-transitions) |
| `gl-Puzzle` | 0.8s | The image is cut into jigsaw puzzle pieces that lift one after another and fall away, revealing the incoming image (gl-transitions) |
| `gl-PuzzleCube` | 0.8s | The frame becomes the face of a twisty cube puzzle: dark gaps open between its cubies, then whole columns and rows of cubies turn a quarter turn around the cube one after another in 3D, each bringing the incoming image from the cube's side to the front, until the gaps close on the incoming image (gl-transitions) |
| `gl-RadialWipe` | 0.8s | A radial wipe that sweeps around the center like a clock hand (gl-transitions) |
| `gl-RandomSquares` | 0.8s | The incoming image appears in random squares (gl-transitions) |
| `gl-RectangleCover` | 0.8s | A rectangle grows from the center to cover the outgoing image, then shrinks to reveal the incoming one (gl-transitions) |
| `gl-RectangleIris` | 0.8s | The outgoing image shrinks into a small rectangle over a background color, then the incoming one grows from it (gl-transitions) |
| `gl-Refraction` | 0.8s | The frame is seen through flowing liquid glass that bends the outgoing image more and more, with rainbow fringes, flares up as the incoming image takes over, then calms down and clears (gl-transitions) |
| `gl-Revolve` | 0.8s | The outgoing image swirls and zooms with motion blur into the incoming one (gl-transitions) |
| `gl-RibbonTwist` | 0.8s | The image twists like a ribbon around its horizontal center line, the twist travelling smoothly across its width, the outgoing image on its front and the incoming one on its back (gl-transitions) |
| `gl-RingSpin` | 0.8s | The frame is cut into concentric rings that spin like the dials of a combination lock, in alternating directions and blurred with speed, one after another from the center outward; each ring overshoots a little and locks into place on the incoming image (gl-transitions) |
| `gl-RingsWipe` | 0.8s | Concentric rings ripple out from the center and, one after another, each sweeps around like a clock hand in the opposite direction of its neighbors to reveal the incoming image, or fills across its width, with optional colored borders between the rings (gl-transitions) |
| `gl-Ripple` | 0.8s | Ripples spread from the center while crossfading (gl-transitions) |
| `gl-Rolls` | 0.8s | The outgoing image rolls away around a corner, revealing the incoming one (gl-transitions) |
| `gl-RotateScaleFade` | 0.8s | The outgoing image spins and zooms while fading to the incoming one, over a background color (gl-transitions) |
| `gl-RotateScaleVanish` | 0.8s | The outgoing image spins and shrinks away over the incoming one (gl-transitions) |
| `gl-SawtoothWipe` | 0.8s | A wipe whose edge is a row of sharp, regular triangular teeth sweeps across the frame, or two toothed edges that start interlocked part from the middle like jaws opening (gl-transitions) |
| `gl-Shatter` | 0.8s | The outgoing image cracks like a pane of glass from an impact point, then its shards break loose from the impact outward, tumbling in 3D and falling away with gravity to reveal the incoming image behind (gl-transitions) |
| `gl-Shred` | 0.8s | The outgoing image is cut into paper strips that drop away at uneven speeds, tilting as they fall, revealing the incoming image (gl-transitions) |
| `gl-SimpleFlip` | 0.8s | The outgoing image flips around the vertical axis into the incoming one (gl-transitions) |
| `gl-SimpleZoom` | 0.8s | Zooms into the outgoing image, then fades to the incoming one (gl-transitions) |
| `gl-SimpleZoomOut` | 0.8s | The incoming image zooms out into place while fading in (gl-transitions) |
| `gl-SketchDissolve` | 0.8s | The outgoing image fades back to blank paper while the incoming one is drawn on it in pencil, outlines first and then hatching in the shadows, before its shading and colors fill in until the picture is complete (gl-transitions) |
| `gl-SlideAwayRight` | 0.8s | The outgoing image slides to the right, uncovering a crossfade to the incoming one (gl-transitions) |
| `gl-Slides` | 0.8s | The outgoing image slides out, or the incoming one slides in, toward an edge, a corner or the center (gl-transitions) |
| `gl-SlotReels` | 0.8s | The frame is cut into vertical reels that spin downward like drums, motion-blurred with speed, carrying the outgoing image then the incoming one, and stop one after another from left to right with a small mechanical bounce (gl-transitions) |
| `gl-SmokeDissolve` | 0.8s | Billowing smoke drifts in across the outgoing image, with lit tops, darker folds and wispy edges, and thickens until it covers the frame; as it thins out and drifts away, the incoming image shows through (gl-transitions) |
| `gl-SnakeBlockWipe` | 0.8s | Blocks switch to the incoming image one at a time, row after row from the top (or column after column from the left), each line running the opposite way to the one before, like a snake winding across the frame (gl-transitions) |
| `gl-Snapshot` | 0.8s | A camera flash freezes the outgoing image into a printed photo with a white border, which shrinks, tilts and drops out of the frame, revealing the incoming image behind it (gl-transitions) |
| `gl-Sphere` | 0.8s | The outgoing image wraps itself onto a shaded ball that shrinks and rolls away, revealing the incoming image under its shadow (gl-transitions) |
| `gl-SpiralBlockWipe` | 0.8s | Square blocks switch to the incoming image one after another along a rectangular spiral, from the border inward or from the center outward (gl-transitions) |
| `gl-SpiralWipe` | 0.8s | A spiral arm winds out from the center and widens to reveal the incoming image (gl-transitions) |
| `gl-SplatterWipe` | 0.8s | Splats of paint land one after another, each popping in with a spiky outline, flung droplets and a few drips running down, revealing the incoming image until they cover the frame (gl-transitions) |
| `gl-SplitFlap` | 0.8s | The frame becomes a split-flap board: in each cell the top half of the outgoing image flips down on a hinge across the middle, cell after cell, its back bringing the bottom half of the incoming image (gl-transitions) |
| `gl-SplitSlideInHorizontal` | 0.8s | The incoming image slides in as two halves moving horizontally in opposite directions (gl-transitions) |
| `gl-SplitSlideInOutHorizontal` | 0.8s | The halves of both images slide horizontally in opposite directions, out and in at once (gl-transitions) |
| `gl-SplitSlideInOutVertical` | 0.8s | The halves of both images slide vertically in opposite directions, out and in at once (gl-transitions) |
| `gl-SplitSlideInVertical` | 0.8s | The incoming image slides in as two halves moving vertically in opposite directions (gl-transitions) |
| `gl-SplitSlideOutHorizontal` | 0.8s | The outgoing image slides out as two halves moving horizontally in opposite directions (gl-transitions) |
| `gl-SplitSlideOutVertical` | 0.8s | The outgoing image slides out as two halves moving vertically in opposite directions (gl-transitions) |
| `gl-SpotlightWipe` | 0.8s | The stage lights go down on the outgoing image and a soft oval spotlight searches across it along a curved path, comes to rest and lights the incoming image inside it, then widens until the stage lights come back up on the incoming image (gl-transitions) |
| `gl-SquaresWipe` | 0.8s | Squares grow along a diagonal sweep to reveal the incoming image (gl-transitions) |
| `gl-Squeeze` | 0.8s | The outgoing image is squeezed into a line with color separation, revealing the incoming one (gl-transitions) |
| `gl-StarWipe` | 0.8s | A growing star reveals the incoming image (gl-transitions) |
| `gl-StaticFade` | 0.8s | Cuts to the incoming image halfway, hidden behind a burst of TV static (gl-transitions) |
| `gl-StaticWipe` | 0.8s | A wipe from top to bottom with a band of TV static at its edge (gl-transitions) |
| `gl-StereoViewer` | 0.8s | Both images shrink into rounded cards that swap, like a stereo viewer toy (gl-transitions) |
| `gl-StretchSlide` | 0.8s | The outgoing image stretches out long as it shoots away to one side, pulling in the incoming one squashed behind it, which overshoots and springs back to its shape (gl-transitions) |
| `gl-StripDatamoshGlitch` | 0.8s | A datamosh glitch: torn strips, chroma shifts and scan noise drag the outgoing image into the incoming one (gl-transitions) |
| `gl-Swap` | 0.8s | The two images swap places in 3D, with a floor reflection (gl-transitions) |
| `gl-TangentMotionBlur` | 0.8s | The outgoing image is flung away along a curve with motion blur (gl-transitions) |
| `gl-TilesWave` | 0.8s | The incoming image is revealed tile by tile in a diagonal wave (gl-transitions) |
| `gl-TopBottom` | 0.8s | The outgoing image shrinks away upward while the incoming one slides in from the bottom (gl-transitions) |
| `gl-TruchetWipe` | 0.8s | A grid of square tiles, each holding two quarter-circle arcs, links into long winding paths; starting from the middle and spreading outward, the paths are drawn as thin lines of the incoming image, then thicken into bands with a dark outline and a soft shadow until they merge over the whole frame (gl-transitions) |
| `gl-Tumble` | 0.8s | The outgoing image is thrown away like a rigid card, tumbling end over end with a slight spin as it flies off into the distance in perspective, its darker back showing on every flip and its soft shadow shrinking on the incoming image behind it (gl-transitions) |
| `gl-Tunnel` | 0.8s | The camera flies down a tunnel lined with the outgoing image toward the incoming one, which opens at its far end and grows to fill the frame (gl-transitions) |
| `gl-TvLostSignal` | 0.8s | A crossfade with drifting tracking lines and tearing, like a TV losing its signal (gl-transitions) |
| `gl-TvRoll` | 0.8s | The outgoing image rolls faster and faster, like an old TV losing its vertical hold, then the roll slows down and locks on the incoming image (gl-transitions) |
| `gl-TvStatic` | 0.8s | Cuts to full-screen TV static, then to the incoming image (gl-transitions) |
| `gl-TvTurnOff` | 0.8s | The outgoing image collapses into a glowing line and a dot, like an old TV turned off, then the incoming image powers on from the dot (gl-transitions) |
| `gl-UndulatingBurnOut` | 0.8s | A circle with a wavy edge burns out from the center to reveal the incoming image (gl-transitions) |
| `gl-VerticalClose` | 0.8s | The incoming image closes in from the left and right edges toward the middle (gl-transitions) |
| `gl-VerticalOpen` | 0.8s | The incoming image opens from a line in the middle toward the left and right edges (gl-transitions) |
| `gl-VhsTracking` | 0.8s | Tape-tracking bands of white snow roll down the frame, tearing the lines around them, with smeared color, wobbling lines, a jittering strip at the bottom and a dropout flash, as the incoming image is recorded over the outgoing one under the densest band (gl-transitions) |
| `gl-Vortex` | 0.8s | The outgoing image breaks into hundreds of small squares that a tornado carries away along a spiral around the center, from the eye outward, uncovering the incoming image (gl-transitions) |
| `gl-WarpSpeed` | 0.8s | The camera jumps to light speed: star streaks shoot out from the center and stretch longer and longer while the outgoing image is pulled into a radial smear, then after a flash the incoming image emerges from the center as the streaks shrink back (gl-transitions) |
| `gl-WaterDrop` | 0.8s | A drop falls into the image like into still water: round ripples spread out from where it hits, bending the image with glints on their slopes, the incoming image shows up inside the leading ripple, and the water calms down (gl-transitions) |
| `gl-WaveWipe` | 0.8s | A breaking wave crashes across the frame, its lip curling over in front of its face and throwing foam and spray ahead, its shadow darkening the outgoing image; the incoming image is left behind it, tinted and bent by the water, clearing as the wave passes (gl-transitions) |
| `gl-WedgeWipe` | 0.8s | Two hands sweep away from each other around the center, opening a widening wedge that reveals the incoming image (gl-transitions) |
| `gl-WhipSpin` | 0.8s | The camera rolls faster and faster around the center of the frame, streaking the outgoing image in a spin blur, then the incoming one takes over mid-spin and slows to a stop (gl-transitions) |
| `gl-Wind` | 0.8s | A ragged left-to-right wipe, as if the image was blown away by the wind (gl-transitions) |
| `gl-WindowSlices` | 0.8s | The incoming image appears through vertical slices that widen (gl-transitions) |
| `gl-ZoomInCircles` | 0.8s | Concentric rings of the outgoing image zoom at different speeds before revealing the incoming one (gl-transitions) |
| `gl-ZoomWipeLeft` | 0.8s | Zooms into the outgoing image, then the incoming one wipes in from right to left (gl-transitions) |
| `gl-ZoomWipeRight` | 0.8s | Zooms into the outgoing image, then the incoming one wipes in from left to right (gl-transitions) |

## Hiệu ứng chữ (`texts[].anim`, mặc định theo phong cách)
| Tên | Mô tả |
|---|---|
| `rise` | Từng từ trượt lên, mờ → rõ |
| `mask` | Từng dòng trồi lên từ sau mép (sang trọng) |
| `blur` | Từng từ hiện từ mờ nhòe, không di chuyển (tối giản) |
| `pop` | Từng dòng phóng nhẹ 118% → 100% (hook) |
| `track` | Chữ giãn rộng rồi thu về (tiêu đề sang trọng) |
| `type` | Gõ từng ký tự (phân tích, tin nhanh) |
| `zoom-blur` | Cả dòng lao vào từ to và mờ → đúng cỡ và rõ (mẫu edit-phim-01) |
| `word-pop` | Từng từ bật ra nảy nhẹ theo nhịp nói |

## Khối chữ (`texts[].kind`)
| Tên | Trường bắt buộc | Mô tả |
|---|---|---|
| `hook` | tag, lines | Mở đầu: thẻ nhãn + câu lớn |
| `section` | num, title, lines | Mục số viền + tiêu đề có thanh nhấn |
| `line` | lines | Một hai dòng chữ lớn |
| `outro` | lines | Cảnh kết thương hiệu (có thể thêm 'note') |
| `lower` | title | Thanh tiêu đề dưới màn hình (thêm 'sub' cho dòng phụ) |
| `quote` | lines | Câu trích lớn có dấu ngoặc (thêm 'by' cho người nói) |
| `source` | text | Thẻ nguồn nhỏ, bắt buộc khi có số liệu: 'Nguồn: …, cập nhật …' |
| `checklist` | items | Danh sách kiểm, từng mục hiện dần có dấu ✓ (thêm 'title') |
| `stat` | value, label | Số lớn chạy từ 0 (thêm 'prefix', 'suffix', 'decimals') |
| `title3d` | big | Chữ lớn giữa khung: nhãn nhỏ trên ('top') + chữ lớn + dòng nhỏ dưới ('sub'); kiểu chữ và cách hiện theo phong cách |
| `compare` | a_label, a_value, b_label, b_value | Thẻ so sánh 2 cột (vd. Thuê nhà vs Trả góp), thêm 'title', 'note' |
