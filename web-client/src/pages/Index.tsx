import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Cloud, TrendingUp, Shield } from "lucide-react";
const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background p-4">
      <div className="text-center space-y-6 max-w-2xl">
        <div className="flex justify-center mb-6">
          <Cloud className="h-20 w-20 text-primary" />
        </div>
        <h1 className="text-5xl font-bold">ClimateChart</h1>
        <p className="text-xl text-muted-foreground">
          Track and analyze temperature fluctuations across cities worldwide
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
          <Card>
            <CardHeader className="text-center">
              <TrendingUp className="h-8 w-8 text-primary mb-2 mx-auto" />
              <CardTitle className="text-lg">Temperature Trends</CardTitle>
                <CardDescription></CardDescription>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="text-center">
              <Cloud className="h-8 w-8 text-primary mb-2 mx-auto" />
              <CardTitle className="text-lg">City Analysis</CardTitle>
                <CardDescription></CardDescription>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="text-center">
              <Shield className="h-8 w-8 text-primary mb-2 mx-auto" />
              <CardTitle className="text-lg">API Access</CardTitle>
                <CardDescription></CardDescription>
            </CardHeader>
          </Card>
        </div>

        <div className="flex gap-4 justify-center mt-8">
          <Button size="lg" onClick={() => navigate("/auth")}>
            Get Started
          </Button>
          <Button size="lg" variant="outline" onClick={() => navigate("/dashboard")}>
            View Demo
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Index;
