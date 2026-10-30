
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../authHooks";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { showToast } from "@/utils/toast";
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription,
} from "@/components/ui/card";

export default function RegisterForm() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const { register, loading, error, clearError } = useAuth();
    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();
        clearError();

        try {
            await register({ name, email, password });
            showToast.success("registration successful!");
            navigate("/login", {
                state: { message: "Account created successfully. Please log in." },
            });
        } catch {
            showToast.error(
                typeof error === "string" ? error : "Login failed. Please try again."
            );
        }
    }

    return (
        <Card className="w-full max-w-md shadow-lg">
            <CardHeader className="space-y-1">
                <CardTitle className="text-2xl font-bold">
                    Create your account
                </CardTitle>
                <CardDescription>
                    Start organizing your career with AI.
                </CardDescription>
            </CardHeader>

            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-5">
                    <div className="space-y-2">
                        <Label htmlFor="name">Full name</Label>
                        <Input
                            id="name"
                            placeholder="Your full name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            autoComplete="name"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="register-email">Email</Label>
                        <Input
                            id="register-email"
                            type="email"
                            placeholder="you@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            autoComplete="email"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="register-password">Password</Label>
                        <Input
                            id="register-password"
                            type="password"
                            placeholder="Create a password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete="new-password"
                            minLength={8}
                            required
                        />
                    </div>

                    {error && (
                        <p role="alert" className="text-sm text-destructive">
                            {typeof error === "string" ? error : "Registration failed"}
                        </p>
                    )}

                    <Button type="submit" className="w-full" disabled={loading}>
                        {loading ? "Creating account..." : "Create account"}
                    </Button>

                    <p className="text-center text-sm text-muted-foreground">
                        Already have an account?{" "}
                        <Link
                            to="/login"
                            className="font-medium text-primary underline-offset-4 hover:underline"
                        >
                            Log in
                        </Link>
                    </p>
                </form>
            </CardContent>
        </Card>
    );
}
