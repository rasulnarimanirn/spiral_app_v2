from dataclasses import dataclass
import math

@dataclass
class PipeSpecifications:
    """ساختار داده‌های پایه و محاسبات هندسی محض لوله اسپیرال"""
    outer_diameter: float
    wall_thickness: float
    strip_width: float
    standard_length: float
    t_joint_limit: float
    default_lead_crop: float = 400.0
    default_tail_crop: float = 300.0
    steel_density: float = 7.85e-6

    @property
    def mean_diameter(self) -> float:
        return self.outer_diameter - self.wall_thickness

    @property
    def perimeter(self) -> float:
        return math.pi * self.mean_diameter

    @property
    def sin_alpha(self) -> float:
        return self.strip_width / self.perimeter

    @property
    def helix_angle_deg(self) -> float:
        return math.degrees(math.asin(self.sin_alpha))

    @property
    def weld_pitch(self) -> float:
        return self.strip_width / math.cos(math.asin(self.sin_alpha))

    def pipe_length_to_strip_length(self, pipe_length_mm: float) -> float:
        return pipe_length_mm / self.sin_alpha

    def strip_length_to_pipe_length(self, strip_length_mm: float) -> float:
        return strip_length_mm * self.sin_alpha
