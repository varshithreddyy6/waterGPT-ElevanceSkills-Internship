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

export default function CategoryBarChart({ data = [] }) {
  if (!data.length) return null;

  return (
    <div className="chart-wrap" style={{ padding: 0, height: 260 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid vertical={false} stroke="#222222" />

          <XAxis
            dataKey="category"
            stroke="#ffffff"
            tickLine={false}
            axisLine={{ stroke: "#777777" }}
          />

          <YAxis stroke="#ffffff" axisLine={{ stroke: "#777777" }} />

          <Tooltip
            contentStyle={{ background: "#111111", border: "1px solid #333333" }}
            labelStyle={{ color: "#ffffff" }}
          />

          <Bar dataKey="count" fill="#ffffff" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}