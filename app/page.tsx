"use client";

import { FormEvent, useState } from "react";
import { calculateSection1, Section1Result } from "@/calculations/section-1/section1";

type FormState = {
  pipeSizeMm: string;
  steelGrade: "ST37" | "ST52" | "X42" | "X52" | "X60" | "X65" | "X70";
  coilWidthMm: string;
  thicknessMm: string;
  standardPipeLengthMm: string;
  maxTDistanceMm: string;
  projectNumber: string;
  firstPipeNumber: string;
  totalFirstLastCoilCutMm: string;
};

const initialForm: FormState = {
  pipeSizeMm: "",
  steelGrade: "ST37",
  coilWidthMm: "",
  thicknessMm: "",
  standardPipeLengthMm: "",
  maxTDistanceMm: "",
  projectNumber: "",
  firstPipeNumber: "",
  totalFirstLastCoilCutMm: "",
};

function numberValue(value: string, name: string): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) throw new Error(`${name} مقدار معتبر ندارد.`);
  return parsed;
}

function display(value: number): string {
  return String(value);
}

export default function Home() {
  const [form, setForm] = useState<FormState>(initialForm);
  const [result, setResult] = useState<Section1Result | null>(null);
  const [error, setError] = useState("");

  const update = (key: keyof FormState, value: string) => {
    setForm((current) => ({ ...current, [key]: value }));
  };

  const calculate = (event: FormEvent) => {
    event.preventDefault();
    setError("");
    try {
      setResult(calculateSection1({
        pipeSizeMm: numberValue(form.pipeSizeMm, "سایز لوله"),
        steelGrade: form.steelGrade,
        coilWidthMm: numberValue(form.coilWidthMm, "عرض کلاف"),
        thicknessMm: numberValue(form.thicknessMm, "ضخامت ورق"),
        standardPipeLengthMm: numberValue(form.standardPipeLengthMm, "استاندارد طول لوله"),
        maxTDistanceMm: numberValue(form.maxTDistanceMm, "حد مجاز فاصله T"),
        projectNumber: form.projectNumber,
        firstPipeNumber: form.firstPipeNumber,
        totalFirstLastCoilCutMm: numberValue(form.totalFirstLastCoilCutMm, "جمع برش اول و آخر کلاف"),
      }));
    } catch (e) {
      setResult(null);
      setError(e instanceof Error ? e.message : "خطای نامشخص");
    }
  };

  const fields: Array<[keyof FormState, string, string]> = [
    ["pipeSizeMm", "سایز لوله (mm)", "number"],
    ["coilWidthMm", "عرض کلاف (mm)", "number"],
    ["thicknessMm", "ضخامت ورق (mm)", "number"],
    ["standardPipeLengthMm", "استاندارد طول لوله (mm)", "number"],
    ["maxTDistanceMm", "حد مجاز فاصله T (mm)", "number"],
    ["totalFirstLastCoilCutMm", "جمع برش اول و آخر کلاف (mm)", "number"],
    ["projectNumber", "شماره پروژه", "text"],
    ["firstPipeNumber", "شماره اولین لوله", "text"],
  ];

  return (
    <main className="page">
      <div className="container">
        <header className="header">
          <div className="eyebrow">SPIRAL PIPE • SECTION 01</div>
          <h1>محاسبات پایه تولید لوله اسپیرال</h1>
        </header>

        <section className="card">
          <form onSubmit={calculate}>
            <div className="grid">
              {fields.slice(0, 3).map(([key, label, type]) => (
                <div className="field" key={key}>
                  <label htmlFor={key}>{label}</label>
                  <input id={key} type={type} step="any" value={form[key]} onChange={(e) => update(key, e.target.value)} />
                </div>
              ))}

              <div className="field">
                <label htmlFor="steelGrade">گرید ورق</label>
                <select id="steelGrade" value={form.steelGrade} onChange={(e) => update("steelGrade", e.target.value)}>
                  {['ST37', 'ST52', 'X42', 'X52', 'X60', 'X65', 'X70'].map((grade) => <option key={grade}>{grade}</option>)}
                </select>
              </div>

              {fields.slice(3).map(([key, label, type]) => (
                <div className="field" key={key}>
                  <label htmlFor={key}>{label}</label>
                  <input id={key} type={type} step="any" value={form[key]} onChange={(e) => update(key, e.target.value)} />
                </div>
              ))}
            </div>

            <div className="actions">
              <button className="primary" type="submit">محاسبه</button>
              <button className="secondary" type="button" onClick={() => { setForm(initialForm); setResult(null); setError(""); }}>پاک کردن</button>
            </div>
          </form>

          {error && <div className="error">{error}</div>}

          {result && (
            <div className="results">
              <div className="result-grid">
                <div className="result"><div className="label">زاویه هلیکس نسبت به عرض</div><div className="value">{display(result.helixAngleToWidthDeg)}°</div></div>
                <div className="result"><div className="label">زاویه هلیکس نسبت به طول</div><div className="value">{display(result.helixAngleToLengthDeg)}°</div></div>
                <div className="result"><div className="label">پیرامون لوله</div><div className="value">{display(result.circumferenceMm)} mm</div></div>
                <div className="result"><div className="label">مقدار یک گام لوله</div><div className="value">{display(result.pitchMm)} mm</div></div>
                <div className="result"><div className="label">تعداد گام در طول استاندارد</div><div className="value">{display(result.pitchesPerStandardPipe)}</div></div>
              </div>
              <div className="note">محاسبات بدون گرد کردن در لایه کاربرد انجام می‌شوند. مقدار «جمع برش اول و آخر کلاف» ورودی دستی است و در این بخش فرمول ندارد.</div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
