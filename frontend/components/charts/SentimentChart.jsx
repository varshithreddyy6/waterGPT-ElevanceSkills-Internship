"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const DEFAULT_VALUES = [60, 74, 65, 84, 58, 34, 61];
const LABELS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"];

export default function SentimentChart({ data = DEFAULT_VALUES }) {
  const rows = data.map((value, index) => ({
    name: LABELS[index],
    value,
  }));

  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rows}>
          <CartesianGrid vertical={false} stroke="#000000" />

          <XAxis
            dataKey="name"
            stroke="#ffffff"
            tickLine={false}
            axisLine={{ stroke: "#777777" }}
          />

          <YAxis
            domain={[0, 100]}
            ticks={[0, 25, 50, 75, 100]}
            tickFormatter={(value) => `${value}%`}
            stroke="#ffffff"
            axisLine={{ stroke: "#777777" }}
          />

          <Line
            type="monotone"
            dataKey="value"
            stroke="#ffffff"
            strokeWidth={1.5}
            dot={{
              fill: "#ffffff",
              r: 4,
            }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}