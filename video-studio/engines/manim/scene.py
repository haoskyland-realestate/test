"""Manim: biểu đồ/số liệu động. Đọc spec JSON qua biến môi trường SPEC.
Chạy: SPEC=videos/demo.json manim -qm engines/manim/scene.py Main
"""
import json, os
from manim import Scene, Text, VGroup, Write, FadeIn, DOWN, UP

class Main(Scene):
    def construct(self):
        spec = json.load(open(os.environ["SPEC"], encoding="utf8"))
        hook = Text(spec["hook"], font_size=32).to_edge(UP)
        items = VGroup(*[Text("• " + b, font_size=28) for b in spec["bullets"]]).arrange(DOWN, aligned_edge=None, buff=0.5)
        self.play(Write(hook))
        for it in items:
            self.play(FadeIn(it, shift=DOWN * 0.3))
        self.wait(1)
