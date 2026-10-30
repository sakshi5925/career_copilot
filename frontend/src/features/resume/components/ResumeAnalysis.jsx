
import { useEffect, useState } from "react";
import {
    X,
    Sparkles,
    LoaderCircle,
    Eye,
    CheckCircle2,
    AlertCircle,
    Target,
    Lightbulb,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { useResume } from "../resumeHooks";
import { showToast } from "@/utils/toast";

export default function ResumeAnalysis({
    selectedAnalysis,

}) {
    const {
        currentResume,
        analysis,
        analyzing,
        analyze,
    } = useResume();

    const [open, setOpen] = useState(false);


    const displayedAnalysis = selectedAnalysis ?? analysis;

    useEffect(() => {
        if (selectedAnalysis?.id) {
            setOpen(true);
        }
    }, [selectedAnalysis]);

    useEffect(() => {
        function handleEscape(event) {
            if (event.key === "Escape") setOpen(false);
        }

        if (open) {
            window.addEventListener("keydown", handleEscape);
            document.body.style.overflow = "hidden";
        }

        return () => {
            window.removeEventListener("keydown", handleEscape);
            document.body.style.overflow = "";
        };
    }, [open]);

    async function handleAnalyze() {
        if (!currentResume?.id) {
            showToast.error("Please upload a resume first.");
            return;
        }

        try {
            await analyze(currentResume.id);
            showToast.success("Resume analysis completed!");
        } catch (error) {
            showToast.error(
                error?.response?.data?.detail ||
                "Failed to analyze resume."
            );
        }
    }

    const score = displayedAnalysis?.score;

    return (
        <>
            <section className="space-y-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                        <div className="flex items-center gap-2">
                            <Sparkles className="h-5 w-5 text-primary" />
                            <h2 className="text-xl font-semibold">
                                AI Resume Analysis
                            </h2>
                        </div>

                        <p className="mt-1 text-sm text-muted-foreground">
                            Understand your resume score at a glance.
                        </p>
                    </div>

                    {currentResume && (
                        <Button
                            onClick={handleAnalyze}
                            disabled={analyzing}
                            variant="outline"
                            className="rounded-full"
                        >
                            {analyzing ? (
                                <LoaderCircle className="mr-2 h-4 w-4 animate-spin" />
                            ) : (
                                <Sparkles className="mr-2 h-4 w-4" />
                            )}
                            {analyzing ? "Analyzing..." : "Analyze Resume"}
                        </Button>
                    )}
                </div>

                {displayedAnalysis ? (
                    <div className="flex flex-col justify-between gap-5 rounded-2xl bg-muted/40 p-6 sm:flex-row sm:items-center">
                        <div className="flex items-center gap-5">
                            <div className="flex h-24 w-24 shrink-0 flex-col items-center justify-center rounded-full bg-background shadow-sm">
                                <span className="text-3xl font-bold tracking-tight">
                                    {score}
                                </span>
                                <span className="text-xs text-muted-foreground">
                                    out of 100
                                </span>
                            </div>

                            <div>
                                <p className="text-lg font-semibold">
                                    Resume Score
                                </p>

                                <p className="mt-1 text-sm text-muted-foreground">
                                    {score >= 80
                                        ? "Strong profile — keep improving."
                                        : score >= 60
                                            ? "Good start — a few improvements can help."
                                            : "Review the suggestions to strengthen your resume."}
                                </p>
                            </div>
                        </div>

                        <Button
                            onClick={() => setOpen(true)}
                            className="rounded-full"
                        >
                            <Eye className="mr-2 h-4 w-4" />
                            View Full Analysis
                        </Button>
                    </div>
                ) : (
                    <div className="rounded-2xl bg-muted/40 px-6 py-10 text-center">
                        <Sparkles className="mx-auto mb-3 h-8 w-8 text-muted-foreground" />

                        <p className="font-medium">
                            Your resume insights will appear here
                        </p>

                        <p className="mt-1 text-sm text-muted-foreground">
                            Upload a resume and run AI analysis to see your score.
                        </p>
                    </div>
                )}
            </section>

            {/* Full analysis modal */}
            {open && displayedAnalysis && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-white/30 p-4 backdrop-blur-md"
                    onMouseDown={(event) => {
                        if (event.target === event.currentTarget) {
                            setOpen(false);
                        }
                    }}
                >
                    <section
                        role="dialog"
                        aria-modal="true"
                        aria-labelledby="analysis-modal-title"
                        className="max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-3xl bg-white p-6 text-gray-900 shadow-2xl sm:p-8"
                    >
                        <div className="mb-7 flex items-start justify-between gap-4">
                            <div>
                                <div className="flex items-center gap-2 text-primary">
                                    <Sparkles className="h-5 w-5" />
                                    <span className="text-sm font-medium">
                                        AI-powered insights
                                    </span>
                                </div>

                                <h2
                                    id="analysis-modal-title"
                                    className="mt-2 text-2xl font-bold"
                                >
                                    Full Resume Analysis
                                </h2>

                                <p className="mt-1 text-sm text-muted-foreground">
                                    Score, strengths, skill gaps, and actionable suggestions.
                                </p>
                            </div>

                            <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => setOpen(false)}
                                aria-label="Close analysis"
                                className="shrink-0 rounded-full"
                            >
                                <X className="h-5 w-5" />
                            </Button>
                        </div>

                        <div className="mb-7 flex items-center gap-5 rounded-2xl bg-muted/50 p-5">
                            <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-full bg-background text-3xl font-bold shadow-sm">
                                {score}
                            </div>

                            <div>
                                <h3 className="text-lg font-semibold">
                                    Resume Score
                                </h3>
                                <p className="text-sm text-muted-foreground">
                                    AI-generated score out of 100
                                </p>
                            </div>
                        </div>

                        <div className="grid gap-5 sm:grid-cols-2">
                            <AnalysisSection
                                title="Strengths"
                                items={displayedAnalysis.strengths}
                                icon={CheckCircle2}
                            />

                            <AnalysisSection
                                title="Weaknesses"
                                items={displayedAnalysis.weaknesses}
                                icon={AlertCircle}
                            />

                            <AnalysisSection
                                title="Missing Skills"
                                items={displayedAnalysis.missing_skills}
                                icon={Target}
                            />

                            <AnalysisSection
                                title="Recommendations"
                                items={displayedAnalysis.recommendations}
                                icon={Lightbulb}
                            />
                        </div>
                    </section>
                </div>
            )}
        </>
    );
}

function AnalysisSection({ title, items, icon: Icon }) {
    return (
        <section className="rounded-2xl bg-muted/30 p-5">
            <div className="mb-4 flex items-center gap-2">
                <Icon className="h-5 w-5 text-primary" />
                <h3 className="font-semibold">{title}</h3>
            </div>

            {items?.length ? (
                <ul className="space-y-3">
                    {items.map((item, index) => (
                        <li
                            key={`${title}-${index}`}
                            className="flex gap-3 text-sm leading-6 text-muted-foreground"
                        >
                            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                            <span>{item}</span>
                        </li>
                    ))}
                </ul>
            ) : (
                <p className="text-sm text-muted-foreground">
                    No items available.
                </p>
            )}
        </section>
    );
}
