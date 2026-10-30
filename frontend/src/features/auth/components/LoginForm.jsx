
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../authHooks";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { showToast } from "@/utils/toast";

export default function LoginForm() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const { login, loading, error, clearError } = useAuth();
    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();
        clearError();

        try {
            await login({ email, password });
            showToast.success("Login successful!");
            navigate("/dashboard");
        } catch {
            // The Redux slice stores the API error.
            showToast.error(
                typeof error === "string" ? error : "Login failed. Please try again."
            );
        }
    }

    return (
        <Card className="w-full max-w-md shadow-lg">
            <CardHeader className="space-y-1">
                <CardTitle className="text-2xl font-bold">
                    Welcome back
                </CardTitle>
                <CardDescription>
                    Log in to your AI Career Copilot account.
                </CardDescription>
            </CardHeader>

            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-5">
                    <div className="space-y-2">
                        <Label htmlFor="email">Email</Label>
                        <Input
                            id="email"
                            type="email"
                            placeholder="you@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            autoComplete="email"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="password">Password</Label>
                        <Input
                            id="password"
                            type="password"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete="current-password"
                            required
                        />
                    </div>

                    {error && (
                        <p role="alert" className="text-sm text-destructive">
                            {typeof error === "string" ? error : "Login failed"}
                        </p>
                    )}

                    <Button type="submit" className="w-full" disabled={loading}>
                        {loading ? "Logging in..." : "Log in"}
                    </Button>

                    <p className="text-center text-sm text-muted-foreground">
                        Don't have an account?{" "}
                        <Link
                            to="/register"
                            className="font-medium text-primary underline-offset-4 hover:underline"
                        >
                            Create account
                        </Link>
                    </p>
                </form>
            </CardContent>
        </Card>
    );
}
