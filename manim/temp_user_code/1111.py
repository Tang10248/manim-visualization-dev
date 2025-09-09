
# 画一个圆，然后移动它
from manim import *

class UserScene(Scene):
  def construct(self):
    circle = Circle(color=BLUE, radius=2)
    self.play(Create(circle))
    self.wait(1)
    self.play(circle.animate.shift(RIGHT * 3))
    self.wait(1)

# 渲染场景
scene = UserScene()
scene.render()
    