
import { useEffect, useState } from "react";
import { History, LoaderCircle, FileText } from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../../components/ui/card";
import { resumeService } from "../resumeService";
import { showToast } from "../../../utils/toast";

export default function ResumeHistory({
  onSelect,
  selectedAnalysisId,
  refreshKey,
}) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function loadHistory() {
      setLoading(true);

      try {
        const data = await resumeService.getUserAnalysisHistory();

        if (!cancelled) {
          setHistory(Array.isArray(data) ? data : []);
        }
      } catch (error) {
        if (!cancelled) {
          showToast.error(
            error?.response?.data?.detail ||
              "Could not load analysis history."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadHistory();

    return () => {
      cancelled = true;
    };
  }, [refreshKey]);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <History className="h-5 w-5" />
          All Resume Analysis History
        </CardTitle>
      </CardHeader>

      <CardContent>
        {loading ? (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <LoaderCircle className="h-4 w-4 animate-spin" />
            Loading history...
          </div>
        ) : history.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            No previous analyses found. Upload and analyze a resume to get started.
          </p>
        ) : (
          <div className="space-y-3">
            {history.map((item) => (
              <button
                type="button"
                key={item.id}
                onClick={() => onSelect?.({ ...item })}
                className={`flex w-full items-center justify-between gap-4 rounded-lg border p-4 text-left transition-colors hover:bg-accent ${
                  selectedAnalysisId === item.id
                    ? "border-primary bg-accent"
                    : ""
                }`}
              >
                <div className="flex min-w-0 items-center gap-3">
                  <FileText className="h-5 w-5 shrink-0 text-muted-foreground" />

                  <div className="min-w-0">
                    <p className="font-medium">
                      Resume #{item.resume_id}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {item.created_at
                        ? new Date(item.created_at).toLocaleString()
                        : "Previous analysis"}
                    </p>
                  </div>
                </div>

                <span className="shrink-0 font-semibold">
                  {item.score}/100
                </span>
              </button>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
