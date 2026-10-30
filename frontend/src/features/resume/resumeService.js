import { apiClient } from "@/services/apiClient";

export const resumeService = {
    async uploadResume(file) {
        const formData = new FormData();

        formData.append("file", file);

        const response = await apiClient.post(
            "/resumes/upload",
            formData
        );

        return response.data;
    },

    async analyzeResume(resumeId) {
        const response = await apiClient.post(
            `/resumes/${resumeId}/analyze`
        );

        return response.data;
    },

    async getLatestAnalysis(resumeId) {
        const response = await apiClient.get(
            `/resumes/${resumeId}/analysis`
        );

        return response.data;
    },

    async getAnalysisHistory(resumeId) {
        const response = await apiClient.get(
            `/resumes/${resumeId}/analyses`
        );

        return response.data;
    },

    async createChunks(resumeVersionId) {
        const response = await apiClient.post(
            `/resumes/versions/${resumeVersionId}/chunks`
        );
        return response.data;
    },

    async searchResume(resumeVersionId, query, limit = 5) {
        const response = await apiClient.get(
            `/resumes/versions/${resumeVersionId}/search`,
            { params: { query, limit } }
        );

        return response.data;

    },

    async askResumeQuestion(resumeVersionId, query, limit = 5) {
        const response = await apiClient.get(
            `/resumes/versions/${resumeVersionId}/ask`,
            { params: { query, limit } }
        );
        return response.data;
    },

    async getUserAnalysisHistory() {
        const response = await apiClient.get("/resumes/analyses/history");
        return response.data;
    },

    async getUserResumes() {
        const response = await apiClient.get("/resumes/");
        return response.data;
    },
    



}   