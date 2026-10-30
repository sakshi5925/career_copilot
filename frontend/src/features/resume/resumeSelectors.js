export const selectCurrentResume = (state) =>
  state.resume.currentResume;

export const selectResumeAnalysis = (state) =>
  state.resume.analysis;

export const selectResumeLoading = (state) =>
  state.resume.loading;

export const selectResumeAnalyzing = (state) =>
  state.resume.analyzing;

export const selectResumeError = (state) =>
  state.resume.error;