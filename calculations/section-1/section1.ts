export type Section1Input = {
  pipeSizeMm: number;
  steelGrade: "ST37" | "ST52" | "X42" | "X52" | "X60" | "X65" | "X70";
  coilWidthMm: number;
  thicknessMm: number;
  standardPipeLengthMm: number;
  maxTDistanceMm: number;
  projectNumber: string;
  firstPipeNumber: string;
  totalFirstLastCoilCutMm: number;
};

export type Section1Result = {
  meanDiameterMm: number;
  circumferenceMm: number;
  helixAngleToLengthDeg: number;
  helixAngleToWidthDeg: number;
  pitchMm: number;
  pitchesPerStandardPipe: number;
};

function assertPositive(name: string, value: number): void {
  if (!Number.isFinite(value) || value <= 0) {
    throw new Error(`${name} must be a positive finite number.`);
  }
}

/**
 * Section 1 calculation engine.
 *
 * Definitions used by the production model:
 * - mean diameter = pipe outside diameter - sheet thickness
 * - helix angle to pipe length is measured from the longitudinal axis
 * - helix angle to sheet width is its complementary angle
 * - pitch is the axial distance between consecutive spiral welds
 * - no application-level rounding is performed
 */
export function calculateSection1(input: Section1Input): Section1Result {
  assertPositive("Pipe size", input.pipeSizeMm);
  assertPositive("Coil width", input.coilWidthMm);
  assertPositive("Thickness", input.thicknessMm);
  assertPositive("Standard pipe length", input.standardPipeLengthMm);
  assertPositive("Maximum T distance", input.maxTDistanceMm);
  if (input.pipeSizeMm <= input.thicknessMm) {
    throw new Error("Pipe size must be greater than sheet thickness.");
  }

  const meanDiameterMm = input.pipeSizeMm - input.thicknessMm;
  const circumferenceMm = Math.PI * meanDiameterMm;

  if (input.coilWidthMm >= circumferenceMm) {
    throw new Error("Coil width must be smaller than the pipe mean circumference for this spiral geometry.");
  }

  const helixAngleToLengthRad = Math.acos(input.coilWidthMm / circumferenceMm);
  const helixAngleToLengthDeg = helixAngleToLengthRad * (180 / Math.PI);
  const helixAngleToWidthDeg = 90 - helixAngleToLengthDeg;

  const pitchMm = input.coilWidthMm / Math.sin(helixAngleToLengthRad);
  const pitchesPerStandardPipe = input.standardPipeLengthMm / pitchMm;

  return {
    meanDiameterMm,
    circumferenceMm,
    helixAngleToLengthDeg,
    helixAngleToWidthDeg,
    pitchMm,
    pitchesPerStandardPipe,
  };
}
