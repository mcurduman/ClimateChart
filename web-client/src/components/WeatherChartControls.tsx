import React from "react";
import { Button } from "@/components/ui/button";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Maximize, Minimize, TrendingUp, BarChart3, Activity } from "lucide-react";

interface WeatherChartControlsProps {
  chartType: "line" | "bar" | "area";
  setChartType: (type: "line" | "bar" | "area") => void;
  showGrid: boolean;
  setShowGrid: (v: boolean) => void;
  showDots: boolean;
  setShowDots: (v: boolean) => void;
  smoothCurve: boolean;
  setSmoothCurve: (v: boolean) => void;
  isFullscreen: boolean;
  toggleFullscreen: () => void;
  animate: boolean;
  setAnimate: (v: boolean) => void;
}

const WeatherChartControls: React.FC<WeatherChartControlsProps> = ({
  chartType,
  setChartType,
  showGrid,
  setShowGrid,
  showDots,
  setShowDots,
  smoothCurve,
  setSmoothCurve,
  isFullscreen,
  toggleFullscreen,
  animate,
  setAnimate,
}) => (
  <div className="space-y-4">
    <div className="space-y-2">
      <Label className="text-sm text-muted-foreground">Chart Type</Label>
      <ToggleGroup type="single" value={chartType} onValueChange={(v) => v && setChartType(v as any)} className="justify-start">
        <ToggleGroupItem value="line" aria-label="Line chart"><TrendingUp className="mr-2 h-4 w-4" />Line</ToggleGroupItem>
        <ToggleGroupItem value="bar" aria-label="Bar chart"><BarChart3 className="mr-2 h-4 w-4" />Bar</ToggleGroupItem>
        <ToggleGroupItem value="area" aria-label="Area chart"><Activity className="mr-2 h-4 w-4" />Area</ToggleGroupItem>
      </ToggleGroup>
    </div>
    <div className="flex flex-wrap gap-6">
      <div className="flex items-center space-x-2">
        <Switch id="grid" checked={showGrid} onCheckedChange={setShowGrid} />
        <Label htmlFor="grid" className="cursor-pointer">Show Grid</Label>
      </div>
      {chartType === "line" && (
        <>
          <div className="flex items-center space-x-2">
            <Switch id="dots" checked={showDots} onCheckedChange={setShowDots} />
            <Label htmlFor="dots" className="cursor-pointer">Show Dots</Label>
          </div>
          <div className="flex items-center space-x-2">
            <Switch id="smooth" checked={smoothCurve} onCheckedChange={setSmoothCurve} />
            <Label htmlFor="smooth" className="cursor-pointer">Smooth Curve</Label>
          </div>
        </>
      )}
      {chartType === "area" && (
        <div className="flex items-center space-x-2">
          <Switch id="smooth-area" checked={smoothCurve} onCheckedChange={setSmoothCurve} />
          <Label htmlFor="smooth-area" className="cursor-pointer">Smooth Curve</Label>
        </div>
      )}
    </div>
    <div className="flex items-center justify-end gap-2 mt-2">
      <div className="hidden sm:flex items-center space-x-2">
        <Switch id="animate" checked={animate} onCheckedChange={setAnimate} />
        <Label htmlFor="animate" className="cursor-pointer text-sm">Animate</Label>
      </div>
      <Button
        variant="outline"
        size="icon"
        onClick={toggleFullscreen}
        title={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}
      >
        {isFullscreen ? <Minimize className="h-4 w-4" /> : <Maximize className="h-4 w-4" />}
      </Button>
    </div>
    <Separator />
  </div>
);

export default WeatherChartControls;
