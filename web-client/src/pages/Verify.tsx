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

    const handleVerify = (e: React.FormEvent) => {
        e.preventDefault();

        if (code === currentUser?.verificationCode) {
            const users = JSON.parse(localStorage.getItem("climateapp_users") || "[]");
            const updatedUsers = users.map((u: any) =>
                u.id === currentUser.id ? { ...u, verified: true } : u
            );

            localStorage.setItem("climateapp_users", JSON.stringify(updatedUsers));
            const updatedUser = { ...currentUser, verified: true };
            localStorage.setItem("climateapp_currentUser", JSON.stringify(updatedUser));

            toast.success("Account verified!", { description: "Your account has been successfully verified." });
            navigate("/dashboard");
        } else {
            toast.error("Verification failed", { description: "Invalid verification code." });
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
                            <div className="mt-2 rounded p-2 text-xs">
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