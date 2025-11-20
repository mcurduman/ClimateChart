import React, { useState, useRef, useEffect } from "react";
import { Tooltip } from "recharts";
import { Card } from "@/components/ui/card";
import WeatherChartControls from "./WeatherChartControls";
import WeatherChartDisplay from "./WeatherChartDisplay";
import WeatherChartCharacteristics from "./WeatherChartCharacteristics";
import WeatherChartTable from "./WeatherChartTable";

export type ChartRow = {
  xKey: string;
  date: string;
  temperature_2m_max?: number;
  temperature_2m_min?: number;
  precipitation_sum?: number;
  pressure_msl_mean?: number;
  wind_speed_10m_max?: number;
  relative_humidity_2m_max?: number;
};

interface WeatherChartProps {
  data: ChartRow[];
  city: string;
}

const characteristicConfig: Record<string, { label: string; unit: string; color: string }> = {
  temperature_2m_max: { label: "Temperature Max", unit: "°C", color: "#ef4444" },
  temperature_2m_min: { label: "Temperature Min", unit: "°C", color: "#3b82f6" },
  precipitation_sum:   { label: "Precipitation Sum", unit: "mm", color: "#60a5fa" },
  pressure_msl_mean:   { label: "Pressure Mean", unit: "hPa", color: "#a78bfa" },
  wind_speed_10m_max:  { label: "Wind Speed Max", unit: "km/h", color: "#38bdf8" },
  relative_humidity_2m_max: { label: "Humidity Max", unit: "%", color: "#22c55e" },
};

  const todayISO = new Date().toISOString().slice(0, 10);

const fmtLabel = (iso: string) => {
  const [y, m, d] = iso.split("-").map(Number);
  const dt = new Date(y, (m ?? 1) - 1, d ?? 1);
  return dt.toLocaleDateString("en-US", { month: "short", day: "numeric" });
};

const WeatherChart = ({ data, city }: WeatherChartProps) => {
  console.log("WeatherChart xKey values:", data.map(row => row.xKey));
  console.log("WeatherChart todayISO:", todayISO);
  const todayXKey = data.find((row: ChartRow) => row.xKey === todayISO)?.xKey;
  const [chartType, setChartType] = useState<"line" | "bar" | "area">("line");
  const [showGrid, setShowGrid] = useState(true);
  const [showDots, setShowDots] = useState(true);
  const [smoothCurve, setSmoothCurve] = useState(true);
  const [selectedCharacteristics, setSelectedCharacteristics] = useState<string[]>(["temperature_2m_max"]);
  const [isCharacteristicsOpen, setIsCharacteristicsOpen] = useState(true);

  const [isFullscreen, setIsFullscreen] = useState(false);
  const [animate, setAnimate] = useState(true);
  const chartContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleFullscreenChange = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", handleFullscreenChange);
    return () => document.removeEventListener("fullscreenchange", handleFullscreenChange);
  }, []);

  const toggleFullscreen = async () => {
    if (!chartContainerRef.current) return;
    try {
      if (document.fullscreenElement) {
        await document.exitFullscreen();
      } else {
        await chartContainerRef.current.requestFullscreen();
      }
    } catch (error) {
      console.error("Error toggling fullscreen:", error);
    }
  };

  if (!data || data.length === 0) {
    return (
      <Card className="p-6">
        <p className="text-muted-foreground">No weather data available. Please fetch data first.</p>
      </Card>
    );
  }


  const characteristics = selectedCharacteristics;

  const getYAxisId = (char: string) => {
    if (characteristics.length === 1) return "left";
    const units = characteristics.map(c => characteristicConfig[c].unit);
    const uniqueUnits = [...new Set(units)];
    if (uniqueUnits.length === 1) return "left";
    return char === characteristics[0] ? "left" : "right";
  };

  const units = characteristics.map(c => characteristicConfig[c].unit);
  const uniqueUnits = [...new Set(units)];
  const needsDualAxis = uniqueUnits.length > 1;

  const chartTitle =
    characteristics.length === 1
      ? `${characteristicConfig[characteristics[0]]?.label || ""} in ${city} - Last 2 Weeks`
      : `Weather Comparison in ${city} - Last 2 Weeks`;

  const getFirstUnit = () => characteristicConfig[characteristics[0]]?.unit || "";
  const getSecondUnit = () => uniqueUnits[1] || "";

  const commonXAxisProps = {
    dataKey: "xKey" as const,
    allowDuplicatedCategory: false,
    className: "text-xs",
    tick: { fill: "hsl(var(--foreground))" },
    tickFormatter: (iso: string) => fmtLabel(iso),
  };

  const commonTooltip = (
    <Tooltip
      contentStyle={{
        backgroundColor: "hsl(var(--background))",
        border: "1px solid hsl(var(--border))",
        borderRadius: 6,
      }}
      labelStyle={{ color: "hsl(var(--foreground))" }}
      labelFormatter={(iso: string) => fmtLabel(iso)}
      formatter={(val: any, name: string) => {
        const char = Object.keys(characteristicConfig).find(k => characteristicConfig[k].label === name);
        return char ? [`${val}${characteristicConfig[char].unit}`, name] : [val, name];
      }}
    />
  );

  const chartKey = `${chartType}-${city}-${data.length}-${data[0]?.xKey}-${data.at(-1)?.xKey}`;

  return (
    <Card className="p-6">
      <div ref={chartContainerRef} className={isFullscreen ? "bg-background p-6" : ""}>
        <div className="mb-4 space-y-4">
          <h3 className="text-lg font-semibold">{chartTitle}</h3>
          <WeatherChartCharacteristics
            selectedCharacteristics={selectedCharacteristics}
            setSelectedCharacteristics={setSelectedCharacteristics}
            characteristicConfig={characteristicConfig}
            isOpen={isCharacteristicsOpen}
            setIsOpen={setIsCharacteristicsOpen}
          />
          <WeatherChartControls
            chartType={chartType}
            setChartType={setChartType}
            showGrid={showGrid}
            setShowGrid={setShowGrid}
            showDots={showDots}
            setShowDots={setShowDots}
            smoothCurve={smoothCurve}
            setSmoothCurve={setSmoothCurve}
            isFullscreen={isFullscreen}
            toggleFullscreen={toggleFullscreen}
            animate={animate}
            setAnimate={setAnimate}
          />
        </div>
        <WeatherChartDisplay
          chartType={chartType}
          data={data}
          chartKey={chartKey}
          showGrid={showGrid}
          showDots={showDots}
          smoothCurve={smoothCurve}
          animate={animate}
          characteristics={characteristics}
          characteristicConfig={characteristicConfig}
          getYAxisId={getYAxisId}
          needsDualAxis={needsDualAxis}
          getFirstUnit={getFirstUnit}
          getSecondUnit={getSecondUnit}
          commonXAxisProps={commonXAxisProps}
          commonTooltip={commonTooltip}
          todayXKey={todayXKey}
        />
      </div>
      <WeatherChartTable data={data} todayISO={todayISO} />
    </Card>
  );
};

export default WeatherChart;
