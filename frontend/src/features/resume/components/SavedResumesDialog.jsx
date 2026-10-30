
import { FileText, FolderOpen, Check, LoaderCircle } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "../../../components/ui/dialog";

export default function SavedResumesDialog({
  open,
  onOpenChange,
  resumes,
  loading,
  selectedResumeId,
  onSelect,
}) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FolderOpen className="h-5 w-5" />
            My Saved Resumes
          </DialogTitle>
          <DialogDescription>
            Choose a resume to work with.
          </DialogDescription>
        </DialogHeader>

        <div className="max-h-[60vh] space-y-2 overflow-y-auto pr-1">
          {loading ? (
            <div className="flex items-center gap-2 py-6 text-sm text-muted-foreground">
              <LoaderCircle className="h-4 w-4 animate-spin" />
              Loading resumes...
            </div>
          ) : resumes.length === 0 ? (
            <p className="py-6 text-sm text-muted-foreground">
              No saved resumes yet. Upload one to get started.
            </p>
          ) : (
            resumes.map((resume) => {
              const selected = selectedResumeId === resume.id;

              return (
                <button
                  key={resume.id}
                  type="button"
                  onClick={() => {
                    onSelect(resume);
                    onOpenChange(false);
                  }}
                  className={`flex w-full items-center gap-3 rounded-xl border p-3 text-left transition hover:bg-muted ${selected
                    ? "border-primary bg-primary/5"
                    : "border-border"
                    }`}
                >
                  <FileText className="h-5 w-5 shrink-0 text-primary" />

                  <div className="min-w-0 flex-1">
                    <p className="break-words text-sm font-medium">
                      {resume.filename}
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      Resume ID: {resume.id}
                    </p>
                  </div>

                  {selected && (
                    <Check className="h-5 w-5 shrink-0 text-primary" />
                  )}
                </button>
              );
            })
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
