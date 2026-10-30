
import { useRef, useState } from "react";
import { Upload, FileText, X, LoaderCircle } from "lucide-react";
import { Button } from "../../../components/ui/button";
import { Card, CardContent } from "../../../components/ui/card";
import { useResume } from "../resumeHooks";
import { showToast } from "../../../utils/toast";

export default function ResumeUpload() {
    const fileInputRef = useRef(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const { upload, loading } = useResume();

    function handleFileChange(event) {
        const file = event.target.files?.[0];

        if (!file) return;

        const isPdf = file.type === "application/pdf";
        const isDocx = file.name.toLowerCase().endsWith(".docx");

        if (!isPdf && !isDocx) {
            showToast.error("Please select a PDF or DOCX file.");
            event.target.value = "";
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            showToast.error("File size must be 5 MB or less.");
            event.target.value = "";
            return;
        }

        setSelectedFile(file);
    }

    async function handleUpload() {
        if (!selectedFile) {
            showToast.error("Please select a resume first.");
            return;
        }

        try {
            const uploadedResume = await upload(selectedFile);

            console.log("Uploaded resume:", uploadedResume);

            showToast.success("Resume uploaded successfully!");
            setSelectedFile(null);

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }
        } catch (error) {
            console.error("Resume upload error:", error);

            showToast.error(
                error?.response?.data?.detail || "Failed to upload resume."
            );
        }
    }

    function removeFile() {
        setSelectedFile(null);

        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    }

    return (
        <Card>
            <CardContent className="p-6">
                <div className="mb-5">
                    <h2 className="text-xl font-semibold">Upload your resume</h2>
                    <p className="mt-1 text-sm text-muted-foreground">
                        Upload a PDF or DOCX file to get started with AI-powered resume analysis.
                    </p>
                </div>

                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    onChange={handleFileChange}
                    className="hidden"
                />

                <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className="flex w-full flex-col items-center justify-center rounded-xl border-2 border-dashed border-border bg-muted/30 px-6 py-10 text-center transition hover:border-primary hover:bg-muted/60"
                >
                    <Upload className="mb-3 h-8 w-8 text-primary" />

                    <span className="font-medium">
                        Click to select your resume
                    </span>

                    <span className="mt-1 text-sm text-muted-foreground">
                        PDF or DOCX · Maximum 5 MB
                    </span>
                </button>

                {selectedFile && (
                    <div className="mt-4 flex items-center gap-3 rounded-lg border p-3">
                        <FileText className="h-8 w-8 shrink-0 text-primary" />

                        <div className="min-w-0 flex-1">
                            <p className="truncate text-sm font-medium">
                                {selectedFile.name}
                            </p>
                            <p className="text-xs text-muted-foreground">
                                {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                            </p>
                        </div>

                        <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            onClick={removeFile}
                            disabled={loading}
                            aria-label="Remove selected file"
                        >
                            <X className="h-4 w-4" />
                        </Button>
                    </div>
                )}

                <Button
                    type="button"
                    onClick={handleUpload}
                    disabled={!selectedFile || loading}
                    className="mt-4 w-full"
                >
                    {loading ? (
                        <>
                            <LoaderCircle className="mr-2 h-4 w-4 animate-spin" />
                            Uploading...
                        </>
                    ) : (
                        "Upload Resume"
                    )}
                </Button>
            </CardContent>
        </Card>
    );
}
