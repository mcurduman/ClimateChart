import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const Verify = () => {
    const navigate = useNavigate();
    const [code, setCode] = useState("");
    const [currentUser, setCurrentUser] = useState<any>(null);

    useEffect(() => {
        const user = localStorage.getItem("climateapp_currentUser");
        if (user) {
            const parsedUser = JSON.parse(user);
            setCurrentUser(parsedUser);
            if (parsedUser.verified) {
                navigate("/dashboard");
            }
        } else {
            navigate("/auth");
        }
    }, [navigate]);

    const handleVerify = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!currentUser) return;
        try {
            const res = await fetch("http://localhost:8089/v1/user/confirm-email", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    email: currentUser.email,
                    code,
                }),
            });
            const data = await res.json();
            if (!res.ok || !data.success) {
                throw new Error(data.message || "Invalid verification code.");
            }
            const updatedUser = { ...currentUser, verified: true };
            localStorage.setItem("climateapp_currentUser", JSON.stringify(updatedUser));
            toast.success("Account verified!", { description: "Your account has been successfully verified." });
            navigate("/account");
        } catch (err: any) {
            toast.error("Verification failed", { description: err?.message || "Invalid verification code." });
        }
    };

    const handleRequestCode = async () => {
        if (!currentUser) return;
        try {
            const res = await fetch("http://localhost:8089/v1/user/send-verification-email", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: currentUser.email }),
            });
            const data = await res.json();
            if (!res.ok || !data.success) {
                throw new Error(data.message || "Failed to send verification code.");
            }
            toast.success("Verification code sent!", { description: data.message || "Check your email." });
        } catch (err: any) {
            toast.error("Failed to send code", { description: err?.message || "Try again later." });
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center p-4">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle>Verify Your Account</CardTitle>
                    <CardDescription>
                        Enter the verification code sent to your email
                        {currentUser && (
                            <>: <strong>{currentUser.email}</strong></>
                        )}
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleVerify} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="code">Verification Code</Label>
                            <Input
                                id="code"
                                type="text"
                                value={code}
                                onChange={(e) => setCode(e.target.value)}
                                placeholder="Enter 6-digit code"
                                required
                            />
                        </div>
                        <Button type="submit" className="w-full">Verify</Button>
                        <Button
                            type="button"
                            variant="outline"
                            className="w-full"
                            onClick={handleRequestCode}
                        >
                            Request Verification Code
                        </Button>
                        <Button
                            type="button"
                            variant="ghost"
                            className="w-full"
                            onClick={() => navigate("/dashboard")}
                        >
                            Skip for now
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
};

export default Verify;