"use client";

import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
  ResponsiveContainer,
  CartesianGrid,
  Tooltip,
} from "recharts";

const COLORS = ["#ffffff", "#888888", "#4d9fff", "#ff8a4d", "#7dff8a"];

export default function ConceptScatterChart({ points = [], categories = [] }) {
  if (!points.length) return null;

  const grouped = categories.map((category, index) => ({
    category,
    color: COLORS[index % COLORS.length],
    data: points.filter((p) => p.category === category),
  }));

  return (
    <div className="chart-wrap" style={{ padding: 0, height: 360 }}>
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
          <CartesianGrid stroke="#222222" />

          <XAxis type="number" dataKey="x" stroke="#ffffff" axisLine={{ stroke: "#777777" }} />
          <YAxis type="number" dataKey="y" stroke="#ffffff" axisLine={{ stroke: "#777777" }} />
          <ZAxis range={[60, 60]} />

          <Tooltip
            cursor={{ strokeDasharray: "3 3" }}
            contentStyle={{ background: "#111111", border: "1px solid #333333" }}
            labelStyle={{ color: "#ffffff" }}
            formatter={(value, name, props) => {
              if (name === "x" || name === "y") return null;
              return value;
            }}
            content={({ active, payload }) => {
              if (!active || !payload || !payload.length) return null;
              const point = payload[0].payload;
              return (
                <div style={{ background: "#111111", border: "1px solid #333333", padding: 10, maxWidth: 260 }}>
                  <div style={{ color: "#999", fontSize: 10, letterSpacing: 1, marginBottom: 4 }}>
                    {point.category}
                  </div>
                  <div style={{ color: "#fff", fontSize: 12 }}>{point.title}</div>
                </div>
              );
            }}
          />

          {grouped.map((group) => (
            <Scatter
              key={group.category}
              name={group.category}
              data={group.data}
              fill={group.color}
            />
          ))}
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}