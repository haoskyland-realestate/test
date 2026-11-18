import sys
H = 'D:/AutoEdit/work/demo1/hf/'
s = open('D:/AutoEdit/work/demo1/src.html', encoding='utf-8').read()
CHK = '<svg viewBox="0 0 60 60" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 31l10 10 19-21"/></svg>'
s = s.replace('CHK', CHK)

# nhạc nền + sound effect (nhẹ, theo lúc thẻ/nhãn bật lên)
NL = '\n  '
audio = '<audio id="music" class="clip" data-start="0" data-duration="17.4" data-volume="0.055" data-fade-in="0.8" data-fade-out="1.6" data-track-index="2" src="assets/music.mp3"></audio>' + NL
notif = [0.10, 1.10, 4.50, 4.95, 5.40, 5.85, 7.40, 7.70, 8.80, 9.76, 10.95, 11.51, 11.77, 12.04, 12.30, 13.15, 13.40]
for i, t in enumerate(notif):
    audio += '<audio id="sfx%d" class="clip" data-start="%.2f" data-volume="0.30" data-track-index="3" src="assets/sfx_notif.mp3"></audio>' % (i + 1, t) + NL
audio += '<audio id="sfxm1" class="clip" data-start="14.90" data-volume="0.22" data-track-index="3" src="assets/sfx_metal.mp3"></audio>'
s = s.replace('<!--AUDIO-->', audio)

guides = ''
if len(sys.argv) > 1 and sys.argv[1] == 'guides':
    guides = '''<div id="guides">
    <div class="z" style="left:0;top:0;width:1080px;height:288px">TikTok / Reels che — 15% TRÊN</div>
    <div class="z" style="left:0;top:1440px;width:1080px;height:480px">TikTok / Reels che — 25% DƯỚI (tên, mô tả, nhạc)</div>
    <div class="z" style="left:972px;top:760px;width:108px;height:680px">NÚT<br>THẢ TIM<br>/ BÌNH LUẬN</div>
    <div class="ok"><b>VÙNG AN TOÀN</b></div>
  </div>'''
s = s.replace('<!--GUIDES-->', guides)
open(H + 'index.html', 'w', encoding='utf-8').write(s)
print('built', 'guides' if guides else 'clean')
