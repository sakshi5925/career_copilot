
import { useCallback} from "react";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
    uploadResume,
    analyzeResume,
    clearResumeError,
    clearResumeState,
} from "./resumeSlice";

import {
    selectCurrentResume,
    selectResumeAnalysis,
    selectResumeLoading,
    selectResumeAnalyzing,
    selectResumeError,
} from "./resumeSelectors";

import { resumeService } from "./resumeService";

export function useResume() {
    const dispatch = useAppDispatch();
    const currentResume = useAppSelector(selectCurrentResume);
    const analysis = useAppSelector(selectResumeAnalysis);
    const loading = useAppSelector(selectResumeLoading);
    const analyzing = useAppSelector(selectResumeAnalyzing);
    const error = useAppSelector(selectResumeError);
    const getUserResumes = useCallback(async () => {
        return await resumeService.getUserResumes();
    }, []);

    return {
        currentResume,
        analysis,
        loading,
        analyzing,
        error,
        getUserResumes,
        upload: (file) => dispatch(uploadResume(file)).unwrap(),
        analyze: (resumeId) => dispatch(analyzeResume(resumeId)).unwrap(),
        clearError: () => dispatch(clearResumeError()),
        reset: () => dispatch(clearResumeState()),

    }
}