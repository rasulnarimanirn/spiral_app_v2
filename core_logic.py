from dataclasses import dataclass, field
import math
from typing import Dict

@dataclass
class PipeSpecifications:
    """ساختار داده‌های پایه و محاسبات هندسی محض لوله اسپیرال"""
    outer_diameter: float  # D (mm)
    wall_thickness: float  # t (mm)
    strip_width: float     # W (mm)
    standard_length: float # L (mm)
    t_joint_limit: float   # Limit (mm)
    steel_density: float = 7.85e-6  # kg/mm^3

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


@dataclass
class ProductionLine:
    """مدیریت وضعیت یک خط تولید مجزا"""
    line_name: str
    specs: PipeSpecifications


@dataclass
class FactoryManager:
    """مدیریت هوشمند و بدون تداخل ۳ خط تولید کارخانه"""
    lines: Dict[str, ProductionLine] = field(default_factory=dict)

    def update_or_create_line(self, line_name: str, specs: PipeSpecifications):
        """ثبت یا به‌روزرسانی مشخصات یک خط بدون اثرگذاری روی سایر خطوط"""
        self.lines[line_name] = ProductionLine(line_name=line_name, specs=specs)

    def get_line(self, line_name: str) -> ProductionLine:
        """فراخوانی داده‌های خط انتخابی"""
        return self.lines.get(line_name)
