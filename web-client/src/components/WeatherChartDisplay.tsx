import React from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

const TodayReferenceLabel = ({ viewBox }: { viewBox?: { x?: number; y?: number } }) => {
  const x = viewBox?.x ?? null;
  const y = viewBox?.y ?? null;
  if (x == null || y == null) return null;
  return (
    <g transform={`translate(${x},${y})`}>
      <g transform="translate(0,-28)">
        <rect x={-28} y={-18} width={56} height={20} rx={6} fill="#f59e42" />
        <text x={0} y={-4} textAnchor="middle" fill="#fff" fontWeight={700} fontSize={12}>
          Today
        </text>
        <path d="M 0 0 L 6 -8 L -6 -8 Z" fill="#f59e42" />
      </g>
    </g>
  );
};

const TodayTick: React.FC<any> = ({ x, y, payload, todayKey, fmt }) => {
  const isToday = payload?.value === todayKey;
  return (
    <g transform={`translate(${x},${y})`}>
      <text
        dy={16}
        textAnchor="middle"
        fontSize={12}
        fontWeight={isToday ? 700 : 400}
        fill={isToday ? "#f59e42" : "currentColor"}
      >
        {fmt(payload.value)}
      </text>
      {isToday && <circle cx={0} cy={6} r={3} fill="#f59e42" />}
    </g>
  );
};

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
          <XAxis
            {...commonXAxisProps}
            type="category"
            tick={
              <TodayTick
                todayKey={todayXKey}
                fmt={(iso: string) => commonXAxisProps.tickFormatter(iso)}
              />
            }
          />
          <YAxis
            yAxisId="left"
            className="text-xs"
            tick={{ fill: "hsl(var(--foreground))" }}
            label={{
              value: getFirstUnit(),
              angle: -90,
              position: "insideLeft",
              style: { fill: "hsl(var(--foreground))" },
            }}
          />
          {needsDualAxis && (
            <YAxis
              yAxisId="right"
              orientation="right"
              className="text-xs"
              tick={{ fill: "hsl(var(--foreground))" }}
              label={{
                value: getSecondUnit(),
                angle: 90,
                position: "insideRight",
                style: { fill: "hsl(var(--foreground))" },
              }}
            />
          )}
          {todayXKey && (
            <ReferenceLine
              x={todayXKey}
              stroke="#f59e42"
              strokeWidth={3}
              strokeDasharray="6 2"
              label={<TodayReferenceLabel />}
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
              name={characteristicConfig[char].label}
              connectNulls
              isAnimationActive={animate}
              animationDuration={600}
              animationEasing="ease-in-out"
              dot={(p: any) => {
                const isToday = p?.payload?.xKey === todayXKey;
                if (isToday) {
                  return (
                    <circle
                      cx={p.cx}
                      cy={p.cy}
                      r={5}
                      stroke="#f59e42"
                      strokeWidth={3}
                      fill="#fff"
                    />
                  );
                }
                return showDots ? <circle cx={p.cx} cy={p.cy} r={2} /> : null;
              }}
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
          <XAxis
            {...commonXAxisProps}
            type="category"
            tick={
              <TodayTick
                todayKey={todayXKey}
                fmt={(iso: string) => commonXAxisProps.tickFormatter(iso)}
              />
            }
          />
          <YAxis
            yAxisId="left"
            className="text-xs"
            tick={{ fill: "hsl(var(--foreground))" }}
            label={{
              value: getFirstUnit(),
              angle: -90,
              position: "insideLeft",
              style: { fill: "hsl(var(--foreground))" },
            }}
          />
          {needsDualAxis && (
            <YAxis
              yAxisId="right"
              orientation="right"
              className="text-xs"
              tick={{ fill: "hsl(var(--foreground))" }}
              label={{
                value: getSecondUnit(),
                angle: 90,
                position: "insideRight",
                style: { fill: "hsl(var(--foreground))" },
              }}
            />
          )}
          {todayXKey && (
            <ReferenceLine
              x={todayXKey}
              stroke="#f59e42"
              strokeWidth={3}
              strokeDasharray="6 2"
              label={<TodayReferenceLabel />}
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
          <XAxis
            {...commonXAxisProps}
            type="category"
            tick={
              <TodayTick
                todayKey={todayXKey}
                fmt={(iso: string) => commonXAxisProps.tickFormatter(iso)}
              />
            }
          />
          <YAxis
            yAxisId="left"
            className="text-xs"
            tick={{ fill: "hsl(var(--foreground))" }}
            label={{
              value: getFirstUnit(),
              angle: -90,
              position: "insideLeft",
              style: { fill: "hsl(var(--foreground))" },
            }}
          />
          {needsDualAxis && (
            <YAxis
              yAxisId="right"
              orientation="right"
              className="text-xs"
              tick={{ fill: "hsl(var(--foreground))" }}
              label={{
                value: getSecondUnit(),
                angle: 90,
                position: "insideRight",
                style: { fill: "hsl(var(--foreground))" },
              }}
            />
          )}
          {todayXKey && (
            <ReferenceLine
              x={todayXKey}
              stroke="#f59e42"
              strokeWidth={3}
              strokeDasharray="6 2"
              label={<TodayReferenceLabel />}
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
