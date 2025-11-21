import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, XCircle, Key, ArrowLeft } from "lucide-react";
import { toast } from "sonner";

const Account = () => {
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [password, setPassword] = useState("");
  const [passwordConfirmed, setPasswordConfirmed] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const user = localStorage.getItem("climateapp_currentUser");
    if (user) {
      const parsedUser = JSON.parse(user);
      fetch(`http://localhost:8089/v1/user/me/${parsedUser.email}`)
        .then(async (res) => {
          if (!res.ok) throw new Error("Failed to fetch user info");
          const meData = await res.json();
          fetch(`http://localhost:8089/v1/user/api-key/${parsedUser.email}`)
            .then(async (res) => {
              let apiKey = null;
              if (res.ok) {
                const data = await res.json();
                apiKey = data?.value || null;
              }
              setCurrentUser({
                ...parsedUser,
                apiKey,
                verified: meData.emailVerified,
              });
            })
            .catch(() => {
              setCurrentUser({
                ...parsedUser,
                apiKey: null,
                verified: meData.emailVerified,
              });
            });
        })
        .catch(() => {
          setCurrentUser(parsedUser);
        });
    } else {
      navigate("/auth");
    }
  }, [navigate]);

  const generateApiKey = () => {
    if (currentUser && !currentUser.apiKey) {
      fetch("http://localhost:8089/v1/user/api-keys", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_email: currentUser.email,
          created_at: new Date().toISOString(),
        }),
      })
      .then(async (res) => {
        if (!res.ok) throw new Error("Failed to generate API Key");
        const data = await res.json();
        const apiKey = data.value;
        const updatedUser = { ...currentUser, apiKey };
        localStorage.setItem("climateapp_currentUser", JSON.stringify(updatedUser));
        setCurrentUser(updatedUser);
        toast.success("API Key generated successfully!");
      })
      .catch(() => {
        toast.error("Failed to generate API Key.", {
          description: "Try again later.",
        });
      });
    }
  };

  const handlePasswordConfirm = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8089/v1/user/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: currentUser.email,
          password,
        }),
      });
      if (!res.ok) throw new Error("Invalid password");
      setPasswordConfirmed(true);
      toast.success("Password confirmed!");
    } catch {
      toast.error("Incorrect password. Please try again.");
      setPassword("");
    } finally {
      setLoading(false);
    }
  };

  if (!currentUser) return null;

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="mx-auto max-w-2xl space-y-6">
        <Button variant="ghost" onClick={() => navigate("/dashboard")}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Dashboard
        </Button>

        <Card>
          <CardHeader>
            <CardTitle>Account Information</CardTitle>
            <CardDescription>Manage your account settings and API keys</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <h3 className="text-sm font-medium text-muted-foreground">Name</h3>
              <p className="text-lg">{currentUser.name}</p>
            </div>

            <div className="space-y-2">
              <h3 className="text-sm font-medium text-muted-foreground">Email</h3>
              <p className="text-lg">{currentUser.email}</p>
            </div>

            <div className="space-y-2">
              <h3 className="text-sm font-medium text-muted-foreground">Verification Status</h3>
              <div className="flex items-center gap-2">
                {currentUser.verified ? (
                  <>
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <Badge variant="default">Verified</Badge>
                  </>
                ) : (
                  <>
                    <XCircle className="h-5 w-5 text-orange-600" />
                    <Badge variant="secondary">Not Verified</Badge>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => navigate("/verify")}
                    >
                      Verify Now
                    </Button>
                  </>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <h3 className="text-sm font-medium text-muted-foreground">API Key</h3>
              {!currentUser.verified ? (
                <div className="text-sm text-muted-foreground bg-yellow-50 border border-yellow-200 rounded p-2">
                  You must verify your email before generating or viewing your API key.
                </div>
              ) : (() => {
                if (!passwordConfirmed) {
                  return (
                    <form onSubmit={handlePasswordConfirm} className="space-y-2">
                      <p className="text-sm text-muted-foreground">Please re-enter your password to view or generate your API key.</p>
                      <input
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        placeholder="Enter password"
                        className="border rounded px-2 py-1 w-full"
                        required
                      />
                      <Button type="submit" disabled={loading || !password}>
                        {loading ? "Checking..." : "Confirm Password"}
                      </Button>
                    </form>
                  );
                } else if (currentUser.apiKey) {
                  return (
                    <div className="flex items-center gap-2 rounded-md border bg-muted p-3">
                      <Key className="h-4 w-4" />
                      <code className="text-sm">{currentUser.apiKey}</code>
                    </div>
                  );
                } else {
                  return (
                    <div className="space-y-2">
                      <p className="text-sm text-muted-foreground">No API key generated yet</p>
                      <Button onClick={generateApiKey}>
                        <Key className="mr-2 h-4 w-4" />
                        Generate API Key
                      </Button>
                    </div>
                  );
                }
              })()}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Account;
