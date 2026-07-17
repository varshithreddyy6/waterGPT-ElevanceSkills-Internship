"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  CartesianGrid,
  Tooltip,
} from "recharts";

export default function KeywordBarChart({ data = [] }) {
  if (!data.length) return null;

  const top = data.slice(0, 12);

  return (
    <div className="chart-wrap" style={{ padding: 0, height: 320 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={top} layout="vertical" margin={{ left: 40 }}>
          <CartesianGrid horizontal={false} stroke="#222222" />

          <XAxis type="number" stroke="#ffffff" axisLine={{ stroke: "#777777" }} />

          <YAxis
            type="category"
            dataKey="term"
            stroke="#ffffff"
            width={110}
            tickLine={false}
            axisLine={{ stroke: "#777777" }}
          />

          <Tooltip
            contentStyle={{ background: "#111111", border: "1px solid #333333" }}
            labelStyle={{ color: "#ffffff" }}
          />

          <Bar dataKey="score" fill="#ffffff" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}