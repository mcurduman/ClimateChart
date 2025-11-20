import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import WeatherChart from "@/components/WeatherChart";
import type { ChartRow } from "@/components/WeatherChart";
import { User } from "lucide-react";

type ApiRecord = {
  date: string;
  temperature2mMaxC: number | string;
  temperature2mMinC: number | string;
  precipitationSumMm: number | string;
  pressureMslMeanHpa: number | string;
  windSpeed10mMaxKmh: number | string;
  relativeHumidity2mMaxPct: number | string;
};

type ApiResponse = {
  city: string;
  timezone: string;
  records: ApiRecord[];
};

const API_BASE = "http://localhost:8089/v1/weather";
// WIP user will have to enter his key
const API_KEY = "your_secret_key";

const parseYMDorISO = (s: string) => {
  const iso = s.slice(0, 10);
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(y, (m ?? 1) - 1, d ?? 1);
};

const toISODate = (d: Date) => {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
};

const fmtLabel = (d: Date) =>
  d.toLocaleDateString("en-US", { month: "short", day: "numeric" });

const mapApiToChartData = (recs: ApiRecord[]): ChartRow[] =>
  recs
    .slice()
    .sort((a, b) => parseYMDorISO(a.date).getTime() - parseYMDorISO(b.date).getTime())
    .map((r) => {
      const dt = parseYMDorISO(r.date);
      const xKey = toISODate(dt);
      return {
        xKey,
        date: fmtLabel(dt),
        temperature_2m_max: Number(r.temperature2mMaxC),
        temperature_2m_min: Number(r.temperature2mMinC),
        precipitation_sum: Number(r.precipitationSumMm),
        pressure_msl_mean: Number(r.pressureMslMeanHpa),
        wind_speed_10m_max: Number(r.windSpeed10mMaxKmh),
        relative_humidity_2m_max: Number(r.relativeHumidity2mMaxPct),
      };
    });

const makeMock = (days = 14): ChartRow[] =>
  Array.from({ length: days }, (_, i) => {
    const d = new Date();
    d.setHours(0, 0, 0, 0);
    d.setDate(d.getDate() - (days - 1 - i));
    const xKey = toISODate(d);
    return {
      xKey,
      date: fmtLabel(d),
      temperature_2m_max: 20 + Math.floor(Math.random() * 10),
      temperature_2m_min: 8 + Math.floor(Math.random() * 6),
      precipitation_sum: Math.floor(Math.random() * 10),
      pressure_msl_mean: 1000 + Math.floor(Math.random() * 30),
      wind_speed_10m_max: 5 + Math.floor(Math.random() * 25),
      relative_humidity_2m_max: 40 + Math.floor(Math.random() * 40),
    };
  });

const Dashboard = () => {
  const navigate = useNavigate();
  const [city, setCity] = useState("London");
  const [weatherData, setWeatherData] = useState<ChartRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [currentUser, setCurrentUser] = useState<any>(null);

  useEffect(() => {
    const user = localStorage.getItem("climateapp_currentUser");
    if (!user) {
      navigate("/auth");
    } else {
      setCurrentUser(JSON.parse(user));
    }
  }, [navigate]);

  const fetchWeatherData = async (cityName: string) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/${encodeURIComponent(cityName)}`, {
        headers: { "x-api-key": API_KEY },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const payload: ApiResponse = await res.json();

      const mapped = mapApiToChartData(payload.records);
      setWeatherData(mapped);

      toast.success(`Weather data for ${payload.city} loaded!`);
    } catch (e) {
      console.error(e);
      toast.error("Failed to fetch weather data. Using mock data.");
      setWeatherData(makeMock(14));
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchWeatherData(city);
  };

  const handleLogout = () => {
    localStorage.removeItem("climateapp_currentUser");
    navigate("/auth");
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="mx-auto max-w-6xl space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">ClimateChart Dashboard</h1>
          <div className="flex items-center gap-2">
            <Button variant="outline" onClick={() => navigate("/account")}>
              <User className="mr-2 h-4 w-4" />
              Account
            </Button>
            <Button variant="outline" onClick={handleLogout}>Logout</Button>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Weather Analysis</CardTitle>
            <CardDescription>View weather data fluctuations over the past 2 weeks</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="flex gap-4">
                <div className="flex-1 space-y-2">
                  <Label htmlFor="city">City</Label>
                  <Input
                    id="city"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    placeholder="Enter city name"
                    required
                  />
                </div>
                <div className="flex items-end">
                  <Button type="submit" disabled={loading}>
                    {loading ? "Loading..." : "Fetch Weather Data"}
                  </Button>
                </div>
              </div>
            </form>

            {weatherData.length > 0 && (
              <WeatherChart data={weatherData} city={city} />
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
