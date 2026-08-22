export type Section2CoilInput = {
  coilNumber: string;
  coilWeightKg: number;
  firstCutMm: number;
  lastCutMm: number;
  outOfPlanCutMm: number;
  actualTDistanceMm: number;
};

export type Section2Input = {
  pipeSizeMm: number;
  coilWidthMm: number;
  thicknessMm: number;
  standardPipeLengthMm: number;
  pitchMm: number;
  totalFirstLastCoilCutMm: number;
  coils: Section2CoilInput[];
};

export type Section2CoilResult = {
  coilNumber: string;
  coilWeightKg: number;
  calculatedWasteKg: number;
  note: string;
};

export type Section2Result = {
  coils: Section2CoilResult[];
  totalWasteKg: number;
};

function positive(name: string, value: number): void {
  if (!Number.isFinite(value) || value < 0) throw new Error(`${name} مقدار معتبر ندارد.`);
}

/**
 * Section 2 calculation engine.
 *
 * This module intentionally contains no rounding and does not modify Section 1.
 * T belongs to the pipe; its effect on coil waste is handled here only after
 * the production/T relation is supplied by the production data.
 *
 * The exact conversion from an observed T position to the corresponding coil
 * weight is kept isolated until the production relation is finalized, rather
 * than being guessed here.
 */
export function calculateSection2(input: Section2Input): Section2Result {
  positive("Pipe size", input.pipeSizeMm);
  positive("Coil width", input.coilWidthMm);
  positive("Thickness", input.thicknessMm);
  positive("Standard pipe length", input.standardPipeLengthMm);
  positive("Pitch", input.pitchMm);

  const coils = input.coils.map((coil) => {
    positive("Coil weight", coil.coilWeightKg);
    positive("First cut", coil.firstCutMm);
    positive("Last cut", coil.lastCutMm);
    positive("Out-of-plan cut", coil.outOfPlanCutMm);
    positive("Actual T distance", coil.actualTDistanceMm);

    return {
      coilNumber: coil.coilNumber,
      coilWeightKg: coil.coilWeightKg,
      calculatedWasteKg: 0,
      note: "محاسبه وزن متناظر با موقعیت واقعی T پس از نهایی‌شدن رابطه تولید تکمیل می‌شود.",
    };
  });

  return {
    coils,
    totalWasteKg: coils.reduce((sum, coil) => sum + coil.calculatedWasteKg, 0),
  };
}
