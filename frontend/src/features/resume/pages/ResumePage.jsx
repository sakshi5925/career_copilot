import { useEffect, useState } from "react";
import {
    FileText,
    History,
    MessageSquare,
    Sparkles,
    FolderOpen,
    ChevronDown,
} from "lucide-react";
import { Button } from "../../../components/ui/button";

import ResumeUpload from "../components/ResumeUpload";
import ResumeAnalysis from "../components/ResumeAnalysis";
import ResumeHistory from "../components/ResumeHistory";
import SavedResumesDialog from "../components/SavedResumesDialog";
import ResumeChat from "../components/ResumeChat";
import { useResume } from "../resumeHooks";

export default function ResumePage() {
    const { currentResume, getUserResumes } = useResume();
    const [selectedResume, setSelectedResume] = useState(null);
    const [resumes, setResumes] = useState([]);
    const [resumesLoading, setResumesLoading] = useState(true);
    const [savedResumesOpen, setSavedResumesOpen] = useState(false);


    useEffect(() => {
        async function loadResumes() {
            try {
                const data = await getUserResumes();
                const savedResumes = Array.isArray(data) ? data : [];

                setResumes(savedResumes);




                setSelectedResume((previous) => {
                    if (previous) {
                        return savedResumes.find(
                            (resume) => resume.id === previous.id
                        ) ?? savedResumes[0] ?? null;
                    }


                    return savedResumes[0] ?? null;
                });
            } catch (error) {
                console.error("Failed to load resumes:", error);
            } finally {
                setResumesLoading(false);
            }
        }

        loadResumes();
    }, [getUserResumes]);
    

    const [selectedAnalysis, setSelectedAnalysis] = useState(null);

    return (
        <div className="mx-auto w-full max-w-[1600px] space-y-8 px-1 pb-10">
            <header className="flex flex-wrap items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">
                        Resume Manager
                    </h1>
                    <p className="mt-2 text-sm text-muted-foreground">
                        Manage your resumes and improve your career profile with AI.
                    </p>
                </div>


            </header>

            <div className="grid grid-cols-1 items-start gap-8 lg:grid-cols-12">
                {/* Left: Upload */}
                <aside className="min-w-0 space-y-6 lg:col-span-3">
                    <div className="flex items-center gap-2">
                        <FileText className="h-5 w-5 text-primary" />
                        <h2 className="text-lg font-semibold">Your Resume</h2>
                    </div>

                    <ResumeUpload />

                    <Button
                        type="button"
                        variant="outline"
                        className="w-full justify-between"
                        onClick={() => setSavedResumesOpen(true)}
                    >
                        <span className="flex items-center gap-2">
                            <FolderOpen className="h-4 w-4" />
                            My Saved Resumes
                            <span className="rounded-full bg-muted px-2 py-0.5 text-xs">
                                {resumes.length}
                            </span>
                        </span>
                        <ChevronDown className="h-4 w-4" />
                    </Button>

                    {selectedResume && (
                        <div className="rounded-xl bg-muted/40 p-3">
                            <p className="text-xs text-muted-foreground">
                                Resume selected for chat
                            </p>
                            <p className="mt-1 break-words text-sm font-medium">
                                {selectedResume.filename}
                            </p>
                        </div>
                    )}

                </aside>

                {/* Center: Analysis and chat */}
                <main className="min-w-0 space-y-8 lg:col-span-6">
                    <ResumeAnalysis
                        selectedAnalysis={selectedAnalysis}
                    />

                    <section className="space-y-4">

                        <ResumeChat
                            key={selectedResume?.id}
                            resumeVersionId={selectedResume?.resume_version_id}
                        />
                    </section>
                </main>

                {/* Right: History */}
                <aside className="min-w-0 space-y-4 lg:col-span-3">
                    <div className="flex items-center gap-2">
                        <History className="h-5 w-5 text-primary" />
                        <h2 className="text-lg font-semibold">Analysis History</h2>
                    </div>

                    <p className="text-sm text-muted-foreground">
                        Select a previous result to view its full analysis.
                    </p>

                    <ResumeHistory
                        onSelect={(item) => setSelectedAnalysis(item)}
                        selectedAnalysisId={selectedAnalysis?.id}
                    />
                </aside>
            </div>
            <SavedResumesDialog
                open={savedResumesOpen}
                onOpenChange={setSavedResumesOpen}
                resumes={resumes}
                loading={resumesLoading}
                selectedResumeId={selectedResume?.id}
                onSelect={(resume) => {
                    setSelectedResume(resume);
                    setSelectedAnalysis(null);
                }}
            />
        </div>
    );
}
