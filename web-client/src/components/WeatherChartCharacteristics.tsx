import React from "react";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { ChevronDown } from "lucide-react";

interface WeatherChartCharacteristicsProps {
  selectedCharacteristics: string[];
  setSelectedCharacteristics: (chars: string[]) => void;
  characteristicConfig: Record<string, { label: string; unit: string; color: string }>;
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

const WeatherChartCharacteristics: React.FC<WeatherChartCharacteristicsProps> = ({
  selectedCharacteristics,
  setSelectedCharacteristics,
  characteristicConfig,
  isOpen,
  setIsOpen,
}) => {
  const toggleCharacteristic = (c: string) => {
    setSelectedCharacteristics(
      selectedCharacteristics.includes(c)
        ? selectedCharacteristics.filter(x => x !== c)
        : [...selectedCharacteristics, c]
    );
  };

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen}>
      <CollapsibleTrigger className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors">
        <ChevronDown className={`h-4 w-4 transition-transform ${isOpen ? "rotate-180" : ""}`} />
        Select Characteristics
      </CollapsibleTrigger>
      <CollapsibleContent className="pt-3">
        <div className="grid grid-cols-2 gap-3 p-4 bg-muted/50 rounded-lg">
          {Object.entries(characteristicConfig).map(([key, config]) => (
            <div key={key} className="flex items-center space-x-2">
              <Checkbox id={key} checked={selectedCharacteristics.includes(key)} onCheckedChange={() => toggleCharacteristic(key)} />
              <Label htmlFor={key} className="cursor-pointer text-sm">{config.label} ({config.unit})</Label>
            </div>
          ))}
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
};

export default WeatherChartCharacteristics;
