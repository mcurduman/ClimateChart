import React from "react";
import {
  LineChart, Line, BarChart, Bar, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from "recharts";

interface WeatherChartDisplayProps {
  chartType: "line" | "bar" | "area";
  data: any[];
  chartKey: string;
  showGrid: boolean;
  showDots: boolean;
  smoothCurve: boolean;
  animate: boolean;
  characteristics: string[];
  characteristicConfig: Record<string, { label: string; unit: string; color: string }>;
  getYAxisId: (char: string) => string;
  needsDualAxis: boolean;
  getFirstUnit: () => string;
  getSecondUnit: () => string;
  commonXAxisProps: any;
  commonTooltip: React.ReactNode;
  todayXKey?: string;
}

const WeatherChartDisplay: React.FC<WeatherChartDisplayProps> = ({
  chartType,
  data,
  chartKey,
  showGrid,
  showDots,
  smoothCurve,
  animate,
  characteristics,
  characteristicConfig,
  getYAxisId,
  needsDualAxis,
  getFirstUnit,
  getSecondUnit,
  commonXAxisProps,
  commonTooltip,
  todayXKey,
}) => {
  if (chartType === "line") {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <LineChart key={chartKey} data={data}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />}
          <XAxis {...commonXAxisProps} />
          <YAxis
            yAxisId="left"
            className="text-xs"
            tick={{ fill: "hsl(var(--foreground))" }}
            label={{ value: getFirstUnit(), angle: -90, position: "insideLeft", style: { fill: "hsl(var(--foreground))" } }}
          />
          {needsDualAxis && (
            <YAxis
              yAxisId="right"
              orientation="right"
              className="text-xs"
              tick={{ fill: "hsl(var(--foreground))" }}
              label={{ value: getSecondUnit(), angle: 90, position: "insideRight", style: { fill: "hsl(var(--foreground))" } }}
            />
          )}
          {todayXKey && (
            <ReferenceLine
              x={todayXKey}
              stroke="#f59e42"
              strokeWidth={3}
              strokeDasharray="6 2"
              label={{ value: "Today", position: "top", fill: "#f59e42", fontWeight: "bold", fontSize: 14 }}
            />
          )}
          {commonTooltip}
          <Legend />
          {characteristics.map((char) => (
            <Line
              key={char}
              yAxisId={getYAxisId(char)}
              type={smoothCurve ? "monotone" : "linear"}
              dataKey={char}
              stroke={characteristicConfig[char].color}
              strokeWidth={2}
              dot={showDots ? { r: 2 } : false}
              name={characteristicConfig[char].label}
              connectNulls
              isAnimationActive={animate}
              animationDuration={600}
              animationEasing="ease-in-out"
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    );
  }
  if (chartType === "bar") {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <BarChart key={chartKey} data={data}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />}
          <XAxis {...commonXAxisProps} />
          <YAxis
            yAxisId="left"
            className="text-xs"
            tick={{ fill: "hsl(var(--foreground))" }}
            label={{ value: getFirstUnit(), angle: -90, position: "insideLeft", style: { fill: "hsl(var(--foreground))" } }}
          />
          {needsDualAxis && (
            <YAxis
              yAxisId="right"
              orientation="right"
              className="text-xs"
              tick={{ fill: "hsl(var(--foreground))" }}
              label={{ value: getSecondUnit(), angle: 90, position: "insideRight", style: { fill: "hsl(var(--foreground))" } }}
            />
          )}
          {todayXKey && (
            <ReferenceLine
              x={todayXKey}
              stroke="#f59e42"
              strokeWidth={3}
              strokeDasharray="6 2"
              label={{ value: "Today", position: "top", fill: "#f59e42", fontWeight: "bold", fontSize: 14 }}
            />
          )}
          {commonTooltip}
          <Legend />
          {characteristics.map((char) => (
            <Bar
              key={char}
              yAxisId={getYAxisId(char)}
              dataKey={char}
              fill={characteristicConfig[char].color}
              name={characteristicConfig[char].label}
              isAnimationActive={animate}
              animationDuration={600}
              animationEasing="ease-in-out"
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    );
  }
  if (chartType === "area") {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart key={chartKey} data={data}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />}
          <XAxis {...commonXAxisProps} />
          <YAxis
            yAxisId="left"
            className="text-xs"
            tick={{ fill: "hsl(var(--foreground))" }}
            label={{ value: getFirstUnit(), angle: -90, position: "insideLeft", style: { fill: "hsl(var(--foreground))" } }}
          />
          {needsDualAxis && (
            <YAxis
              yAxisId="right"
              orientation="right"
              className="text-xs"
              tick={{ fill: "hsl(var(--foreground))" }}
              label={{ value: getSecondUnit(), angle: 90, position: "insideRight", style: { fill: "hsl(var(--foreground))" } }}
            />
          )}
          {todayXKey && (
            <ReferenceLine
              x={todayXKey}
              stroke="#f59e42"
              strokeWidth={3}
              strokeDasharray="6 2"
              label={{ value: "Today", position: "top", fill: "#f59e42", fontWeight: "bold", fontSize: 14 }}
            />
          )}
          {commonTooltip}
          <Legend />
          {characteristics.map((char) => (
            <Area
              key={char}
              yAxisId={getYAxisId(char)}
              type={smoothCurve ? "monotone" : "linear"}
              dataKey={char}
              fill={characteristicConfig[char].color}
              stroke={characteristicConfig[char].color}
              fillOpacity={0.4}
              name={characteristicConfig[char].label}
              connectNulls
              isAnimationActive={animate}
              animationDuration={600}
              animationEasing="ease-in-out"
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    );
  }
  return null;
};

export default WeatherChartDisplay;
