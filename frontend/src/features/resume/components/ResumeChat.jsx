import { useState } from "react";
import { Send, Bot, User, LoaderCircle, FileText } from "lucide-react";
import { Button } from "../../../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../../../components/ui/card";
import { Textarea } from "../../../components/ui/textarea";
import { resumeService } from "../resumeService";
import { showToast } from "../../../utils/toast";

export default function ResumeChat({ resumeVersionId }) {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSend(event) {
    event.preventDefault();

    const query = question.trim();

    if (!query || loading) return;

    if (!resumeVersionId) {
      showToast.error("Please select a resume version first.");
      return;
    }

    setMessages((previous) => [
      ...previous,
      { role: "user", content: query },
    ]);
    setQuestion("");
    setLoading(true);

    try {
      const result = await resumeService.askResumeQuestion(
        resumeVersionId,
        query
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: result.answer,
          sources: result.sources ?? [],
        },
      ]);
    } catch (error) {
      console.error("Resume chat error:", error);
      console.error("Response data:", error?.response?.data);
      console.error("Status:", error?.response?.status);

      showToast.error(
        error?.response?.data?.detail ||
        error?.message ||
        "Could not get an answer. Please try again."
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: "Sorry, I couldn't answer that question. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bot className="h-5 w-5 text-primary" />
          Resume Chat
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Ask questions about your skills, experience, and projects.
        </p>
      </CardHeader>

      <CardContent>
        <div className="mb-4 max-h-[420px] min-h-[180px] space-y-4 overflow-y-auto rounded-xl bg-muted/20 p-4">
          {messages.length === 0 && (
            <div className="flex min-h-[150px] flex-col items-center justify-center text-center">
              <Bot className="mb-3 h-8 w-8 text-muted-foreground" />
              <p className="font-medium">Ask your resume anything</p>
              <p className="mt-1 text-sm text-muted-foreground">
                For example: What are my strongest technical skills?
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex gap-2 ${message.role === "user"
                ? "justify-end"
                : "justify-start"
                }`}
            >
              {message.role === "assistant" && (
                <Bot className="mt-2 h-5 w-5 shrink-0 text-primary" />
              )}

              <div
                className={`max-w-[85%] rounded-xl px-4 py-3 text-sm ${message.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-background border"
                  }`}
              >
                <div className="whitespace-pre-wrap break-words">
                  {message.content}
                </div>

                {message.sources?.length > 0 && (
                  <div className="mt-3 border-t pt-2">
                    <p className="mb-2 flex items-center gap-1 text-xs font-semibold">
                      <FileText className="h-3 w-3" />
                      Resume sources
                    </p>

                    {message.sources.map((source, sourceIndex) => (
                      <p
                        key={source.id ?? sourceIndex}
                        className="mb-2 text-xs text-muted-foreground"
                      >
                        {source.content}
                      </p>
                    ))}
                  </div>
                )}
              </div>

              {message.role === "user" && (
                <User className="mt-2 h-5 w-5 shrink-0 text-primary" />
              )}
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <LoaderCircle className="h-4 w-4 animate-spin" />
              Thinking...
            </div>
          )}
        </div>

        <form onSubmit={handleSend} className="flex items-end gap-2">
          <Textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a question about your resume..."
            rows={2}
            className="min-h-[48px] resize-none"
            disabled={loading}
          />

          <Button
            type="submit"
            size="icon"
            disabled={loading || !question.trim() || !resumeVersionId}
            aria-label="Send message"
          >
            {loading ? (
              <LoaderCircle className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
