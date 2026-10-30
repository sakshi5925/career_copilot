import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { resumeService } from "./resumeService";


function getErrorMessage(error, fallback) {
  return (
    error.response?.data?.detail ||
    error.message ||
    fallback
  );
}

export const uploadResume = createAsyncThunk(
    "resume/upload",
    async (file, { rejectWithValue }) => {
        try {
            return await resumeService.uploadResume(file);
        }
        catch (error) {
            return rejectWithValue(
                getErrorMessage(error, "Resume upload failed")
            );
        }
    }

);

export const analyzeResume =createAsyncThunk(
    "resume/analyze",
    async (resumeId,{rejectWithValue})=>{
        try{
            return await  resumeService.analyzeResume(resumeId);
        }
        catch (error){
            return rejectWithValue(
                getErrorMessage(error, "Resume analysis failed")
            );
        }
    }
);



const resumeSlice = createSlice({
    name: "resume",

    initialState: {
        currentResume: null,
        analysis: null,
        loading: false,
        analyzing: false,
        error: null,
    },

    reducers: {
        clearResumeError(state) {
            state.error = null;
        },
        clearResumeState(state) {
            state.currentResume = null;
            state.analysis = null;
            state.error = null;
        },
    },

    extraReducers: (builder) => {
        builder
            .addCase(uploadResume.pending, (state) => {
                state.loading = true;
                state.error = null;
            })

            .addCase(uploadResume.fulfilled, (state, action) => {
                state.loading = false;
                state.currentResume = action.payload;
            })

            .addCase(uploadResume.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })

            .addCase(analyzeResume.pending, (state) => {
                state.analyzing = true;
                state.error = null;
            })

            .addCase(analyzeResume.fulfilled, (state, action) => {
                state.analyzing = false;
                state.analysis = action.payload;
            })

            .addCase(analyzeResume.rejected, (state, action) => {
                state.analyzing = false;
                state.error = action.payload;
            });


    },
});


export const { clearResumeError, clearResumeState } = resumeSlice.actions;

export default resumeSlice.reducer;